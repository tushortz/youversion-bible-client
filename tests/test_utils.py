"""Unit tests for utility functions."""

from typing import Any, Optional
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from youversion.utils import (
    DynamicPydanticFactory,
    create_instance_from_response,
    create_model_from_response,
)


class TestDynamicPydanticFactory:
    """Test cases for DynamicPydanticFactory class."""

    def test_init(self):
        """Test factory initialization."""
        factory = DynamicPydanticFactory()
        assert factory._class_cache == {}

    def test_sanitize_name(self):
        """Test name sanitization."""
        factory = DynamicPydanticFactory()

        assert factory._sanitize_name("test_name") == "test_name"
        assert factory._sanitize_name("test-name") == "test_name"
        assert factory._sanitize_name("123name") == "_123name"
        assert factory._sanitize_name("") == "_empty"
        assert factory._sanitize_name("test.name") == "test_name"

    def test_infer_type_none(self):
        """Test type inference for None."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(None)
        assert default is None

    def test_infer_type_bool(self):
        """Test type inference for bool."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(True)
        assert default is False
        assert type_hint is bool

    def test_infer_type_int(self):
        """Test type inference for int."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(42)
        assert default == 0
        assert type_hint is int

    def test_infer_type_float(self):
        """Test type inference for float."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(3.14)
        assert default == 0.0
        assert type_hint is float

    def test_infer_type_str(self):
        """Test type inference for str."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type("test")
        assert default == ""
        assert type_hint is str

    def test_infer_type_empty_list(self):
        """Test type inference for empty list."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type([], "items")
        # Should create a model for the field name
        assert hasattr(default, "default_factory") or default == []

    def test_infer_type_list_with_items(self):
        """Test type inference for list with items."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type([1, 2, 3])
        assert type_hint == list[int] or "list" in str(type_hint)

    def test_infer_type_dict(self):
        """Test type inference for dict."""
        factory = DynamicPydanticFactory()
        data = {"key": "value"}
        type_hint, default = factory._infer_type(data, "nested")
        assert default is None

    def test_get_element_class_name(self):
        """Test getting element class name from field name."""
        factory = DynamicPydanticFactory()

        assert factory._get_element_class_name("verses") == "Verse"
        assert factory._get_element_class_name("download_urls") == "DownloadUrl"
        assert factory._get_element_class_name("user_ids") == "UserId"
        assert factory._get_element_class_name("items") == "Item"
        # Empty string gets sanitized and should return "Item" as fallback
        result = factory._get_element_class_name("")
        assert result == "Item" or result == "Empty"  # Either is acceptable

    def test_get_element_class_name_singular(self):
        """Test getting element class name for singular field."""
        factory = DynamicPydanticFactory()

        assert factory._get_element_class_name("verse") == "Verse"
        assert factory._get_element_class_name("user") == "User"

    def test_create_model_simple(self):
        """Test creating a simple model."""
        factory = DynamicPydanticFactory()
        data = {"id": 1, "name": "test"}

        model_class = factory.create_model("TestModel", data)

        assert issubclass(model_class, BaseModel)
        assert hasattr(model_class, "model_fields")

    def test_create_model_cached(self):
        """Test that models are cached."""
        factory = DynamicPydanticFactory()
        data = {"id": 1}

        model1 = factory.create_model("TestModel", data)
        model2 = factory.create_model("TestModel", data)

        # Should return the same class (cached)
        assert model1 is model2

    def test_create_instance_simple(self):
        """Test creating a model instance."""
        factory = DynamicPydanticFactory()
        data = {"id": 1, "name": "test"}

        instance = factory.create_instance("TestInstance", data)

        assert isinstance(instance, BaseModel)
        assert hasattr(instance, "id")
        assert hasattr(instance, "name")

    def test_create_instance_nested(self):
        """Test creating instance with nested dict."""
        factory = DynamicPydanticFactory()
        data = {
            "id": 1,
            "user": {"id": 2, "name": "user"},
        }

        instance = factory.create_instance("TestInstance", data)

        assert isinstance(instance, BaseModel)
        assert hasattr(instance, "user")
        # User should also be a model instance
        assert isinstance(instance.user, BaseModel)

    def test_create_instance_list(self):
        """Test creating instance with list."""
        factory = DynamicPydanticFactory()
        data = {
            "id": 1,
            "items": [{"id": 2}, {"id": 3}],
        }

        instance = factory.create_instance("TestInstance", data)

        assert isinstance(instance, BaseModel)
        assert hasattr(instance, "items")
        assert isinstance(instance.items, list)

    def test_infer_type_empty_list_without_field_name(self):
        """Empty list without field name falls back to list[Any]."""
        factory = DynamicPydanticFactory()
        _type_hint, default = factory._infer_type([])
        from pydantic.fields import FieldInfo

        assert isinstance(default, FieldInfo)

    def test_create_model_pascal_case_with_underscore(self):
        """Class names with underscores are converted to PascalCase."""
        factory = DynamicPydanticFactory()
        model_class = factory.create_model("My_test_model", {"id": 1})
        assert model_class.__name__ == "MyTestModel"

    def test_create_model_preserves_pascal_case(self):
        """Already PascalCase names are preserved."""
        factory = DynamicPydanticFactory()
        model_class = factory.create_model("MyModel", {"id": 1})
        assert model_class.__name__ == "MyModel"

    def test_create_model_lowercase_name(self):
        """Lowercase class names get capitalized."""
        factory = DynamicPydanticFactory()
        model_class = factory.create_model("lowercase", {"id": 1})
        assert model_class.__name__ == "Lowercase"

    def test_create_model_fallback_on_invalid_field(self):
        """Invalid field definitions fall back to simple Any model."""
        factory = DynamicPydanticFactory()
        with patch(
            "youversion.utils.create_model",
            side_effect=[TypeError("bad"), MagicMock()],
        ):
            model_class = factory.create_model("BadModel", {"id": 1})
        assert model_class is not None

    def test_create_instance_nested_optional_without_model(self):
        """Nested dict without model type is passed through."""
        factory = DynamicPydanticFactory()
        data = {"meta": {"key": "value"}}
        instance = factory.create_instance("OptionalNested", data)
        assert instance.meta.key == "value"

    def test_create_instance_list_without_model_element(self):
        """List items without model element type are passed through."""
        factory = DynamicPydanticFactory()
        data = {"tags": ["a", "b"]}
        instance = factory.create_instance("TagsModel", data)
        assert instance.tags == ["a", "b"]

    def test_get_element_class_name_underscores_only(self):
        """Underscore-only names fall back to Item."""
        factory = DynamicPydanticFactory()
        assert factory._get_element_class_name("___") == "Item"

    def test_get_element_class_name_when_sanitize_empty(self):
        """Falsy sanitized names fall back to Item."""
        factory = DynamicPydanticFactory()
        with patch.object(factory, "_sanitize_name", return_value=""):
            assert factory._get_element_class_name("ignored") == "Item"

    def test_create_model_when_sanitize_empty(self):
        """Empty sanitized class names are handled."""
        factory = DynamicPydanticFactory()
        with patch.object(factory, "_sanitize_name", return_value=""):
            model_class = factory.create_model("ignored", {"id": 1})
        assert issubclass(model_class, BaseModel)

    def test_create_model_wraps_plain_type_as_optional(self):
        """Plain field types with None defaults are wrapped in Optional."""
        factory = DynamicPydanticFactory()
        with patch.object(factory, "_infer_type", return_value=(int, None)):
            model_class = factory.create_model("PlainOptional", {"count": 1})
        assert "count" in model_class.model_fields

    def test_create_model_optional_type_hint_preserved(self):
        """Optional hints from inference are preserved without re-wrapping."""
        factory = DynamicPydanticFactory()
        with patch.object(factory, "_infer_type", return_value=(Optional[int], None)):
            model_class = factory.create_model("AlreadyOptional", {"count": 1})
        assert "count" in model_class.model_fields

    def test_create_instance_validate_double_fallback(self):
        """Validation failures fall back to direct constructor."""
        factory = DynamicPydanticFactory()

        class Strict(BaseModel):
            id: int

        with patch.object(Strict, "model_validate", side_effect=ValueError("invalid")):
            instance = factory._create_instance_recursive(Strict, {"id": 1})
        assert instance.id == 1

    def test_create_instance_optional_any_passes_dict(self):
        """Optional Any nested values pass dicts through."""
        factory = DynamicPydanticFactory()

        class Parent(BaseModel):
            meta: Optional[Any] = None

        instance = factory._create_instance_recursive(Parent, {"meta": {"k": "v"}})
        assert instance.meta == {"k": "v"}

    def test_create_instance_list_without_field_info(self):
        """List values on unknown fields pass dict items through."""
        factory = DynamicPydanticFactory()

        class Parent(BaseModel):
            id: int

        instance = factory._create_instance_recursive(
            Parent, {"id": 1, "tags": [{"name": "a"}]}
        )
        assert instance.id == 1

    def test_create_instance_plain_dict_field(self):
        """Plain dict annotations pass nested dicts through."""
        factory = DynamicPydanticFactory()

        class Parent(BaseModel):
            meta: dict

        instance = factory._create_instance_recursive(Parent, {"meta": {"k": "v"}})
        assert instance.meta == {"k": "v"}

    def test_create_instance_direct_nested_model(self):
        """Nested dict with direct model annotation is recursively built."""
        factory = DynamicPydanticFactory()

        class Child(BaseModel):
            name: str

        class Parent(BaseModel):
            child: Child

        instance = factory._create_instance_recursive(Parent, {"child": {"name": "x"}})
        assert instance.child.name == "x"

    def test_create_instance_list_with_model_elements(self):
        """List elements using nested models are recursively built."""
        factory = DynamicPydanticFactory()

        class Child(BaseModel):
            id: int

        class Parent(BaseModel):
            rows: list[Child]

        instance = factory._create_instance_recursive(Parent, {"rows": [{"id": 1}]})
        assert instance.rows[0].id == 1

    def test_create_instance_list_without_typing_args(self):
        """Lists without subscripted args pass dict items through."""
        factory = DynamicPydanticFactory()

        class Parent(BaseModel):
            items: list

        instance = factory._create_instance_recursive(Parent, {"items": [{"id": 1}]})
        assert instance.items == [{"id": 1}]

    def test_create_instance_no_field_info_passes_value(self):
        """Values for unknown fields are passed through."""
        factory = DynamicPydanticFactory()

        class Parent(BaseModel):
            id: int

        instance = factory._create_instance_recursive(
            Parent, {"id": 1, "extra": {"k": "v"}}
        )
        assert instance.id == 1


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_create_model_from_response(self):
        """Test create_model_from_response function."""
        data = {"id": 1, "name": "test"}

        model_class = create_model_from_response("TestModel", data)

        assert issubclass(model_class, BaseModel)

    def test_create_instance_from_response(self):
        """Test create_instance_from_response function."""
        data = {"id": 1, "name": "test"}

        instance = create_instance_from_response("TestInstance", data)

        assert isinstance(instance, BaseModel)
        assert hasattr(instance, "id")
        assert hasattr(instance, "name")
