from aiogram import types


def send_contact():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text="Отправить контакт", request_contact=True)
    menu.add(btn1)

    return menu


def main_menu():
    pass
    # menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Объявление")
    # btn2 = types.KeyboardButton("Подробнее")
    # btn3 = types.KeyboardButton("Личный кабинет")
    # menu.add(btn1, btn2)
    # menu.add(btn3)

    # return menu


def cancel():
    pass
    # menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn = types.KeyboardButton("Отмена")
    # menu.add(btn)

    # return menu