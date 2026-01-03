from fastapi import FastAPI, HTTPException, File, UploadFile, Form, BackgroundTasks
from pathlib import Path
import uuid
import ocr_service
from schemas import Item
from ocr_service import extract_ocr_text
from typing import List
import json
from datetime import datetime,timezone

app = FastAPI()
items = []
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {"Hello", "World"}

@app.post("/items")
def create_item(item:Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int=10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
@app.post("/extract_ingredients")
def upload_recipes(
        background_tasks: BackgroundTasks,
        recipe_name: str = Form(...),
        files: List[UploadFile] = File(...)
    ):
    try:
        recipe_id = f"{uuid.uuid4().hex}"
        Path(UPLOAD_DIR / recipe_id).mkdir(exist_ok=True)
        image_dir = UPLOAD_DIR / recipe_id / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        meta_json = {
            "recipe_name":recipe_name,
            "created_at":datetime.now(timezone.utc),
            "image_count":len(files)
        }
        
        meta_path = (UPLOAD_DIR / recipe_id / "meta.json")
        meta_path.write_text(json.dumps(meta_json, ensure_ascii=False))
        
        #saving each files with unique name
        for file in files:
            try:
                suffix = Path(file.filename).suffix.lower() or ".bin"
                saved_file_name = f"{recipe_id}{suffix}"
                saved_file_path = UPLOAD_DIR / recipe_id / "images" / saved_file_name
                contents = file.file.read()
                saved_file_path.write_bytes(contents)
                # return {"message": f"successfully uploaded {file.filename}"}
            except Exception:
                    raise HTTPException(status_code=500, detail="Cannot save file")
            finally:
                file.file.close()
        background_tasks.add_task(extract_ocr_text, Path(UPLOAD_DIR / recipe_id / "images"))
    except Exception:
        raise HTTPException(status_code=500, detail="Cannot accept files")