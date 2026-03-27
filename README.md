# Zecpath AI - Applicant Tracking & Interview System

A modular, scalable AI repository designed for efficient developer workflows and high-performance screening.

## Project Structure

- `data/`: Raw and processed candidate data, resumes, and interview transcripts.
- `parsers/`: Document processing logic (PDF, Docx, etc.) for extracting text from resumes.
- `ats_engine/`: Core logic for the Applicant Tracking System, including candidate management.
- `screening_ai/`: AI models and scripts for automated screening of resumes against job descriptions.
- `interview_ai/`: AI models for generating and analyzing automated interview responses.
- `scoring/`: Quantitative scoring algorithms and evaluation metrics for candidate ranking.
- `utils/`: Common utilities including logging, configuration management, and API clients.
- `tests/`: Automated unit and integration tests using `pytest`.

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Initial Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Zecpath AI"
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   ```bash
   pytest
   ```

## Development Standards
- **Logging**: Use the centralized logger in `utils/logger.py`.
- **Testing**: All new features must include unit tests in the `tests/` directory.
- **Documentation**: Use Google-style docstrings for all functions and classes.
- **Formatting**: Adhere to PEP 8 standards.

## Logging System
The project uses `loguru` for structured logging. Logs are automatically saved to `logs/ai_system.log` and rotated once they reach 10MB.
