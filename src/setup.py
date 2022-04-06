import logging
import threading
import time

from sqlalchemy import Column, Integer, MetaData, create_engine
from sqlalchemy.orm import configure_mappers, declarative_base, sessionmaker

# logging config
LOGGER_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(format=LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# db config
DB_URI = "postgresql://postgres:postgres@localhost:5432/testdb"
engine = create_engine(DB_URI)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, autoincrement=True)
    important_counter = Column(Integer, default=0, nullable=False)
    version_id = Column(Integer, default=0, nullable=False)

    def __str__(self):
        return f"Example(id={self.id}, important_counter={self.important_counter}, version_id={self.version_id})"

    __repr__ = __str__


configure_mappers()
metadata.drop_all(engine)
metadata.create_all(engine)

Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)


def add_example(session_cls) -> int:
    with session_cls() as session:
        example = Example()
        session.add(example)
        session.commit()
        return example.id


def run_experiment(func, session_cls):
    example_id = add_example(session_cls)
    threading.Thread(target=func, args=[session_cls, example_id]).start()
    threading.Thread(target=func, args=[session_cls, example_id]).start()

    time.sleep(5)
    with session_cls() as session:
        example = session.query(Example).get(example_id)
        logger.info(f"{example} state")
