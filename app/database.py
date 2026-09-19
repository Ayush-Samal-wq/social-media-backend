from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from .config import settings

SQLALCHMEY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
print("HOSTNAME =", settings.database_hostname)
print("DB URL =", SQLALCHMEY_DATABASE_URL)

engine = create_engine(SQLALCHMEY_DATABASE_URL) # we should never hardcore database url cause we are xposing our database password .. when we commit to git hub 

sessionlocal = sessionmaker(autocommit = False , autoflush= False , bind = engine)

Base = declarative_base() #parent class for every model / table.. 


#dependency..
def get_db():
    db = sessionlocal()  # Creates a new database session for the current request.
    try:
        yield db # opens a session to the endpoint 
    finally:
        db.close() # closes the session after request is complete .. 
