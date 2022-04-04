import logging
import threading
import time

from sqlalchemy import Column, Integer, MetaData, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import configure_mappers, declarative_base, sessionmaker

from config import LOGGER_FORMAT

DB_URI = "postgresql://postgres:postgres@localhost:5432/testdb"
engine = create_engine(DB_URI, isolation_level="REPEATABLE READ")
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, autoincrement=True)
    important_counter = Column(Integer, default=0, nullable=False)

    def __str__(self):
        return f"Example(id={self.id}, important_counter={self.important_counter})"


configure_mappers()

metadata.drop_all(engine)
metadata.create_all(engine)
Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)

logging.basicConfig(format=LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def add_example(Session) -> int:
    with Session() as session:
        example = Example()
        session.add(example)
        session.commit()
        return example.id


def increment_example(Session, example_id):
    with Session() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        example.important_counter += 1
        logger.info(f"{example} instance incremented")
        try:
            session.commit()
        except OperationalError:
            logger.error("Concurrent update error")


with Session() as session:
    example = Example()
    session.add(example)
    session.commit()
    example_id = example.id

example_id = add_example(Session)
threading.Thread(target=increment_example, args=[Session, example_id]).start()
threading.Thread(target=increment_example, args=[Session, example_id]).start()

time.sleep(5)
with Session() as session:
    example = session.query(Example).get(example_id)
    logger.info(f"{example} state")

"""
2022-04-04 22:44:28,142 [INFO] Call for increment example_id=2
2022-04-04 22:44:28,143 [INFO] Call for increment example_id=2
2022-04-04 22:44:28,143 [INFO] Example(id=2, important_counter=0) instance retrieved
2022-04-04 22:44:28,147 [INFO] Example(id=2, important_counter=0) instance retrieved
2022-04-04 22:44:29,144 [INFO] Example(id=2, important_counter=1) instance incremented
2022-04-04 22:44:29,148 [INFO] Example(id=2, important_counter=1) instance incremented
2022-04-04 22:44:29,151 [ERROR] Concurrent update error
2022-04-04 22:44:33,152 [INFO] Example(id=2, important_counter=1) state
"""
