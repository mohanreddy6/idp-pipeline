import os
from flask import Flask, request, jsonify
from PIL import Image
import io, base64

from src.ocr.ocr import ocr_text
from src.llm.extract import extract_structured

app = Flask(__name__, static_folder="static", static_url_path="/static")
from flask import send_from_directory

@app.get("/")
def home():
    # Serve /src/app/static/index.html
    return send_from_directory(app.static_folder, "index.html")

@app.get("/")
def home():
    # Serve the demo page from /src/app/static/index.html
    return send_from_directory(app.static_folder, "index.html")


@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/extract')
def extract():
    # multipart upload
    if request.content_type and 'multipart/form-data' in request.content_type:
        f = request.files.get('file')
        if not f:
            return jsonify({'error': 'file missing'}), 400
        img = Image.open(f.stream)
        text = ocr_text(img)
        return jsonify({'text': text})

    data = request.get_json(silent=True) or {}
    if 'text' in data:
        return jsonify({'text': data['text']})
    if 'image_b64' in data:
        try:
            img_bytes = base64.b64decode(data['image_b64'])
            img = Image.open(io.BytesIO(img_bytes))
            text = ocr_text(img)
            return jsonify({'text': text})
        except Exception as e:
            return jsonify({'error': f'invalid image_b64: {e}'}), 400

    return jsonify({'error': "provide 'file' (multipart) or 'image_b64' or 'text'"}), 400

@app.post('/extract_structured')
def extract_structured_api():
    # multipart upload
    if request.content_type and 'multipart/form-data' in request.content_type:
        f = request.files.get('file')
        if not f:
            return jsonify({'error': 'file missing'}), 400
        img = Image.open(f.stream)
        text = ocr_text(img)
        result = extract_structured(text)
        return jsonify(result.model_dump())

    data = request.get_json(silent=True) or {}
    if 'text' in data:
        result = extract_structured(data['text'])
        return jsonify(result.model_dump())
    if 'image_b64' in data:
        try:
            img_bytes = base64.b64decode(data['image_b64'])
            img = Image.open(io.BytesIO(img_bytes))
            text = ocr_text(img)
            result = extract_structured(text)
            return jsonify(result.model_dump())
        except Exception as e:
            return jsonify({'error': f'invalid image_b64: {e}'}), 400

    return jsonify({'error': "provide 'file' (multipart) or 'image_b64' or 'text'"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
