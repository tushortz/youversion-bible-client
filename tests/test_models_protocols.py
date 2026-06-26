"""Coverage for model protocol __getattr__ and package exports."""

from __future__ import annotations

import importlib

import pytest

PROTOCOL_MODULES = [
    "youversion.models.base",
    "youversion.models.bible",
    "youversion.models.common",
    "youversion.models.commons",
    "youversion.models.events",
    "youversion.models.friends",
    "youversion.models",
]


def _protocol_classes(module) -> list[type]:
    return [
        obj
        for name, obj in vars(module).items()
        if name.endswith("Protocol") and hasattr(obj, "__getattr__")
    ]


@pytest.mark.parametrize("module_name", PROTOCOL_MODULES)
def test_protocol_modules_import(module_name):
    importlib.import_module(module_name)


@pytest.mark.parametrize("module_name", PROTOCOL_MODULES)
def test_protocol_getattr_raises(module_name):
    module = importlib.import_module(module_name)
    for proto in _protocol_classes(module):
        stub = type("Stub", (), {"__class__": type("Stub", (), {})})()
        with pytest.raises(AttributeError, match="has no attribute 'missing_field'"):
            proto.__getattr__(stub, "missing_field")


def test_models_package_exports():
    import youversion.models as models

    for name in models.__all__:
        assert hasattr(models, name)
