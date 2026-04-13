import os
import glob
from typing import List
from utils.logger import log

def get_resume_files(directory: str) -> List[str]:
    """
    Finds all PDF and DOCX files in the specified directory.
    """
    if not os.path.exists(directory):
        log.warning(f"Directory {directory} does not exist.")
        return []

    # Get absolute paths of PDF and DOCX files
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    docx_files = glob.glob(os.path.join(directory, "*.docx"))
    
    all_files = pdf_files + docx_files
    log.info(f"Scanning {directory}: Found {len(all_files)} files.")
    
    return all_files

def save_processed_text(text: str, source_path: str, output_dir: str):
    """
    Saves the cleaned text into a .txt file in the output directory.
    Filename is based on the source filename.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(source_path))[0]
    output_filename = f"{base_name}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        log.info(f"Saved cleaned output to {output_path}")
    except Exception as e:
        log.error(f"Failed to save processed file {output_path}: {e}")
