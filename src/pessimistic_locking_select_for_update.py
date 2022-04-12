import time

from setup import Example, Session, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
        logger.info(f"Call for increment {example_id=}")
        example = session.query(Example).with_for_update().get(example_id)
        logger.info(f"{example} instance retrieved")
        time.sleep(1)
        logger.info(f"{example} instance incremented")
        example.important_counter += 1
        session.commit()


run_experiment(increment_example, Session)

"""
2022-04-12 11:48:19,157 [INFO] Call for increment example_id=1
2022-04-12 11:48:19,158 [INFO] Call for increment example_id=1
2022-04-12 11:48:19,158 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:48:20,159 [INFO] Example(id=1, important_counter=0, version_id=0) instance incremented
2022-04-12 11:48:20,173 [INFO] Example(id=1, important_counter=1, version_id=0) instance retrieved
2022-04-12 11:48:21,174 [INFO] Example(id=1, important_counter=1, version_id=0) instance incremented
2022-04-12 11:48:24,164 [INFO] Example(id=1, important_counter=2, version_id=0) state
"""
