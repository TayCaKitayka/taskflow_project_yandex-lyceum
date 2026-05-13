import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, index=True, unique=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now)

    projects = orm.relationship("Project", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
