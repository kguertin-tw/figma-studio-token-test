import json
import sys
import os

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

def convert_and_append_file(file_path, locale_prefix=None):
    """
    Convert a JSON file and append it to the existing content_tokens_studio.json
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
    
    try:
        # Read the new file to convert
        with open(file_path, "r", encoding="utf-8") as f:
            new_data = json.load(f)
        
        # Load existing content_tokens_studio.json if it exists
        existing_data = {}
        if os.path.exists("content_tokens_studio.json"):
            with open("content_tokens_studio.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        
        # Convert the new data
        if isinstance(new_data, dict):
            # Create token sets optimized for Tokens Studio
            new_token_sets = create_token_sets(new_data, locale_prefix)
            
            # Merge with existing data
            for set_name, tokens in new_token_sets.items():
                if set_name in existing_data:
                    # If set already exists, add tokens (this will overwrite if same key, but that's expected with locale prefixes)
                    existing_data[set_name].update(tokens)
                    print(f"Added {len(tokens)} tokens to existing '{set_name}' set (keys with locale prefix will be added as new entries)")
                else:
                    # If set doesn't exist, add it
                    existing_data[set_name] = tokens
                    print(f"Added new '{set_name}' set with {len(tokens)} tokens")
        else:
            # If it's not a dict, create a single token set
            flattened = flatten_to_text_tokens(new_data)
            cleaned = {}
            for key, value in flattened.items():
                clean_key = key.replace('.value', '')
                if locale_prefix:
                    clean_key = f"{locale_prefix}.{clean_key}"
                cleaned[clean_key] = value
            
            # Add to global set or create one
            if "global" in existing_data:
                existing_data["global"].update(cleaned)
                print(f"Added {len(cleaned)} tokens to existing 'global' set (keys with locale prefix will be added as new entries)")
            else:
                existing_data["global"] = cleaned
                print(f"Added new 'global' set with {len(cleaned)} tokens")
        
        # Write the updated structure
        with open("content_tokens_studio.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully converted and appended '{file_path}' to content_tokens_studio.json")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return False

def main():
    """
    Main function to handle command line arguments and execute conversion
    """
    if len(sys.argv) < 2:
        print("Usage: python append_content.py <file_path> [locale_prefix]")
        print("Example: python append_content.py new_content.json EN")
        print("Example: python append_content.py additional_tokens.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    locale_prefix = sys.argv[2] if len(sys.argv) > 2 else None
    
    if locale_prefix:
        print(f"Using locale prefix: {locale_prefix}")
    
    success = convert_and_append_file(file_path, locale_prefix)
    
    if success:
        print("Conversion and append completed successfully!")
    else:
        print("Conversion failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
