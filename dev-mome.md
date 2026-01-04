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