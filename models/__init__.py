from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 2.0スタイルの基底クラス
Base = declarative_base()

# エンジンとセッションファクトリー（アプリケーションコンテキスト内で初期化）
engine = None
Session = None


def init_db(app):
    """データベースエンジンとセッションファクトリーを初期化"""
    global engine, Session

    database_url = app.config["DATABASE_URL"]
    engine = create_engine(database_url, echo=True)
    # autocommit=False: セッションで明示的に commit() を呼び出すまでトランザクションを自動でコミットしません。
    # autoflush=False: クエリ実行前に自動でセッションの変更内容をデータベースにフラッシュ（反映）しません。
    # bind=engine: このセッションが利用するデータベースエンジンを指定します。
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """データベースセッションを取得するコンテキストマネージャー"""
    if Session is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")

    db = Session()
    try:
        yield db
    finally:
        db.close()
