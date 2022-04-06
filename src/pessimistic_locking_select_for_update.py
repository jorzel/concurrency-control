import time

from setup import Example, Session, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).with_for_update().get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        example.important_counter += 1
        logger.info(f"{example} instance incremented")
        session.commit()


run_experiment(increment_example, Session)

"""
2022-04-04 22:45:44,541 [INFO] Call for increment example_id=1
2022-04-04 22:45:44,544 [INFO] Call for increment example_id=1
2022-04-04 22:45:44,545 [INFO] Example(id=1, important_counter=0) instance retrieved
2022-04-04 22:45:45,547 [INFO] Example(id=1, important_counter=1) instance incremented
2022-04-04 22:45:45,549 [INFO] Example(id=1, important_counter=1) instance retrieved
2022-04-04 22:45:46,551 [INFO] Example(id=1, important_counter=2) instance incremented
2022-04-04 22:45:49,552 [INFO] Example(id=1, important_counter=2) state
"""
