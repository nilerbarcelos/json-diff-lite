"""Core diff functionality."""


def diff(a, b, prefix=""):
    """
    Compare two JSON-like objects and return a list of human-readable differences.

    Args:
        a: The original object (dict, list, or primitive).
        b: The new object to compare against.
        prefix: Internal parameter for tracking nested paths.

    Returns:
        A list of strings describing the differences:
        - '+' for additions
        - '-' for removals
        - '~' for modifications
    """
    changes = []

    if _is_primitive(a) and _is_primitive(b):
        if a != b:
            changes.append(f"~ {prefix}: {a!r} -> {b!r}")
        return changes

    if type(a) != type(b):
        changes.append(f"~ {prefix}: {a!r} -> {b!r}")
        return changes

    if isinstance(a, dict):
        all_keys = set(a.keys()) | set(b.keys())

        for key in sorted(all_keys):
            full_key = f"{prefix}.{key}" if prefix else key

            if key not in a:
                changes.append(f"+ {full_key}: {b[key]!r}")
            elif key not in b:
                changes.append(f"- {full_key}: {a[key]!r}")
            else:
                changes += diff(a[key], b[key], prefix=full_key)

        return changes

    if isinstance(a, list):
        max_len = max(len(a), len(b))
        for i in range(max_len):
            full_key = f"{prefix}[{i}]"

            if i >= len(a):
                changes.append(f"+ {full_key}: {b[i]!r}")
            elif i >= len(b):
                changes.append(f"- {full_key}: {a[i]!r}")
            else:
                changes += diff(a[i], b[i], prefix=full_key)

        return changes

    if a != b:
        changes.append(f"~ {prefix}: {a!r} -> {b!r}")

    return changes


def _is_primitive(value):
    """Check if a value is a JSON primitive type."""
    return isinstance(value, (int, float, str, bool, type(None)))
