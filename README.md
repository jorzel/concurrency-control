# Concurrency control strategies
In this repo I would like to show 4 strategies of concurrency control for writing data
using Python SQLAlchemy ORM and PostgresSQL (however this examples could be easily transformed to
plain SQL).

## Suprising results
```python
Session = sessionmaker(autoflush=False)

with Session() as session:
    example = Example()
    session.add(example)
    session.commit()
    return example.id


session1 = Session()
example1 = session1.query(Example).get(example.id)
session2 = Session()
example2 = session2.query(Example).get(example.id)

example1.important_counter += 1
session1.commit()
example2.important_counter += 1
session2.commit()
```
What result do you expect?

## Optimistic locking
- additional `version_id` column in a model, object can be updated if only its `version_id` is correct

## Pessimistic locking
- `REPEATABLE READS` isolation level
- `SELECT FOR UPDATE NO WAIT`
- `SELECT FOR UPDATE`