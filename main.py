from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pathlib import Path
import uuid
from schemas import Item

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
    
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        suffix = Path(file.filename).suffix.lower() or ".bin"
        safe_name = f"{uuid.uuid4().hex}{suffix}"
        save_path = UPLOAD_DIR / safe_name
        contents = file.file.read()
        save_path.write_bytes(contents)
        return {"message": f"successfully uploaded {file.filename}"}
    except Exception:
            raise HTTPException(status_code=500, detail="Someting went wrong")
    finally:
        file.file.close()
    