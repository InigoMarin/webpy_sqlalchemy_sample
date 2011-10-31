from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///mydatabase.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.username, self.email, self.password)

users_table = User.__table__

metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(engine)
