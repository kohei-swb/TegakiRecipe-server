from fastapi import FastAPI, HTTPException, File, UploadFile, Form, BackgroundTasks
from pathlib import Path
import uuid
import ocr_service
from schemas import Item
from ocr_service import extract_ocr_text
from typing import List
import json
from datetime import datetime,timezone
from json.decoder import JSONDecodeError

app = FastAPI()
items = []
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



@app.get("/")
def root():
    return {"Hello", "World"}
    
@app.post("/jobs/{job_id}")
def upload_recipes(
        background_tasks: BackgroundTasks,
        recipe_name: str = Form(...),
        files: List[UploadFile] = File(...)
    ):
    try:
        # creating directory: recipe id
        # uploads/recipe_id
        recipe_id = f"{uuid.uuid4().hex}"
        recipe_dir_path = Path(UPLOAD_DIR / recipe_id)
        recipe_dir_path.mkdir(exist_ok=True)
        #creating directory: image_dir
        # uploads/recipe_id/image
        image_dir = UPLOAD_DIR / recipe_id / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        # create meta data and save to uploads/recipe_id/meta.json
        meta_json = {
            "recipe_name":recipe_name,
            "created_at":datetime.now(timezone.utc),
            "image_count":len(files)
        }
        meta_path = (UPLOAD_DIR / recipe_id / "meta.json")
        meta_path.write_text(json.dumps(meta_json, ensure_ascii=False))
        
        for file in files:
            try:
                #uploading each files with unique name
                suffix = Path(file.filename).suffix.lower() or ".bin"
                saved_file_name = f"{recipe_id}{suffix}"
                saved_file_path = UPLOAD_DIR / recipe_id / "images" / saved_file_name
                contents = file.file.read()
                saved_file_path.write_bytes(contents)
            except Exception:
                    raise HTTPException(status_code=500, detail="Cannot save file")
            finally:
                file.file.close()
        # adding background task for auto polling
        background_tasks.add_task(extract_ocr_text, Path(UPLOAD_DIR / recipe_id / "images"))
        status = {
            "job_id":recipe_id,
            "status":"pending"
            }
        recipe_dir_path.write_text(json.dumps(status, ensure_ascii=False))
        return status
    except Exception:
        raise HTTPException(status_code=500, detail="Cannot accept files")
    
    
@app.get("/jobs/{job_id}")
def get_result(job_id):
    recipe_path = UPLOAD_DIR / job_id
    if not recipe_path.is_dir():
        raise HTTPException(status_code=404, detail="recipes are not uploaded yet")

    status_path = (recipe_path / "status.json")
    
    if not status_path.exists():
        raise HTTPException(status_code=404, detail="status_json file does not exist")
    
    try:
        status_obj = json.loads(status_path.read_text(encoding="utf-8"))
        if status_obj.get("status") != "done":
            return status_obj
        ingredients_path = (recipe_path / "ingredients.json")
    except JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="status_obj is broken or empty.") from e
    
    if not ingredients_path.exists():
        raise HTTPException(status_code=404, detail="ingredients_json file does not exist")
    
    try:
        result_obj = json.loads(ingredients_path.read_text())
    except JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="ingredients.json is broken") from e
    return result_obj

