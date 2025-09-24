from app import TestConfig, app

from models import init_db

# テスト用のFlaskアプリケーションを設定
app.config.from_object(TestConfig)
init_db(app)

# テストクライアントを作成
client = app.test_client()
