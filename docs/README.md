# Sphinx documentation

Build HTML docs from this directory.

## Build

```bash
cd docs
pip install sphinx==7.4.7 sphinx-rtd-theme==3.0.2
make html
```

Output: `build/html/index.html`

## Contents

| File | Topic |
|------|--------|
| `source/index.rst` | Overview and table of contents |
| `source/quickstart.rst` | First script |
| `source/examples.rst` | Common patterns |
| `source/cli.rst` | CLI commands |
| `source/api.rst` | Autodoc API reference |
| `source/clients.rst` | Client classes |

For a flat method list and sample JSON, see [DOCS.md](../DOCS.md) in the repo root.
