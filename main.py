import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.jd_parser import JDParser, save_jd_json
from parsers.resume_parser import ResumeParser, save_resume_json
from utils.text_cleaner import clean_text
from utils.file_handler import get_resume_files, save_processed_text
from utils.aggregator import aggregate_resume_results
from utils.logger import log

def run_jd_pipeline(jd_dir="data/tech_lead_jds", output_dir="output/job_data"):
    """
    Pipeline for processing Job Descriptions into schema-compliant JSON.
    """
    log.info("Starting Job Description Extraction Engine...")
    
    if not os.path.exists(jd_dir):
        log.warning(f"JD directory {jd_dir} not found.")
        return 0

    parser = JDParser()
    files = [f for f in os.listdir(jd_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
    
    if not files:
        log.warning(f"No JD files found in {jd_dir}")
        return 0

    log.info(f"Found {len(files)} JDs to process.")
    success_count = 0

    for filename in files:
        file_path = os.path.join(jd_dir, filename)
        try:
            log.info(f"Processing JD: {filename}")
            structured_data = parser.parse_file(file_path)
            
            json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, json_name)
            
            save_jd_json(structured_data, output_path)
            log.success(f"Successfully structured JD: {filename}")
            success_count += 1

        except Exception as e:
            log.error(f"Error processing JD {filename}: {str(e)}")
    
    return success_count

def run_extraction_pipeline(resume_dir="data/resumes", output_dir="output/resume_data"):
    """
    Main orchestration function for the Resume Text Extraction Engine.
    """
    log.info("Starting Resume Text Extraction Engine...")
    
    # Ensure input directory exists
    if not os.path.exists(resume_dir):
        log.warning(f"Input directory {resume_dir} not found. Creating it.")
        os.makedirs(resume_dir, exist_ok=True)
        return 0

    files = get_resume_files(resume_dir)
    if not files:
        log.warning(f"No supported resume files found in {resume_dir}")
        return 0

    log.info(f"Found {len(files)} files to process.")
    success_count = 0
    parser = ResumeParser()

    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            log.info(f"Processing: {filename}")
            
            structured_data = parser.parse_file(file_path)

            if not structured_data:
                log.error(f"Failed to parse {filename}")
                continue

            json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, json_name)
            
            save_resume_json(structured_data, output_path)
            log.success(f"Successfully structured resume: {filename}")
            success_count += 1

        except Exception as e:
            log.exception(f"Unexpected error processing {file_path}: {str(e)}")

    log.info("Extraction pipeline completed.")
    return success_count

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    log.info("=== ZECPATH AI PIPELINE START ===")
    
    # 1. Run Resume Extraction Pipeline
    res_count = run_extraction_pipeline()
    
    # 2. Run Job Description Extraction Pipeline
    jd_count = run_jd_pipeline()

    # 3. Aggregate results into summary JSON
    aggregate_resume_results("output/resume_data", "output/day10_results/result.json")
    log.info("Aggregated results into output/day10_results/result.json")
    
    log.info("=== ZECPATH AI PIPELINE SUMMARY ===")
    log.success(f"Processed Resumes: {res_count}")
    log.success(f"Processed Job Descriptions: {jd_count}")
    log.info("Done.")
