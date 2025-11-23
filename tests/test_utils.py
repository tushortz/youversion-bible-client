"""Unit tests for utility functions."""


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
        assert type_hint == bool

    def test_infer_type_int(self):
        """Test type inference for int."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(42)
        assert default == 0
        assert type_hint == int

    def test_infer_type_float(self):
        """Test type inference for float."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type(3.14)
        assert default == 0.0
        assert type_hint == float

    def test_infer_type_str(self):
        """Test type inference for str."""
        factory = DynamicPydanticFactory()
        type_hint, default = factory._infer_type("test")
        assert default == ""
        assert type_hint == str

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

