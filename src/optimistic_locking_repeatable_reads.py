import time

from sqlalchemy.exc import OperationalError

from setup import Example, Session, engine, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        example.important_counter += 1
        try:
            session.commit()
            logger.info(f"{example} instance incremented")
        except OperationalError:
            logger.error("Concurrent update error")


engine = engine.execution_options(isolation_level="REPEATABLE READ")
Session.configure(bind=engine)
run_experiment(increment_example, Session)


"""
2022-04-12 11:47:28,485 [INFO] Call for increment example_id=1
2022-04-12 11:47:28,486 [INFO] Call for increment example_id=1
2022-04-12 11:47:28,486 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:47:28,490 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:47:29,502 [ERROR] Concurrent update error
2022-04-12 11:47:29,504 [INFO] Example(id=1, important_counter=1, version_id=0) instance incremented
2022-04-12 11:47:33,493 [INFO] Example(id=1, important_counter=1, version_id=0) state
"""
