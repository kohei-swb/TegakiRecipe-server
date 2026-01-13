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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",  
    "http://127.0.0.1:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


items = []
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



@app.get("/")
def root():
    return {"Hello", "World"}
    
@app.post("/jobs")
async def upload_recipes(
        background_tasks: BackgroundTasks,
        recipe_name: str = Form(...),
        files: List[UploadFile] = File(...)
    ):
 
    # generate unique_id for allowing users to upload multiple recipes of same meal
    recipe_id = f"{uuid.uuid4().hex}"
    recipe_dir_path = Path(UPLOAD_DIR / recipe_id)
    image_dir = UPLOAD_DIR / recipe_id / "images"
    try:
        recipe_dir_path.mkdir(exist_ok=True)
    except OSError as e:
        raise HTTPException(status_code=500, detail="failed to create recipe(job) directory") from e
    #create directory: image_dir | uploads/recipe_id/image
    try:
        image_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise HTTPException(status_code=500, detail="failed to create image directory") from e

    # create meta data and save to uploads/recipe_id/meta.json
    meta_json = {
        "recipe_name":recipe_name,
        "created_at":datetime.now(timezone.utc).isoformat(),
        "image_count":len(files)
    }
    meta_path = (UPLOAD_DIR / recipe_id / "meta.json")
    try:
        meta_path.write_text(json.dumps(meta_json, ensure_ascii=False))
    except OSError as e:
        raise HTTPException(status_code=500, detail="failed to save meta_json") from e
    for i, file in enumerate(files):
            #uploading each files with unique name
            if file.filename is None:
                suffix = ".bin"
            else:
                suffix = Path(file.filename).suffix.lower() or ".bin"
            
            saved_file_name = f"{recipe_id}_{i}{suffix}"
            saved_file_path = UPLOAD_DIR / recipe_id / "images" / saved_file_name
            try:
                contents = await file.read()
            except OSError as e:
                raise HTTPException(status_code=500, detail="Failed to read the image") from e
            try:
                saved_file_path.write_bytes(contents)
            except OSError as e:
                raise HTTPException(status_code=500, detail="Failed to save the image") from e
            await file.close()
    # adding background task for auto polling
    background_tasks.add_task(extract_ocr_text, Path(UPLOAD_DIR / recipe_id), recipe_id)
    status = {
        "job_id":recipe_id,
        "status":"pending"
        }
    try:
        (recipe_dir_path / "status.json").write_text(json.dumps(status, ensure_ascii=False))
    except OSError as e:
        raise HTTPException(status_code=500, detail="Failed to save the status") from e
    return status
    
    
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
        ingredients_path = (recipe_path / "ingredients_result.json")
    except JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="status_obj is broken or empty.") from e
    
    if not ingredients_path.exists():
        raise HTTPException(status_code=404, detail="ingredients_json file does not exist")
    
    try:
        result_obj = json.loads(ingredients_path.read_text())
    except JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="ingredients_result.json is broken") from e
    return result_obj

