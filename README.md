# json-diff-lite

A minimal, zero-dependency Python library for comparing JSON objects with human-readable output.

## Why?

Existing JSON diff libraries have their drawbacks:

| Library | Issue |
|---------|-------|
| **deepdiff** | Powerful but heavy, complex output |
| **jsondiff** | Unintuitive API, hard to interpret results |
| **dictdiffer** | Output as technical tuples, not human-friendly |
| **difflib** | Operates on strings, not structured JSON |

**json-diff-lite** is designed to be:
- Zero dependencies
- Minimal API
- Human-readable output
- Perfect for logs, debugging, and CI

## Installation

```bash
pip install json-diff-lite
```

## Usage

```python
from json_diff_lite import diff

old = {
    "name": "Ana",
    "age": 30,
    "address": {"street": "Rua A", "number": 100}
}

new = {
    "name": "Ana Maria",
    "age": 31,
    "address": {"street": "Rua B", "number": 100}
}

changes = diff(old, new)
for change in changes:
    print(change)
```

Output:
```
~ address.street: 'Rua A' -> 'Rua B'
~ age: 30 -> 31
~ name: 'Ana' -> 'Ana Maria'
```

### Output format

- `+` key: value — Added
- `- `key: value — Removed
- `~` key: old -> new — Modified

### Supported types

- Dicts (recursive)
- Lists (index-based comparison)
- Primitives: `str`, `int`, `float`, `bool`, `None`

## Limitations

Current version (v0.1.0) does **not** support:

- Smart list matching (by similarity or ID)
- Custom objects
- Colored output
- Unordered comparison tolerance

These features are planned for future releases.

## Development

```bash
# Clone the repository
git clone https://github.com/nilerbarcelos/json-diff-lite.git
cd json-diff-lite

# Install dev dependencies
pip install hatch

# Run tests
hatch run test:run
```

## Roadmap

### v0.1.0 — MVP (current)
- Basic diff for dict/list/primitives
- Human-readable output
- Tests

### v0.2.0 — CLI
```bash
json-diff-lite file1.json file2.json
```

### v0.3.0 — Colored output
- ANSI colors (optional)

### v0.4.0 — Smart list diffing
- Match list items by similarity

## License

MIT
