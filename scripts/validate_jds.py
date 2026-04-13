import os
import json
import jsonschema
from utils.logger import log

def validate_jds():
    schema_path = "data/schemas/jd_schema.json"
    data_dir = "data/processed_jds"
    
    if not os.path.exists(schema_path):
        log.error(f"Schema not found: {schema_path}")
        return
        
    with open(schema_path, 'r') as f:
        schema = json.load(f)
        
    files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    log.info(f"Validating {len(files)} JD JSONs...")
    
    success_count = 0
    error_count = 0
    
    for filename in files:
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        try:
            jsonschema.validate(instance=data, schema=schema)
            success_count += 1
        except jsonschema.exceptions.ValidationError as e:
            log.error(f"Validation failed for {filename}: {e.message}")
            error_count += 1
            
    log.info(f"Validation complete: {success_count} passed, {error_count} failed.")

if __name__ == "__main__":
    validate_jds()
