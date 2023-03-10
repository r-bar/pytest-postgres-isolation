import string
import random

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, close_all_sessions


@pytest.fixture(scope="session")
def template():
    from dbtest import engine, migrate
    template_database = 'dbtest_template'
    with engine.connect() as conn:
        template_exists = conn.execute(
            sa.text("select true from pg_database where datname = :datname ;")
            .bindparams(datname=template_database)
        ).scalar()
    if template_exists:
        return template_database
    url = engine.url._replace(database=template_database)
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(sa.text(f'CREATE DATABASE {template_database};'))
        tengine = sa.create_engine(url.render_as_string(False))
        migrate(tengine)
        tengine.dispose()
        del tengine
    except Exception as e:
        print(f"migration failed: {e}")
    return template_database


@pytest.fixture
def engine(template):
    from dbtest import engine
    dbname = "".join(random.choice(string.ascii_lowercase) for _ in range(7))
    url = engine.url._replace(database=dbname)
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(sa.text(
            f'CREATE DATABASE {dbname} WITH TEMPLATE {template};'
        ))

    new_engine = sa.create_engine(url.render_as_string(False))
    yield new_engine
    new_engine.dispose()
    del new_engine

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(sa.text(f'DROP DATABASE {dbname};'))


@pytest.fixture
def session(engine):
    s = sessionmaker(bind=engine)
    yield s
    close_all_sessions()
    del s


@pytest.mark.parametrize("i", range(10))
def test_main(i, session):
    from dbtest import main, User
    main(session)
    user_count = session().execute(sa.select(sa.func.count(User.id))).scalar()
    assert user_count == 5
