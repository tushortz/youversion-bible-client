"""Utility functions for YouVersion API client."""

import re
from typing import Any, Optional

from pydantic import BaseModel, Field, create_model


class DynamicPydanticFactory:
    """Factory for creating Pydantic models dynamically from API responses."""

    def __init__(self):
        """Initialize the factory with a cache for generated classes."""
        self._class_cache: dict[str, type[BaseModel]] = {}

    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name to be a valid Python identifier.

        Args:
            name: Original name

        Returns:
            Sanitized name valid as Python identifier
        """
        # Replace invalid characters with underscores
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        # Ensure it doesn't start with a number
        if name and name[0].isdigit():
            name = "_" + name
        # Ensure it's not empty
        if not name:
            name = "_empty"
        return name

    def _infer_type(
        self, value: Any, field_name: str = ""
    ) -> tuple[Any, Any]:
        """Infer Python type from a value.

        Args:
            value: Value to infer type from
            field_name: Name of the field (for context)

        Returns:
            Tuple of (type, default_value)
        """
        if value is None:
            return (Optional[Any], None)
        elif isinstance(value, bool):
            return (bool, False)
        elif isinstance(value, int):
            return (int, 0)
        elif isinstance(value, float):
            return (float, 0.0)
        elif isinstance(value, str):
            return (str, "")
        elif isinstance(value, list):
            if not value:
                # Empty list - can't infer element type
                # Use field_name to create model name
                # (e.g., "verses" -> "Verse")
                if field_name:
                    # Singularize and PascalCase: "verses" -> "Verse"
                    element_class_name = (
                        self._get_element_class_name(field_name)
                    )
                    element_class = self.create_model(element_class_name, {})
                    return (list[element_class], Field(default_factory=list))
                return (list[Any], Field(default_factory=list))
            # Infer type from first element
            # Use field_name to create model name for dict elements
            if isinstance(value[0], dict) and field_name:
                element_class_name = (
                    self._get_element_class_name(field_name)
                )
                element_type, _ = self._infer_type(
                    value[0], element_class_name
                )
            else:
                element_type, _ = self._infer_type(value[0], field_name)
            return (list[element_type], Field(default_factory=list))
        elif isinstance(value, dict):
            # Nested dict - create a nested Pydantic model
            nested_class_name = (
                self._get_element_class_name(field_name)
                if field_name
                else self._sanitize_name(field_name)
            )
            nested_class = self.create_model(nested_class_name, value)
            # Return as optional type with None default
            return (Optional[nested_class], None)
        else:
            return (Any, None)

    def _get_element_class_name(self, field_name: str) -> str:
        """Get a class name for list elements based on field name.

        Converts snake_case to PascalCase and handles plural forms.
        Examples: "download_urls" -> "DownloadUrl", "user_ids" -> "UserId"

        Args:
            field_name: Field name (e.g., "verses", "download_urls", "results")

        Returns:
            Singularized and PascalCase class name
            (e.g., "Verse", "DownloadUrl")
        """
        sanitized = self._sanitize_name(field_name)
        if sanitized:
            # Handle plural forms: remove trailing 's' if present
            if sanitized.endswith("s") and len(sanitized) > 1:
                singular = sanitized[:-1]
            else:
                singular = sanitized

            # Convert snake_case to PascalCase
            # Split by underscore, capitalize each word, then join
            parts = singular.split("_")
            # Check if already in PascalCase
            # (no underscores and has mixed case)
            if len(parts) == 1 and singular[0].isupper():
                # Already PascalCase - preserve it
                pascal_case = singular
            else:
                # Convert to PascalCase: capitalize each word
                pascal_case = "".join(
                    word.capitalize() for word in parts if word
                )

            # Ensure it's not empty after processing
            if not pascal_case or pascal_case == "_empty":
                return "Item"
            return pascal_case
        return "Item"

    def create_model(
        self, class_name: str, data: dict[str, Any]
    ) -> type[BaseModel]:
        """Create a Pydantic model dynamically from a dictionary.

        Args:
            class_name: Name for the generated class
            data: Dictionary containing the data structure

        Returns:
            Generated Pydantic model class
        """
        # Sanitize class name first
        sanitized = self._sanitize_name(class_name)
        # Check if already in PascalCase (multiple capital letters)
        if sanitized and sanitized[0].isupper():
            # Check if it's already PascalCase
            # (has multiple words or is single word)
            # If it contains underscores, convert to PascalCase
            if "_" in sanitized:
                parts = sanitized.split("_")
                final_class_name = "".join(
                    word.capitalize() for word in parts if word
                )
            else:
                # Already PascalCase or single word - preserve it
                final_class_name = sanitized
        elif sanitized:
            # Not uppercase, capitalize first letter only
            final_class_name = sanitized.capitalize()
        else:
            final_class_name = sanitized

        # Check cache with sanitized class name
        cache_key = f"{final_class_name}_{id(data)}"
        if cache_key in self._class_cache:
            return self._class_cache[cache_key]

        # Use final_class_name for model creation
        class_name = final_class_name

        # Build field definitions for Pydantic
        # Make all fields optional to avoid field ordering issues
        field_definitions: dict[str, tuple[Any, Any]] = {}

        for key, value in data.items():
            field_name = self._sanitize_name(key)
            field_type, default_value = self._infer_type(value, field_name)

            # Handle different default value types
            # Check if default_value is a Field instance by checking type name
            if (
                default_value is not None
                and hasattr(default_value, "__class__")
                and default_value.__class__.__name__ == "FieldInfo"
            ):
                # Already a Pydantic Field
                field_definitions[field_name] = (field_type, default_value)
            elif default_value is None:
                # Optional field with None default
                type_str = str(field_type)
                if "Optional" in type_str or "Union" in type_str:
                    optional_type = field_type
                else:
                    optional_type = Optional[field_type]
                field_definitions[field_name] = (optional_type, None)
            else:
                # Field with explicit default value
                field_definitions[field_name] = (field_type, default_value)

        # Create the Pydantic model
        try:
            generated_class = create_model(class_name, **field_definitions)

            # Cache the class
            self._class_cache[cache_key] = generated_class

            return generated_class
        except (TypeError, ValueError):
            # Fallback to a simple model if creation fails
            fallback_fields = {
                self._sanitize_name(k): (Any, None) for k in data.keys()
            }
            return create_model(class_name, **fallback_fields)

    def create_instance(
        self, class_name: str, data: dict[str, Any]
    ) -> Any:
        """Create a Pydantic model instance from a dictionary.

        Args:
            class_name: Name for the generated class
            data: Dictionary containing the data

        Returns:
            Instance of the generated Pydantic model
        """
        model_type = self.create_model(class_name, data)
        return self._create_instance_recursive(model_type, data)

    def _create_instance_recursive(
        self, model_type: type[BaseModel], data: dict[str, Any]
    ) -> Any:
        """Recursively create Pydantic model instance.

        Handles nested dictionaries and lists, creating model instances.

        Args:
            model_type: The Pydantic model type to instantiate
            data: Dictionary containing the data

        Returns:
            Instance of the Pydantic model
        """
        processed_data = {}

        for key, value in data.items():
            field_name = self._sanitize_name(key)

            # Handle nested dictionaries
            if isinstance(value, dict):
                # Check if the field type is a nested model
                field_info = model_type.model_fields.get(field_name)
                if field_info:
                    annotation = field_info.annotation
                    # Handle Optional types
                    if hasattr(annotation, "__args__"):
                        args = annotation.__args__
                        # Find the model type in Optional[ModelType]
                        nested_class = None
                        for arg in args:
                            if hasattr(arg, "model_fields"):
                                nested_class = arg
                                break
                        if nested_class:
                            processed_data[field_name] = (
                                self._create_instance_recursive(
                                    nested_class, value
                                )
                            )
                        else:
                            # No model type found, pass dict
                            processed_data[field_name] = value
                    elif hasattr(annotation, "model_fields"):
                        # Direct model type
                        processed_data[field_name] = (
                            self._create_instance_recursive(annotation, value)
                        )
                    else:
                        # dict type, pass as-is
                        processed_data[field_name] = value
                else:
                    # No field info, pass as-is
                    processed_data[field_name] = value
            # Handle lists
            elif isinstance(value, list):
                processed_list = []
                for item in value:
                    if isinstance(item, dict):
                        # Check if list element type is a model
                        field_info = model_type.model_fields.get(field_name)
                        if field_info:
                            annotation = field_info.annotation
                            # Handle list[ModelType] or list[Any]
                            if hasattr(annotation, "__args__"):
                                element_type = annotation.__args__[0]
                                if hasattr(element_type, "model_fields"):
                                    item_class = element_type
                                    processed_list.append(
                                        self._create_instance_recursive(
                                            item_class, item
                                        )
                                    )
                                else:
                                    processed_list.append(item)
                            else:
                                processed_list.append(item)
                        else:
                            processed_list.append(item)
                    else:
                        processed_list.append(item)
                processed_data[field_name] = processed_list
            else:
                processed_data[field_name] = value

        # Pydantic models handle extra fields and validation automatically
        # Use model_validate for better compatibility with Pydantic v2
        try:
            return model_type.model_validate(processed_data)
        except Exception:
            # If validation fails, try with only known fields
            model_fields = set(model_type.model_fields.keys())
            filtered_data = {
                k: v for k, v in processed_data.items() if k in model_fields
            }
            try:
                return model_type.model_validate(filtered_data)
            except Exception:
                # Last resort: try direct instantiation
                return model_type(**filtered_data)


# Global factory instance
_factory = DynamicPydanticFactory()


def create_model_from_response(
    class_name: str, data: dict[str, Any]
) -> type[BaseModel]:
    """Create a Pydantic model dynamically from an API response.

    Args:
        class_name: Name for the generated class
        data: Dictionary containing the API response data

    Returns:
        Generated Pydantic model class

    Example:
        >>> response = {"id": 1, "name": "Test"}
        >>> MyClass = create_model_from_response("MyResponse", response)
        >>> instance = MyClass(id=1, name="Test")
    """
    return _factory.create_model(class_name, data)


def create_instance_from_response(
    class_name: str, data: dict[str, Any]
) -> Any:
    """Create a Pydantic model instance from an API response.

    Args:
        class_name: Name for the generated class
        data: Dictionary containing the API response data

    Returns:
        Instance of the generated Pydantic model

    Example:
        >>> response = {"id": 1, "name": "Test"}
        >>> instance = create_instance_from_response("MyResponse", response)
        >>> print(instance.id)  # 1
    """
    return _factory.create_instance(class_name, data)


# Backward compatibility aliases
create_dataclass_from_response = create_model_from_response
