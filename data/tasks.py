import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = "tasks"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    status = sa.Column(sa.String, default="Новая")
    priority = sa.Column(sa.String, default="Средний")
    deadline = sa.Column(sa.Date, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now)
    project_id = sa.Column(sa.Integer, sa.ForeignKey("projects.id"), nullable=False)

    project = orm.relationship("Project", back_populates="tasks")
    attachments = orm.relationship(
        "Attachment",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        deadline_value = None

        if self.deadline:
            deadline_value = self.deadline.isoformat()

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "deadline": deadline_value,
            "project_id": self.project_id,
        }
