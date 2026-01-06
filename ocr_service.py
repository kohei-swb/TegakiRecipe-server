from pathlib import Path

from fastapi import HTTPException
from schemas import Ingredient, Item
import easyocr
import json
from pydantic import RootModel
reader = easyocr.Reader(['ja']) 

# dir_path = /uploads/recipe_id(job_id)/
def extract_ocr_text(dir_path:Path, recipe_id):
    if len(recipe_id) == 0:
        raise ValueError("recipe_id is empty")
    if not dir_path.exists():
        raise FileNotFoundError(f"recipe directory of {recipe_id} does not exist")
    
    images_path = dir_path / "images"
    
    if not images_path.exists():
        raise FileNotFoundError(f"images directory of {recipe_id} deoes not exist")
    
    files = list(images_path.glob("*"))
    
    if len(files) == 0:
        raise FileNotFoundError(f"images of {recipe_id} is not included")
    
    Ingredients = RootModel[list[Ingredient]]
    ingredients = Ingredients([])
    for file in files:
        try:
            results = reader.readtext(str(file))
        except RuntimeError as e:
            raise RuntimeError(f"image file is empty in recipe_id:{recipe_id}") from e
        for (bbox, text, prob) in results:
            if prob > 0.1:
                # items.append(Ingredient(text=text, conf_rate=prob))
                ingredients.root.append(Ingredient(text=text, conf_rate=prob))
    ingredients_result = ingredients.model_dump_json(indent=2)
    try:
        (dir_path / "ingredients_result.json").write_text(ingredients_result)
    except OSError as e:
        raise OSError(f"cannot write to ingredients_result.json in recipe_id{recipe_id}") from e
    # update status
    status = {
            "job_id":recipe_id,
            "status":"done"
            }
    try:
        (dir_path / "status.json").write_text(json.dumps(status, ensure_ascii=False))
    except OSError as e:
        raise OSError(f"cannot write to status.json in recipe_id:f{recipe_id}") from e
    return ingredients_result