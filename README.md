# LegalEase

LegalEase is an AI-powered legal document drafting application.

## Technologies

- Python
- Streamlit
- FastAPI
- Google Gemini
- python-docx
- FPDF2
- Requests
- Pytest

## Features

- AI legal document generation
- Editable document preview
- TXT download
- DOCX download
- PDF download
- Company logo upload
- FastAPI REST API
- API documentation
- Automated tests

## Project Structure

```text
LegalEase/
│
├── app.py
├── requirements.txt
├── .env
│
├── backend/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── ai_core/
│   └── gemini_generator.py
│
├── services/
│   ├── document_service.py
│   └── sanitization.py
│
├── tests/
│   ├── test_api.py
│   └── test_document_service.py
│
└── assets/
    └── logo.svg
