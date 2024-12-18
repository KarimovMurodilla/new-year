# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from utils.db_api.models import Promocodes
# from promos import codes

# # Define the database URL
# DATABASE_URL = "sqlite:///database.db"  # You can replace this with your database URL

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

# # Create a configured "Session" class
# Session = sessionmaker(bind=engine)

# # Create a Session
# session = Session()

# for code in codes:
#     promo = Promocodes(code = code)
#     session.add(promo)

# # Commit the transaction
# session.commit()

# # Close the session
# session.close()


import asyncio
from pprint import pprint
import uuid
import json
from data import config
from yookassa import Configuration, Payment


class YooKassa:
    def __init__(self) -> None:
        Configuration.account_id = config.SHOP_ID
        Configuration.secret_key = config.SHOP_API_TOKEN

    def payment_create(self, value: float, description: str):
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "sbp"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/MorozruBot"
            },
            "receipt": {
                "customer": {
                    "full_name": "Ivanov Ivan Ivanovich",
                    "email": "email@email.ru",
                    "phone": "79211234567",
                    "inn": "6321341814"
                },
                "items": [
                    {
                        "description": "Переносное зарядное устройство Хувей",
                        "quantity": "1.00",
                        "amount": {
                            "value": value,
                            "currency": "RUB"
                        },
                        "vat_code": "2",
                        "payment_mode": "full_payment",
                        "payment_subject": "commodity",
                        "country_of_origin_code": "CN",
                        "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                        "customs_declaration_number": "10714040/140917/0090376",
                        "excise": "20.00",
                        "supplier": {
                            "name": "string",
                            "phone": "string",
                            "inn": "string"
                        }
                    },
                ]
            },
            "capture": True,
            "description": description
        }, idempotence_key)

        return json.loads(payment.json())

    def check_payment(self, payment_id: str):
        payment = json.loads((Payment.find_one(payment_id)).json())
        print("payment status:", payment['status'])
        print(payment)
        # while payment['status'] == 'pending':
        #     print("Payment status inside while loop:", payment['status'])
        #     payment = json.loads((Payment.find_one(payment_id)).json())
        #     # await asyncio.sleep(3)

        # if payment['status']=='succeeded':
        #     return True


kassa = YooKassa()
# res = kassa.payment_create(1, "test")
res = kassa.check_payment("2ec4f427-000f-5000-8000-17138f180427")
pprint(res)


"""
Александр	Саша	
Алексей	Лёша	
Анатолий	Толя	Толик
Аркадий	Аркаша	
Артём	Тёма	
Борис	Боря	
Вадим	Вадя	Вадик
Валентин	Валя	
Валерий	Валера	
Василий	Вася	
Вениамин	Веня	
Виктор	Витя	
Виталий	Виталик	
Владимир	Вова	Володя
Владислав	Влад	Владик
Вячеслав	Слава	
Геннадий	Гена	
Георгий	Жорик	
Григорий	Гриша	
Дмитрий	Дима	
Евгений	Женя	
Иван	Ваня	
Константин	Костя	
Леонид	Леня	
Михаил	Миша	
Николай	Коля	
Павел	Паша	
Пётр	Петр	Петя
Родион	Родя	
Роман	Рома	
Семён	Сёма	Сема
Сергей	Серёжа	Сережа
Станислав	Стас	Сиасик
Фёдор	Федя	
Филипп	Филя	
Эдуард	Эдик	
Юрий	Юра	
Ярослав	Ярик

"""


