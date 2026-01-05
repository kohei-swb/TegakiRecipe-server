APIは1本

POST /extract_ingredients
multipartで送る
recipe_name は Form
images は files 複数

返す
recipe_id
recipe_name
ingredients

サーバー側の保存はこう

保存先は日本語名のフォルダじゃなくて uuid。

debug または uploads
recipe_id
meta.json ここに recipe_name と日時
images ここにアップロード画像
ocr.txt OCR結果
ingredients.json 抽出結果

Backgroundtasksを使う

concurrent.futures.ProcessPoolExecutor() and asyncio to manage long running jobs.
BackgroundTaskはよくなさそうだから上の方法かCeleryを使って管理した方がいいかも
https://medium.com/@hitorunajp/celery-and-background-tasks-aebb234cae5d


async def upload_recipes(
これのTry exceptを改善する

エラーが出てるけど
INFO:     127.0.0.1:63423 - "POST /jobs/%7Bjob_id%7D HTTP/1.1" 500 Internal Server Error
だから原因追及をする

def extract_ocr_text(dir_path:Path) -> list[Item]:
    # return ingredients.json
    # need to update uploads/recipe_id(job_id)/status.json
これもする