import time

from sqlalchemy.exc import OperationalError

from setup import Example, Session, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        try:
            example = (
                session.query(Example).with_for_update(nowait=True).get(example_id)
            )
            logger.info(f"{example} instance retrieved")
            time.sleep(1)
            example.important_counter += 1
            logger.info(f"{example} instance incremented")
            session.commit()
        except OperationalError:
            logger.error("Row is locked, cannot fetch record")


run_experiment(increment_example, Session)

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
