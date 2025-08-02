import os
from typing import Union
from PIL import Image
import pytesseract

# Optional: if Tesseract isn't on PATH for some users, allow override via env var
TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def ocr_text(img: Union[str, Image.Image], lang: str = "eng") -> str:
    """
    img: file path or PIL.Image
    """
    if isinstance(img, str):
        image = Image.open(img)
    else:
        image = img
    # Basic config: LSTM engine, assume a block of text
    return pytesseract.image_to_string(image, lang=lang, config="--oem 3 --psm 6").strip()
