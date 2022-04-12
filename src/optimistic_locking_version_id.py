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
        logger.info(f"{example} instance incremented")
        if results.rowcount != 1:
            logger.error(f"Version mismatch for {example_id=}, cannot update")


run_experiment(increment_example, Session)

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
