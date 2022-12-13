from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import update, delete
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import Base
from utils.db_api.models import Concats, Users

db_string = r"sqlite:///database.db"
db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

Base.metadata.create_all(db)

class Database:
    def reg_user(self, user_id: str, username: str):
        """Some docs"""
        session.merge(Users(user_id = user_id, 
                            username = username))
        session.commit()
    

    def reg_new_concat(self, type: str, file_id: str, wishes: str, bot_name, name = None, age = None, hobbies = None, male = None):
        """Some docs"""
        session.merge(Concats(
            name = name, 
            age = age,
            hobbies = hobbies,
            wishes = wishes,
            type = type,
            file_id = file_id
            )
        )
        session.commit()       
    

    def get_concat_many(self, wishes, bot_name) -> Concats:
        """Some docs"""
        response = session.query(Concats).filter(
            Concats.wishes == wishes,
            Concats.bot_name == bot_name
        ).first()

        return response


    def get_concat_one(self, name, male, age, hobbies, wishes, bot_name) -> Concats:
        """Some docs"""
        response = session.query(Concats).filter(
            Concats.type == 'one',
            Concats.name == name,
            Concats.male == male,
            Concats.age == age,
            Concats.hobbies == hobbies,
            Concats.wishes == wishes,
            Concats.bot_name == bot_name
        ).first()

        return response