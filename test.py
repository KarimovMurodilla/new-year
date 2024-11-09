from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils.db_api.models import Promocodes
from promos import codes

# Define the database URL
DATABASE_URL = "sqlite:///database.db"  # You can replace this with your database URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

for code in codes:
    promo = Promocodes(code = code)
    session.add(promo)

# Commit the transaction
session.commit()

# Close the session
session.close()

