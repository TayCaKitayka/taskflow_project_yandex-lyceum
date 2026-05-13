import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()
factory = None


def global_init(db_file):
    global factory

    if factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    connection_string = f"sqlite:///{db_file.strip()}"
    engine = sa.create_engine(connection_string, echo=False)

    factory = orm.sessionmaker(bind=engine)

    from data import users, projects, tasks, attachments

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global factory
    return factory()
