import unittest

from models import get_db
from models.todos import Todo
from tests.conftest import client


class TestGetTodos(unittest.TestCase):
    """get_todosメソッドのテストクラス"""

    def setUp(self):
        """テスト実行前の準備"""
        # テスト用のデータを登録
        with get_db() as db:
            # テスト用のTODOデータを作成
            todo1 = Todo(task="テストタスク1", completion_flg=0)
            todo2 = Todo(task="テストタスク2", completion_flg=1)
            todo3 = Todo(task="テストタスク3", completion_flg=0)

            db.add(todo1)
            db.add(todo2)
            db.add(todo3)
            db.commit()

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        # テスト用のデータを削除
        with get_db() as db:
            db.query(Todo).delete()
            db.commit()

    def test_get_todos_success(self):
        """get_todosメソッドの正常系テスト"""
        response = client.get("/todos")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

        # 各TODOの内容確認
        tasks = [todo["task"] for todo in data]
        self.assertIn("テストタスク1", tasks)
        self.assertIn("テストタスク2", tasks)
        self.assertIn("テストタスク3", tasks)

        # 完了フラグの確認
        completion_flags = [todo["completion_flg"] for todo in data]
        self.assertIn(0, completion_flags)
        self.assertIn(1, completion_flags)

    def test_get_todos_empty(self):
        """get_todosメソッドの空データテスト"""
        # データをクリア
        with get_db() as db:
            db.query(Todo).delete()
            db.commit()

        response = client.get("/todos")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main()
