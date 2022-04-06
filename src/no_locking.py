import time

from setup import Example, Session, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        example.important_counter += 1
        logger.info(f"{example} instance incremented")
        session.commit()


run_experiment(increment_example, Session)

"""
2022-04-04 22:42:45,889 [INFO] Call for increment example_id=1
2022-04-04 22:42:45,890 [INFO] Call for increment example_id=1
2022-04-04 22:42:45,890 [INFO] Example(id=1, important_counter=0) instance retrieved
2022-04-04 22:42:45,894 [INFO] Example(id=1, important_counter=0) instance retrieved
2022-04-04 22:42:46,892 [INFO] Example(id=1, important_counter=1) instance incremented
2022-04-04 22:42:46,896 [INFO] Example(id=1, important_counter=1) instance incremented
2022-04-04 22:42:50,899 [INFO] Example(id=1, important_counter=1) state
"""
