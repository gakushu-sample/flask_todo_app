from flask import Flask, jsonify, render_template, request

from models import get_db
from models.todos import Todo

app = Flask(__name__)
app.json.ensure_ascii = False  # type: ignore


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    return render_template("todo.html")


@app.route("/todos", methods=["GET"])
def get_todos():
    """すべての TODO を取得."""
    with get_db() as db:
        todos = db.query(Todo).all()
        return jsonify([{"id": todo.id, "task": todo.task, "completion_flg": todo.completion_flg} for todo in todos])


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """TODO を単一取得.

    Args:
        todo_id: TODO の ID.

    Returns:
        TODO の情報.
    """
    with get_db() as db:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return jsonify({"message": "id not found"}), 404
        return jsonify({"id": todo.id, "task": todo.task, "completion_flg": todo.completion_flg})


@app.route("/todos", methods=["POST"])
def create_todo():
    """TODO を作成若しくは更新."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "invalid request"}), 400
    if "task" not in data:
        return jsonify({"message": "task is required"}), 400
    with get_db() as db:
        if "id" in data:
            todo = db.query(Todo).filter(Todo.id == data["id"]).first()
            if not todo:
                return jsonify({"message": "id not found"}), 404
            todo.task = data["task"]
            if "completion_flg" in data:
                todo.completion_flg = data["completion_flg"]
        else:
            todo = Todo(task=data["task"], completion_flg=data.get("completion_flg", 0))
            db.add(todo)
        db.commit()
        return jsonify({"code": 200, "message": "ok"})


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """TODO を削除.

    Args:
        todo_id: TODO の ID.

    Returns:
        TODO の情報.
    """
    with get_db() as db:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return jsonify({"message": "id not found"}), 404
        db.delete(todo)
        db.commit()
        return jsonify({"code": 200, "message": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
