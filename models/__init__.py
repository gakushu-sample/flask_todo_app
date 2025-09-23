from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 2.0スタイルの基底クラス
Base = declarative_base()

# データベース設定（必要に応じて環境変数から取得）
DATABASE_URL = "mysql+pymysql://app:app_password@localhost/todo_app"

# エンジンとセッションファクトリーの作成
engine = create_engine(DATABASE_URL, echo=True)
# autocommit=False: セッションで明示的に commit() を呼び出すまでトランザクションを自動でコミットしません。
# autoflush=False: クエリ実行前に自動でセッションの変更内容をデータベースにフラッシュ（反映）しません。
# bind=engine: このセッションが利用するデータベースエンジンを指定します。
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """データベースセッションを取得するコンテキストマネージャー"""
    db = Session()
    try:
        yield db
    finally:
        db.close()
