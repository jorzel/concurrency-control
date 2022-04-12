import time

from setup import Example, Session, logger, run_experiment


def increment_example(session_cls, example_id):
    with session_cls() as session:
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
        session.flush()
        session.commit()
        if results.rowcount != 1:
            logger.error(f"Version mismatch for {example_id=}, cannot update")
        else:
            logger.info(f"{example} instance incremented")


run_experiment(increment_example, Session)

"""
2022-04-12 11:46:39,896 [INFO] Call for increment example_id=1
2022-04-12 11:46:39,897 [INFO] Call for increment example_id=1
2022-04-12 11:46:39,897 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:46:39,901 [INFO] Example(id=1, important_counter=0, version_id=0) instance retrieved
2022-04-12 11:46:40,913 [INFO] Example(id=1, important_counter=1, version_id=1) instance incremented
2022-04-12 11:46:40,914 [ERROR] Version mismatch for example_id=1, cannot update
2022-04-12 11:46:44,905 [INFO] Example(id=1, important_counter=1, version_id=1) state
"""
