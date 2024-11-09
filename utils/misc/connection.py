from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import update, delete, func
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import Base
from utils.db_api.models import Concats, Users, Promocodes

db_string = r"sqlite:///database.db"
db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

Base.metadata.create_all(db)


class Database:
    # ---Users---
    def reg_user(
        self, 
        user_id: str,
        username: str,
        phone_number: str
    ):
        """Some docs"""
        session.merge(
            Users(
                user_id = user_id, 
                username = username,
                phone_number = phone_number
            )
        )
        session.commit()
    

    # All concat
    def reg_new_concat(
        self, 
        user_id: int, 
        type: str, 
        wishes: str, 
        bot_name: str, 
        file_id: str, 
        name = None, 
        age = None, 
        hobbies = None, 
        gender = None
    ):
        """Some docs"""
        session.merge(Concats(
                user_id = user_id,
                name = name,
                age = age,
                hobbies = hobbies,
                wishes = wishes,
                type = type,
                file_id = file_id,
                bot_name = bot_name,
                gender = gender
            )
        )
        session.commit()       
    

    # ---Many child---
    def get_concat_many(self, wishes, bot_name) -> Concats:
        """Some docs"""
        response = session.query(Concats).filter(
            Concats.type == 'many',
            Concats.wishes == wishes,
            Concats.bot_name == bot_name
        ).first()

        return response


    # ---One child---
    def update_video_file_id(self, user_id, file_id):
        """Some changes"""
        session.execute(
                update(Concats).filter(Concats.user_id == user_id).
                values(file_id = file_id)
        )
        session.commit()



    def get_concat_one(self, name, gender, age, hobbies, wishes, bot_name) -> Concats:
        """Some docs"""
        response = session.query(Concats).filter(
            Concats.type == 'one',
            Concats.name == name,
            Concats.gender == gender,
            Concats.age == age,
            Concats.hobbies == hobbies,
            Concats.wishes == wishes,
            Concats.bot_name == bot_name
        ).first()

        return response


    def get_concat_one_by_id(self, user_id) -> Concats:
        """Some docs"""
        response = session.query(Concats).filter(
            Concats.user_id == user_id
        ).first()

        return response

    def get_promocode_status(self, code) -> Promocodes:
        """Some docs"""
        response = session.query(Promocodes).filter(
            func.lower(Promocodes.code) == func.lower(code),
        ).first()

        return response 

    def update_promo_to_expired(self, code, user_id):
        """Some changes"""
        session.execute(
                update(Promocodes).filter(Promocodes.code == code).
                values(status = True, user_id=user_id)
        )
        session.commit()
