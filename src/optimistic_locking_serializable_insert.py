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


engine = engine.execution_options(isolation_level="SERIALIZABLE")
Session.configure(bind=engine)
run_experiment(increment_example, Session)


"""
2022-04-12 10:46:32,171 [INFO] Call for increment example_id=1
2022-04-12 10:46:32,172 [INFO] Call for increment example_id=1
2022-04-12 10:46:32,172 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 10:46:32,176 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 10:46:33,178 [ERROR] Insert error
2022-04-12 10:46:33,181 [INFO] Example(id=1, important_counter=0, version_id=0) new instance inserted
"""
