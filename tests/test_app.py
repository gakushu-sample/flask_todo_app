import json
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


class TestGetTodo(unittest.TestCase):
    """get_todoメソッドのテストクラス"""

    def setUp(self):
        """テスト実行前の準備"""
        # テスト用のデータを登録
        with get_db() as db:
            todo = Todo(task="テストタスク", completion_flg=0)
            db.add(todo)
            db.commit()
            self.todo_id = todo.id

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        # テスト用のデータを削除
        with get_db() as db:
            db.query(Todo).delete()
            db.commit()

    def test_get_todo_success(self):
        """get_todoメソッドの正常系テスト"""
        response = client.get(f"/todos/{self.todo_id}")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["id"], self.todo_id)
        self.assertEqual(data["task"], "テストタスク")
        self.assertEqual(data["completion_flg"], 0)

    def test_get_todo_not_found(self):
        """get_todoメソッドの存在しないIDテスト"""
        response = client.get("/todos/99999")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["message"], "id not found")


class TestCreateTodo(unittest.TestCase):
    """create_todoメソッドのテストクラス"""

    def setUp(self):
        """テスト実行前の準備"""
        # テスト用のデータを登録
        with get_db() as db:
            todo = Todo(task="既存タスク", completion_flg=0)
            db.add(todo)
            db.commit()
            self.existing_todo_id = todo.id

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        # テスト用のデータを削除
        with get_db() as db:
            db.query(Todo).delete()
            db.commit()

    def test_create_todo_success(self):
        """create_todoメソッドの新規作成テスト"""
        data = {"task": "新しいタスク", "completion_flg": 0}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        response_data = response.get_json()
        self.assertEqual(response_data["code"], 200)
        self.assertEqual(response_data["message"], "ok")

        # データベースに保存されているか確認
        with get_db() as db:
            todos = db.query(Todo).filter(Todo.task == "新しいタスク").all()
            self.assertEqual(len(todos), 1)
            self.assertEqual(todos[0].completion_flg, 0)

    def test_create_todo_without_completion_flg(self):
        """create_todoメソッドのcompletion_flgなしテスト"""
        data = {"task": "デフォルトタスク"}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # データベースに保存されているか確認（デフォルト値0）
        with get_db() as db:
            todos = db.query(Todo).filter(Todo.task == "デフォルトタスク").all()
            self.assertEqual(len(todos), 1)
            self.assertEqual(todos[0].completion_flg, 0)

    def test_update_todo_success(self):
        """create_todoメソッドの更新テスト"""
        data = {"id": self.existing_todo_id, "task": "更新されたタスク", "completion_flg": 1}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        response_data = response.get_json()
        self.assertEqual(response_data["code"], 200)
        self.assertEqual(response_data["message"], "ok")

        # データベースの更新確認
        with get_db() as db:
            todo = db.query(Todo).filter(Todo.id == self.existing_todo_id).first()
            self.assertEqual(todo.task, "更新されたタスク")
            self.assertEqual(todo.completion_flg, 1)

    def test_update_todo_without_completion_flg(self):
        """create_todoメソッドのcompletion_flgなし更新テスト"""
        data = {"id": self.existing_todo_id, "task": "タスクのみ更新"}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # データベースの更新確認（completion_flgは変更されない）
        with get_db() as db:
            todo = db.query(Todo).filter(Todo.id == self.existing_todo_id).first()
            self.assertEqual(todo.task, "タスクのみ更新")
            self.assertEqual(todo.completion_flg, 0)  # 元の値のまま

    def test_create_todo_invalid_request(self):
        """create_todoメソッドの無効なリクエストテスト"""
        response = client.post("/todos", data="invalid json", content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 400)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["message"], "invalid request")

    def test_create_todo_missing_task(self):
        """create_todoメソッドのtaskなしテスト"""
        data = {"completion_flg": 0}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 400)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["message"], "task is required")

    def test_update_todo_not_found(self):
        """create_todoメソッドの存在しないID更新テスト"""
        data = {"id": 99999, "task": "存在しないタスク", "completion_flg": 0}
        response = client.post("/todos", data=json.dumps(data), content_type="application/json")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["message"], "id not found")


class TestDeleteTodo(unittest.TestCase):
    """delete_todoメソッドのテストクラス"""

    def setUp(self):
        """テスト実行前の準備"""
        # テスト用のデータを登録
        with get_db() as db:
            todo = Todo(task="削除対象タスク", completion_flg=0)
            db.add(todo)
            db.commit()
            self.todo_id = todo.id

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        # テスト用のデータを削除
        with get_db() as db:
            db.query(Todo).delete()
            db.commit()

    def test_delete_todo_success(self):
        """delete_todoメソッドの正常系テスト"""
        response = client.delete(f"/todos/{self.todo_id}")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["code"], 200)
        self.assertEqual(data["message"], "ok")

        # データベースから削除されているか確認
        with get_db() as db:
            todo = db.query(Todo).filter(Todo.id == self.todo_id).first()
            self.assertIsNone(todo)

    def test_delete_todo_not_found(self):
        """delete_todoメソッドの存在しないIDテスト"""
        response = client.delete("/todos/99999")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)

        # レスポンスデータの確認
        data = response.get_json()
        self.assertEqual(data["message"], "id not found")


class TestRoutes(unittest.TestCase):
    """ルートのテストクラス"""

    def test_index_route(self):
        """indexルートのテスト"""
        response = client.get("/")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # HTMLが返されることを確認
        self.assertIn("text/html", response.content_type)

    def test_demo_route(self):
        """demoルートのテスト"""
        response = client.get("/demo")

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # HTMLが返されることを確認
        self.assertIn("text/html", response.content_type)


if __name__ == "__main__":
    unittest.main()
