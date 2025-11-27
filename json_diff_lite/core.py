"""Core diff functionality."""


def diff(a, b, prefix="", list_key=None):
    """
    Compare two JSON-like objects and return a list of human-readable differences.

    Args:
        a: The original object (dict, list, or primitive).
        b: The new object to compare against.
        prefix: Internal parameter for tracking nested paths.
        list_key: Key field(s) for matching list items. Can be a string or list of strings.
                  When provided, list items are matched by this field instead of by index.
                  Example: list_key="id" or list_key=["id", "name"]

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
                changes += diff(a[key], b[key], prefix=full_key, list_key=list_key)

        return changes

    if isinstance(a, list):
        # Try smart matching by key
        matched = _match_lists_by_key(a, b, list_key)

        if matched is not None:
            keys_a, keys_b, key_field = matched
            all_key_values = set(keys_a.keys()) | set(keys_b.keys())

            for key_value in sorted(all_key_values, key=lambda x: (type(x).__name__, str(x))):
                full_key = f"{prefix}[{key_field}={key_value!r}]"

                if key_value not in keys_a:
                    changes.append(f"+ {full_key}: {keys_b[key_value]!r}")
                elif key_value not in keys_b:
                    changes.append(f"- {full_key}: {keys_a[key_value]!r}")
                else:
                    changes += diff(keys_a[key_value], keys_b[key_value], prefix=full_key, list_key=list_key)
        else:
            # Fallback to index-based comparison
            max_len = max(len(a), len(b)) if a or b else 0
            for i in range(max_len):
                full_key = f"{prefix}[{i}]"

                if i >= len(a):
                    changes.append(f"+ {full_key}: {b[i]!r}")
                elif i >= len(b):
                    changes.append(f"- {full_key}: {a[i]!r}")
                else:
                    changes += diff(a[i], b[i], prefix=full_key, list_key=list_key)

        return changes

    if a != b:
        changes.append(f"~ {prefix}: {a!r} -> {b!r}")

    return changes


def _match_lists_by_key(list_a, list_b, list_key):
    """
    Try to match list items by a key field.

    Args:
        list_a: First list
        list_b: Second list
        list_key: Key field name (str) or list of field names to try

    Returns:
        Tuple of (keys_a, keys_b, key_field) if successful, None otherwise.
        keys_a and keys_b are dicts mapping key values to items.
    """
    if not list_key:
        return None

    # Normalize to list
    keys_to_try = [list_key] if isinstance(list_key, str) else list(list_key)

    for key_field in keys_to_try:
        keys_a = {}
        keys_b = {}
        success_a = True
        success_b = True

        for item in list_a:
            if isinstance(item, dict) and key_field in item:
                key_value = item[key_field]
                if key_value in keys_a:
                    # Duplicate key, can't use this field
                    success_a = False
                    break
                keys_a[key_value] = item
            else:
                success_a = False
                break

        if not success_a:
            continue

        for item in list_b:
            if isinstance(item, dict) and key_field in item:
                key_value = item[key_field]
                if key_value in keys_b:
                    success_b = False
                    break
                keys_b[key_value] = item
            else:
                success_b = False
                break

        if success_a and success_b:
            return keys_a, keys_b, key_field

    return None


def _is_primitive(value):
    """Check if a value is a JSON primitive type."""
    return isinstance(value, (int, float, str, bool, type(None)))
