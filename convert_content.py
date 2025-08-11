import json

def convert(obj):
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert(i) for i in obj]
    elif isinstance(obj, str):
        return {"value": obj}
    else:
        return obj

with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

converted = convert(data)

with open("content.json", "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=4) 