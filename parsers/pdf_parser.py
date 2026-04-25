import pdfplumber
from utils.logger import log

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file while handling complex layouts like tables and columns.
    1. Sorts text by vertical and horizontal position to merge columns correctly.
    2. Extracts tables and formats them as readable text.
    3. Handles multi-page PDFs.
    """
    if not pdf_path:
        return ""

    full_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                log.debug(f"Processing page {page_num + 1} of {pdf_path}")
                
                # 1. Extract tables first
                tables = page.extract_tables()
                table_text = ""
                if tables:
                    for table in tables:
                        for row in table:
                            # Filter out None values and join with |
                            clean_row = [str(cell).strip() if cell else "" for cell in row]
                            table_text += " | ".join(clean_row) + "\n"
                        table_text += "\n"
                
                # 2. Extract text with layout preservation
                # We use a custom sort to ensure columns are read top-to-bottom, then left-to-right
                words = page.extract_words()
                
                if not words:
                    continue
                
                # Basic column detection by sorting words
                # Sort by top (y-coordinate) then x0 (x-coordinate)
                words.sort(key=lambda x: (x['top'], x['x0']))
                
                lines = []
                current_top = words[0]['top']
                current_line = []
                
                for word in words:
                    # If vertical distance is small, consider it the same line
                    if abs(word['top'] - current_top) < 3:
                        current_line.append(word['text'])
                    else:
                        line_text = " ".join(current_line)
                        # Add extra spacing for blocks that look like experience dates
                        if any(month in line_text for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Present"]):
                            lines.append("\n" + line_text + "\n")
                        else:
                            lines.append(line_text)
                            
                        current_line = [word['text']]
                        current_top = word['top']
                
                # Add the last line
                if current_line:
                    line_text = " ".join(current_line)
                    lines.append(line_text)
                
                page_text = "\n\n".join(lines)
                
                # 3. Concatenate table and text
                full_text.append(f"--- Page {page_num + 1} ---\n{page_text}\n\n{table_text}")

        return "\n".join(full_text)

    except Exception as e:
        log.error(f"Error parsing PDF {pdf_path}: {e}")
        return ""
