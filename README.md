git add README.md
git commit -m "Add CI status badge"
git push origin main
# Intelligent Document Processing (IDP) Pipeline

## Overview

The Intelligent Document Processing (IDP) Pipeline automates the extraction of structured data from noisy receipts and other document images. By leveraging Optical Character Recognition (OCR) and optional advanced language model integrations, it efficiently captures critical information including vendor details, itemized transactions (SKU, quantity, and price), and payment totals. This tool helps reduce manual data entry, improve accuracy, and enhance business efficiency.

## Key Features

* **OCR Text Extraction:**

  * Reliable text extraction using Tesseract OCR with minimal preprocessing.

* **Structured Data Extraction:**

  * Optional integration with advanced language models (e.g., OpenAI) to produce structured JSON data.

* **REST API Endpoints:**

  * `POST /extract`: Runs OCR and returns raw text.
  * `POST /extract_structured`: Performs OCR and returns structured JSON containing vendor details, line items, payment totals, and raw extracted text.

* **Dry Run Mode:**

  * Provides deterministic mock data output by default, ideal for testing without external API keys or associated costs.

* **Real Parsing Mode:**

  * Enable actual parsing by configuring environment variables:

```bash
DRY_RUN=0
OPENAI_API_KEY=<your-api-key>
```

## Technologies Used

* Python for backend scripting and processing.
* Tesseract OCR for reliable optical character recognition.
* Flask for creating RESTful API endpoints.
* Pydantic for data validation and structured schemas.
* OpenAI (optional) for advanced text parsing capabilities.

## Quick Start Guide

Follow these steps to set up and run the IDP Pipeline locally:

```bash
git clone https://github.com/mohanreddy6/idp-pipeline.git
cd idp-pipeline

python -m venv .venv
# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Start the Flask API
python app.py
```

## Project Structure

```
idp-pipeline/
├── README.md
├── requirements.txt
├── app.py
├── scripts/
│   ├── ocr.py
│   └── parser.py
└── tests/
    ├── test_ocr.py
    └── test_parser.py
```

## Links

* [GitHub Repository](https://github.com/mohanreddy6/idp-pipeline)
* [Live Demo](https://idp-pipeline.onrender.com)

## Limitations and Error Handling

* Effective with clear document images; less effective with poor scans or unclear images.
* Users may experience inaccuracies in OCR text extraction from poorly formatted documents.
* Advanced parsing requires an active API key and internet connectivity.

## Testing and Reliability

The IDP Pipeline includes unit tests to verify functionality and maintain reliability. Integration with continuous integration and continuous deployment (CI/CD) pipelines is recommended for ongoing automated validation.

## Future Enhancements

* Integration with Docker and AWS Lambda for scalable deployment.
* Improvement of parsing accuracy with advanced NLP models.
* Expansion to handle additional document formats and extraction types.
