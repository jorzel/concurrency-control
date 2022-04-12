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
            session.commit()
            logger.info(f"{example} instance incremented")
        except OperationalError:
            logger.error("Row is locked, cannot fetch record")


run_experiment(increment_example, Session)

"""
2022-04-12 11:48:42,676 [INFO] Call for increment example_id=1
2022-04-12 11:48:42,677 [INFO] Call for increment example_id=1
2022-04-12 11:48:42,678 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:48:42,681 [ERROR] Row is locked, cannot fetch record
2022-04-12 11:48:43,693 [INFO] Example(id=1, important_counter=1, version_id=0) instance incremented
2022-04-12 11:48:47,684 [INFO] Example(id=1, important_counter=1, version_id=0) state
"""
