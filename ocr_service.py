import easyocr
from schemas import Item


def extract_ocr_text(path:str) -> list[Item]:
    reader = easyocr.Reader(['ja']) 
    items = []
    results = reader.readtext('uploads/a84b332b3fe84c0ba94bbe0b3b25842d.png')
    for (bbox, text, prob) in results:
        if prob > 0.1:
            items.append(Item(text=text, conf_rate=prob))
    return items