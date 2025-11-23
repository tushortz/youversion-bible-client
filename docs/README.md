# YouVersion Bible Client Documentation

This directory contains the Sphinx documentation for the YouVersion Bible Client.

## Building the Documentation

### Prerequisites

Install the required dependencies:

```bash
# Install Sphinx and theme
pip install sphinx==7.4.7 sphinx-rtd-theme==3.0.2

# Or using Poetry (already included in dev dependencies)
poetry install --with dev
```

### Building HTML Documentation

```bash
# Navigate to the documentation directory
cd documentation

# Build HTML documentation
make html

# Or using sphinx-build directly
sphinx-build -b html source build
```

The built documentation will be available in the `build/html` directory.

### Building Other Formats

```bash
# Build PDF documentation
make latexpdf

# Build EPUB documentation
make epub

# Build man pages
make man
```

### Viewing the Documentation

After building, open `build/html/index.html` in your web browser to view the documentation.

## Documentation Structure

- `source/index.rst` - Main documentation page
- `source/clients.rst` - Client documentation
- `source/models.rst` - Data models documentation
- `source/cli.rst` - Command-line interface documentation
- `source/examples.rst` - Usage examples
- `source/api.rst` - Complete API reference (auto-generated)
- `source/conf.py` - Sphinx configuration

## Writing Documentation

The documentation uses reStructuredText (RST) format. Key features:

- **Code blocks**: Use `.. code-block:: python` for syntax highlighting
- **Cross-references**: Use `:class:`Class`` for class references
- **Sections**: Use `=` for main sections, `-` for subsections
- **Lists**: Use `*` for bullet points, `#.` for numbered lists
- **Admonitions**: Use `.. warning::`, `.. note::`, etc.

## Auto-Documentation

The documentation uses Sphinx autodoc to automatically generate API documentation from docstrings. Make sure your Python code has proper docstrings:

```python
class MyClass:
    """Brief description of the class.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """

    def my_method(self, param):
        """Brief description of the method.

        Args:
            param: Description of the parameter

        Returns:
            Description of the return value

        Raises:
            ValueError: When something goes wrong
        """
        pass
```

## Updating Documentation

When making changes to the code:

1. Update relevant RST files in `source/`
2. Add or update docstrings in Python code
3. Rebuild the documentation
4. Check for any warnings or errors

## Configuration

The Sphinx configuration is in `source/conf.py`. Key settings:

- **Extensions**: autodoc, napoleon, viewcode, etc.
- **Theme**: sphinx_rtd_theme (Read the Docs theme)
- **Path**: Points to the parent directory for imports
- **Version**: Set to current version

## Troubleshooting

### Import Errors

If you get import errors when building:

1. Make sure the Python path is correct in `conf.py`
2. Ensure all dependencies are installed
3. Check that the package can be imported from the documentation directory

### Missing Documentation

If some classes or methods are missing:

1. Check that they have proper docstrings
2. Verify they're included in the appropriate `.. automodule::` directive
3. Make sure they're not excluded by `exclude_patterns` in `conf.py`

### Theme Issues

If the theme doesn't look right:

1. Ensure `sphinx_rtd_theme` is installed
2. Check `html_theme` setting in `conf.py`
3. Clear the build directory and rebuild
