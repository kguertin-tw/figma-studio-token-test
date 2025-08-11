import json

def flatten_to_text_tokens(obj, prefix="", out=None):
    """
    Flatten nested structure to create clean text tokens for Tokens Studio
    """
    if out is None:
        out = {}
    
    if isinstance(obj, dict):
        # Check if this is already a token (has 'value' and 'type')
        if 'value' in obj and 'type' in obj and obj['type'] == 'string':
            # Clean up the prefix by removing '.value' if it exists
            clean_prefix = prefix.replace('.value', '') if prefix.endswith('.value') else prefix
            out[clean_prefix] = {
                "value": obj['value'],
                "type": "text"  # Use 'text' type for Tokens Studio
            }
        else:
            # Continue flattening nested structure
            for k, v in obj.items():
                new_prefix = f"{prefix}.{k}" if prefix else k
                flatten_to_text_tokens(v, new_prefix, out)
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            new_prefix = f"{prefix}[{idx}]"
            flatten_to_text_tokens(v, new_prefix, out)
    elif isinstance(obj, str):
        out[prefix] = {"value": obj, "type": "text"}
    
    return out

def create_token_sets(data):
    """
    Create properly structured token sets for Tokens Studio
    """
    token_sets = {}
    
    for set_name, set_data in data.items():
        # Create a flattened token set
        flattened = flatten_to_text_tokens(set_data)
        
        # Clean up any remaining '.value' suffixes in keys
        cleaned = {}
        for key, value in flattened.items():
            clean_key = key.replace('.value', '')
            cleaned[clean_key] = value
        
        # Organize into a clean structure for Tokens Studio
        token_sets[set_name] = cleaned
    
    return token_sets

# Read the original content
with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to Tokens Studio format
if isinstance(data, dict):
    # Create token sets optimized for Tokens Studio
    token_sets = create_token_sets(data)
    
    # Create the final structure
    output = token_sets
else:
    # If it's not a dict, create a single token set
    output = {"global": flatten_to_text_tokens(data)}

# Write the optimized structure
with open("content_tokens_studio.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2) 