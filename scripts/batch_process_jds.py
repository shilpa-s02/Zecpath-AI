import os
from parsers.jd_parser import JDParser, save_jd_json
from utils.logger import log

def batch_process():
    input_dir = "data/tech_lead_jds"
    output_dir = "data/processed_jds"
    
    parser = JDParser()
    
    if not os.path.exists(input_dir):
        log.error(f"Input directory {input_dir} not found.")
        return
        
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    log.info(f"Batch processing {len(files)} files into structured JSON...")
    
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        try:
            structured_data = parser.parse_file(file_path)
            
            # Use original index/title for filename but with .json
            json_name = filename.replace('.txt', '.json')
            output_path = os.path.join(output_dir, json_name)
            
            save_jd_json(structured_data, output_path)
        except Exception as e:
            log.error(f"Failed to process {filename}: {e}")

    log.info(f"Successfully processed {len(files)} files to {output_dir}/")

if __name__ == "__main__":
    batch_process()
