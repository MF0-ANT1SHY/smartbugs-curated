#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib.parse import quote, unquote

def dump_runtime_bytecode(json_file: Path, output_dir: Path, base_dir: Path):
    """Extract runtime bytecode from JSON and save to .hex files"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Preserve directory structure
    relative_path = json_file.parent.relative_to(base_dir)
    target_dir = output_dir / relative_path
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each contract in the JSON
    for contract_key, contract_data in data.items():
        contract_name = quote(contract_key, safe='') # Safe encoding for file names
        
        # Get runtime bytecode
        runtime_bytecode = contract_data.get('bin-runtime', '')
        
        # Write to .hex file
        output_file = target_dir / f"{contract_name}.hex"
        with open(output_file, 'w') as f:
            f.write(runtime_bytecode)


def main():
    parser = argparse.ArgumentParser(description='Dump runtime bytecode from JSON files to .hex files')
    parser.add_argument('--dir', required=True, help='Target directory containing JSON files')
    parser.add_argument('--o', required=True, help='Output directory for .hex files')
    
    args = parser.parse_args()
    
    target_dir = Path(args.dir)
    output_dir = Path(args.o)
    
    if not target_dir.exists():
        print(f"Error: Target directory '{target_dir}' does not exist")
        return
    
    # Recursively process all JSON files
    json_files = list(target_dir.rglob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in '{target_dir}'")
        return
    
    print(f"Processing {len(json_files)} JSON files...")
    
    for json_file in json_files:
        try:
            dump_runtime_bytecode(json_file, output_dir, target_dir)
            print(f"Processed: {json_file.relative_to(target_dir)}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    print(f"\nDone! Output saved to '{output_dir}'")


if __name__ == '__main__':
    main()
