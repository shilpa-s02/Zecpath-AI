import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.jd_parser import JDParser, save_jd_json
from parsers.resume_parser import ResumeParser, save_resume_json
from utils.text_cleaner import clean_text
from utils.file_handler import get_resume_files, save_processed_text
from utils.logger import log

def run_jd_pipeline(jd_dir="data/tech_lead_jds", output_dir="data/processed_jds"):
    """
    Pipeline for processing Job Descriptions into schema-compliant JSON.
    """
    log.info("Starting Job Description Extraction Engine...")
    
    if not os.path.exists(jd_dir):
        log.warning(f"JD directory {jd_dir} not found.")
        return

    parser = JDParser()
    files = [f for f in os.listdir(jd_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
    
    if not files:
        log.warning(f"No JD files found in {jd_dir}")
        return

    log.info(f"Found {len(files)} JDs to process.")

    for filename in files:
        file_path = os.path.join(jd_dir, filename)
        try:
            log.info(f"Processing JD: {filename}")
            structured_data = parser.parse_file(file_path)
            
            json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, json_name)
            
            save_jd_json(structured_data, output_path)
            log.success(f"Successfully structured JD: {filename}")

        except Exception as e:
            log.error(f"Error processing JD {filename}: {str(e)}")

def run_extraction_pipeline(resume_dir="data/resumes", output_dir="data/processed"):
    # ... (existing code for resumes)
    """
    Main orchestration function for the Resume Text Extraction Engine.
    1. Reads files from data/resumes
    2. Parses PDF/DOCX
    3. Cleans text
    4. Saves to data/processed
    """
    log.info("Starting Resume Text Extraction Engine...")
    
    # Ensure input directory exists
    if not os.path.exists(resume_dir):
        log.warning(f"Input directory {resume_dir} not found. Creating it.")
        os.makedirs(resume_dir, exist_ok=True)
        return

    files = get_resume_files(resume_dir)
    if not files:
        log.warning(f"No supported resume files found in {resume_dir}")
        log.info("Place your PDF/DOCX resumes in 'data/resumes/' and run again.")
        return

    log.info(f"Found {len(files)} files to process.")

    parser = ResumeParser()

    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            log.info(f"Processing: {filename}")
            
            # Use the new ResumeParser which handles extraction, cleaning, and classification
            structured_data = parser.parse_file(file_path)

            if not structured_data:
                log.error(f"Failed to parse {filename}")
                continue

            # Save as JSON instead of TXT
            json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, json_name)
            
            save_resume_json(structured_data, output_path)
            log.success(f"Successfully structured resume: {filename}")

        except Exception as e:
            log.exception(f"Unexpected error processing {file_path}: {str(e)}")

    log.info("Extraction pipeline completed.")

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # 1. Run Resume Extraction Pipeline
    run_extraction_pipeline(output_dir="output/resume_data")
    
    # 2. Run Job Description Extraction Pipeline
    # Using the 107 split JDs as source
    run_jd_pipeline(jd_dir="data/tech_lead_jds", output_dir="output/job_data")
