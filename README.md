\# Intelligent Document Processing (IDP) Pipeline



LLM-based pipeline to extract \*\*vendor metadata\*\*, \*\*line items (SKU/qty/price)\*\*, and \*\*payment totals\*\* from \*\*noisy receipts\*\*.



\*\*Tech\*\*: Python · Tesseract OCR · Flask API · Pydantic · (Optional) OpenAI via LangChain-like prompt · Docker (later) · AWS Lambda (later)



---



\## Features

\- OCR with Tesseract (preprocessing kept minimal for reliability)

\- REST API:

&nbsp; - `POST /extract` → runs OCR, returns raw text

&nbsp; - `POST /extract\_structured` → OCR → structured JSON (vendor/items/payment/raw\_text)

\- \*\*DRY\_RUN\*\* mode (default): returns deterministic mock JSON (no API keys or cost)

\- Real LLM parsing optional (set `DRY\_RUN=0` and add `OPENAI\_API\_KEY`)



---



\## Quickstart



\### 1) Clone and set up

```bash

git clone https://github.com/<your-username>/idp-pipeline.git

cd idp-pipeline

python -m venv .venv

\# Windows PowerShell:

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt



