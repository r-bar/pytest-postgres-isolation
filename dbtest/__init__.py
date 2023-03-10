import os

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_DBURL = "postgresql://postgres:postgres@localhost:5432/postgres"
DBURL = os.environ.get("DBURL", DEFAULT_DBURL)

engine = sa.create_engine(DBURL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r})"


Session = sessionmaker(bind=engine)


def migrate(engine):
    with engine.connect() as conn:
        conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
        try:
            Base.metadata.create_all(engine)
            conn.execute(sa.insert(User).values(name='Foo'))
            conn.execute(sa.insert(User).values(name='Bar'))
            conn.commit()
        except Exception as e:
            print(f"Did not create tables: {e}")


def main(Session=Session):
    db = Session()
    user1 = User(name="Tom")
    user2 = User(name="Dick")
    user3 = User(name="Harry")
    db.add_all([user1, user2, user3])
    db.commit()
    users = db.execute(sa.select(User))
    for user in users:
        print(repr(user))
