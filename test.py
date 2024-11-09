import asyncio
import uuid
import json
from data import config
from yookassa import Configuration, Payment


# Configuration.account_id = config.SHOP_ID
# Configuration.secret_key = config.SHOP_API_TOKEN

Configuration.configure(config.SHOP_ID, config.SHOP_API_TOKEN)

# class YooKassa:
    # def __init__(self) -> None:
    #     Configuration.account_id = config.SHOP_ID
    #     Configuration.secret_key = config.SHOP_API_TOKEN

def payment_create(value: float, description: str):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
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
                        "value": 90,
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

async def check_payment(payment_id: str):
    payment = json.loads((Payment.find_one(payment_id)).json())
    while payment['status'] == 'pending':
        payment = json.loads((Payment.find_one(payment_id)).json())
        await asyncio.sleep(3)

    if payment['status']=='succeeded':
        return True


res = payment_create(90, "test")
print(res)
