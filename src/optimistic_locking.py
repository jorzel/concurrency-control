import logging
import threading
import time

from sqlalchemy import Column, Integer, MetaData, create_engine
from sqlalchemy.orm import configure_mappers, declarative_base, sessionmaker

from config import LOGGER_FORMAT

DB_URI = "postgresql://postgres:postgres@localhost:5432/testdb"
engine = create_engine(DB_URI)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, default=0, nullable=False)
    important_counter = Column(Integer, default=0, nullable=False)

    def __str__(self):
        return f"Example(id={self.id}, important_counter={self.important_counter}, version_id={self.version_id})"

    __repr__ = __str__


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
        stmt = (
            Example.__table__.update()
            .values(
                version_id=example.version_id + 1,
                important_counter=example.important_counter + 1,
            )
            .where(Example.version_id == example.version_id, Example.id == example_id)
        )
        results = session.execute(stmt)
        logger.info(f"{example} instance incremented")
        session.flush()
        session.commit()
        if results.rowcount != 1:
            logger.error(f"Version mismatch for {example_id=}, cannot update")


example_id = add_example(Session)
threading.Thread(target=increment_example, args=[Session, example_id]).start()
threading.Thread(target=increment_example, args=[Session, example_id]).start()

time.sleep(5)
with Session() as session:
    example = session.query(Example).get(example_id)
    logger.info(f"{example} state")

"""
2022-04-04 22:43:49,436 [INFO] Call for increment example_id=1
2022-04-04 22:43:49,437 [INFO] Call for increment example_id=1
2022-04-04 22:43:49,438 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-04 22:43:49,444 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-04 22:43:50,439 [INFO] Example(id=1, important_counter=0, version_id=0) instance incremented
2022-04-04 22:43:50,445 [INFO] Example(id=1, important_counter=0, version_id=0) instance incremented
2022-04-04 22:43:50,454 [ERROR] Version mismatch for example_id=1, cannot update
2022-04-04 22:43:54,443 [INFO] Example(id=1, important_counter=1, version_id=1) state
"""
