import time

from sqlalchemy.exc import OperationalError

from setup import Example, Session, engine, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        try:
            session.add(Example())
            session.commit()
            logger.info(f"{example} new instance inserted")
        except OperationalError:
            logger.error("Insert error")


engine = engine.execution_options(isolation_level="REPEATABLE READ")
Session.configure(bind=engine)
run_experiment(increment_example, Session)


"""
2022-04-12 10:47:24,641 [INFO] Call for increment example_id=1
2022-04-12 10:47:24,642 [INFO] Call for increment example_id=1
2022-04-12 10:47:24,642 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 10:47:24,646 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 10:47:25,657 [INFO] Example(id=1, important_counter=0, version_id=0) new instance inserted
2022-04-12 10:47:25,658 [INFO] Example(id=1, important_counter=0, version_id=0) new instance inserted
"""
