import json

def flatten(obj, prefix="", out=None):
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            flatten(v, new_prefix, out)
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            new_prefix = f"{prefix}[{idx}]"
            flatten(v, new_prefix, out)
    elif isinstance(obj, str):
        out[prefix] = {"value": obj, "type": "string"}
    return out

with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# If the top-level keys are token sets, flatten each set separately
if isinstance(data, dict):
    sets = {}
    for set_name, set_value in data.items():
        if isinstance(set_value, dict):
            sets[set_name] = flatten(set_value)
        else:
            # If not a dict, skip or handle as needed
            pass
    output = sets
else:
    output = flatten(data)

with open("content.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4) 