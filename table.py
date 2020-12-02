from sqlalchemy import Integer, Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# catalog for the ORM model
Base = declarative_base()


# ORM table model
class unpopulation(Base):
    __tablename__ = 'population'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    code = Column(Integer)
    year = Column(Integer)
    population = Column(Float)
    group = Column(String)

    def __repr__(self):
        return f"<unpopulation(id={self.id},\
                    country={self.country},\
                    country_code={self.code},\
                    year={self.year},\
                    population={self.population},\
                    group={self.group})>"


# creates a new engine instance using postgres
engine = create_engine(
    'postgres://chris:chris@localhost:5432/sqlp', echo=True)

Base.metadata.create_all(engine)

# creating session object and binding to engine
Session = sessionmaker(bind=engine)
session = Session()
