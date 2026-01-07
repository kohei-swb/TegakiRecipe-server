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
これのTry exceptを実装する

実行してエラーが出たら直す

1/6
動いてるけど、ingredients_resultのTextから具材を取り出さないと意味がない
辞書　OR 形態素解析 → 辞書照合
でもあとiosのUIも作らないといけないし、、、って考えると辞書照合だけで今はいい気がする
辞書照合　で行く

TODO: 
iOSのUI