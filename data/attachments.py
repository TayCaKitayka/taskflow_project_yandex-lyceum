import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.db_session import SqlAlchemyBase


class Attachment(SqlAlchemyBase):
    __tablename__ = "attachments"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    filename = sa.Column(sa.String, nullable=False)
    file_path = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now)
    task_id = sa.Column(sa.Integer, sa.ForeignKey("tasks.id"), nullable=False)

    task = orm.relationship("Task", back_populates="attachments")
