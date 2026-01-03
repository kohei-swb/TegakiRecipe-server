from pathlib import Path
from schemas import Item
import easyocr
reader = easyocr.Reader(['ja']) 


def extract_ocr_text(dir_path:Path) -> list[Item]:
    files = list(dir_path.glob("*"))
    items = []
    for file in files:
        results = reader.readtext(str(file))
        for (bbox, text, prob) in results:
            if prob > 0.1:
                items.append(Item(text=text, conf_rate=prob))
    return items