import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.db_session import SqlAlchemyBase


class Project(SqlAlchemyBase):
    __tablename__ = "projects"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)

    user = orm.relationship("User", back_populates="projects")
    tasks = orm.relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )
