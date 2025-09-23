from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT

from . import Base


class Todo(Base):
    """todosテーブルのモデルクラス"""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String(100), nullable=False)
    completion_flg = Column(TINYINT(unsigned=True), nullable=False, default=0)

    def __repr__(self):
        return f"<Todo(id={self.id}, task='{self.task}', completion_flg={self.completion_flg})>"
