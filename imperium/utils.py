def write_to_env(env_path, config_dict, append=False):
    """
    Generates a .env file by flattening the provided dictionary.
    If append is True, appends lines instead of overwriting.
    """

    lines = [f"{k}={v}" for k, v in flatten_dict(config_dict)]
    mode = "a" if append else "w"

    with open(env_path, mode, encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def flatten_dict(d, parent_key=""):
    items = []
    # Recursively append parent key to the key until a non-dictionary value is found
    for k, v in d.items():
        new_key = f"{parent_key}_{k.upper()}" if parent_key else k.upper()
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key))
        else:
            items.append((new_key, v))
    return items
