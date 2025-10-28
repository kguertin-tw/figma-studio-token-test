import json
import sys

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

def create_token_sets(data, locale_prefix=None):
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
            
            # Add locale prefix if provided
            if locale_prefix:
                clean_key = f"{locale_prefix}.{clean_key}"
            
            cleaned[clean_key] = value
        
        # Organize into a clean structure for Tokens Studio
        token_sets[set_name] = cleaned
    
    return token_sets

# Read the original content
with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Check for locale prefix argument
locale_prefix = None
if len(sys.argv) > 1:
    locale_prefix = sys.argv[1]
    print(f"Using locale prefix: {locale_prefix}")

# Convert to Tokens Studio format
if isinstance(data, dict):
    # Create token sets optimized for Tokens Studio
    token_sets = create_token_sets(data, locale_prefix)
    
    # Create the final structure
    output = token_sets
else:
    # If it's not a dict, create a single token set
    flattened = flatten_to_text_tokens(data)
    cleaned = {}
    for key, value in flattened.items():
        clean_key = key.replace('.value', '')
        if locale_prefix:
            clean_key = f"{locale_prefix}.{clean_key}"
        cleaned[clean_key] = value
    output = {"global": cleaned}

# Write the optimized structure
with open("content_tokens_studio.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Conversion completed successfully!") 