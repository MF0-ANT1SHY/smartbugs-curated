import solcx
import json
import os
import csv
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Compile Solidity contracts based on versions.csv')
    parser.add_argument('--csv', required=True, help='Path to versions.csv file')
    parser.add_argument('--o', required=True, help='Output directory for compiled contracts')
    args = parser.parse_args()
    
    # Read CSV file
    with open(args.csv, 'r') as f:
        reader = csv.DictReader(f)
        contracts = list(reader)
    
    # Compile each contract
    for row in contracts:
        file_path = row['file'].strip()
        version = row['compiled version'].strip()
        
        if not file_path or not version:
            continue
        
        # Get the full path to the contract
        contract_path = Path(file_path)
        if not contract_path.exists():
            print(f"Warning: {file_path} does not exist, skipping...")
            continue
        
        # Determine output path (preserve directory structure)
        # e.g., dataset/access_control/file.sol -> output_dir/access_control/file.json
        relative_dir = contract_path.parent.name
        contract_name = contract_path.stem
        output_dir = Path(args.o) / relative_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{contract_name}.json"
        
        try:
            print(f"Compiling {file_path} with version {version}...")
            
            # Compile the contract
            result = solcx.compile_files(
                [str(contract_path)],
                output_values=["abi", "bin-runtime"],
                solc_version=version,
            )
            
            # Save the result
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"  -> Saved to {output_file}")
            
        except Exception as e:
            print(f"Error compiling {file_path}: {e}")
            continue


if __name__ == "__main__":
    main()
