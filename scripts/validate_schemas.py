import os
import json
from jsonschema import validate, ValidationError

def validate_files(directory, schema_path):
    print(f"Validating files in {directory} against {schema_path}...")
    
    with open(schema_path, 'r') as f:
        schema = json.load(f)
        
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    if not files:
        print(f"No files found in {directory}")
        return True

    all_valid = True
    for filename in files:
        path = os.path.join(directory, filename)
        with open(path, 'r') as f:
            data = json.load(f)
            try:
                validate(instance=data, schema=schema)
                print(f"  [PASS] {filename}")
            except ValidationError as e:
                print(f"  [FAIL] {filename}: {e.message}")
                all_valid = False
            except Exception as e:
                print(f"  [ERROR] {filename}: {str(e)}")
                all_valid = False
                
    return all_valid

if __name__ == "__main__":
    resume_valid = validate_files("output/resume_data", "data/schemas/resume_schema.json")
    jd_valid = validate_files("output/job_data", "data/schemas/jd_schema.json")
    
    if resume_valid and jd_valid:
        print("All files are schema-compliant!")
        exit(0)
    else:
        print("Some files failed schema validation.")
        exit(1)
