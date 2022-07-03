"""
MODELS.PY

Contains the class architecture of the Point objects, as well as
functions and variables related to database set-up and creation.
"""
from os import path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base


BASE_DIR = path.dirname(path.realpath(__file__))
FILE_BASE = "sqlite:///"
DB_NAME = "tasklist.db"

Base = declarative_base()

def create_database():
    """
    Create database engine.

    Returns:
        file_location (str): Directory location of database file
        engine (Engine): Session engine for queries
    """
    file_name = DB_NAME
    file_location = path.join(FILE_BASE, file_name)
    engine = create_engine(file_location, echo=False)
    try:
        if not path.isfile(file_name):
            Base.metadata.create_all(bind=engine)
            print('Database created!')

    except Exception as e:
        print(f'Error in database management: {e}')

    finally:
        return file_location, engine

class Task(Base):
    """
    Class representation of each data point.

    Parameters:
        id (int): Primary key, identifies individual points
        date (DateTime): Date of recorded point
        active (int): Number of active cases in country
        confirmed (int): Number of confirmed cases (total)
        deaths (int): Number of deaths from COVID-19
    """
    __tablename__ = "tasklist"

    id = Column(Integer(), primary_key=True)
    date = Column(DateTime(), nullable=False)
    user = Column(String(60), nullable=False)
    task = Column(String(150), nullable=False)
    completed = Column(Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'<Point id={self.id} date={self.date}>'

    def __eq__(self, other):
        return self.id == other.id

    def __len__(self):
        return self.active
