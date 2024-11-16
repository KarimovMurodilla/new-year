from aiogram import types


def create_congrats():
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="СОЗДАТЬ ПОЗДРАВЛЕНИЕ", callback_data="create")
    btn2 = types.InlineKeyboardButton(text="Политика конфиденциальности", url="https://telegra.ph/Vot-tak-11-09")
    menu.add(btn1, btn2)

    return menu


def choose_type():
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="ОДНОГО РЕБЁНКА", callback_data="one_child")
    btn2 = types.InlineKeyboardButton(text="КОМПАНИЮ ДЕТЕЙ", callback_data="many_child")
    menu.add(btn1, btn2)

    return menu


def choose_hobbies():
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="ЧИТАТЬ", callback_data="read")
    btn2 = types.InlineKeyboardButton(text="РИСОВАТЬ", callback_data="paint")
    btn3 = types.InlineKeyboardButton(text="ГУЛЯТЬ", callback_data="walk")
    btn4 = types.InlineKeyboardButton(text="ЗАНИМАТЬСЯ СПОРТОМ", callback_data="do_sport")
    btn5 = types.InlineKeyboardButton(text="СМОТРЕТЬ МУЛЬТИКИ", callback_data="watch_cartoons")
    btn6 = types.InlineKeyboardButton(text="ЕСТЬ СЛАДОСТИ", callback_data="eat_sweets")
    btn7 = types.InlineKeyboardButton(text="ПЕТЬ", callback_data="sing")
    btn8 = types.InlineKeyboardButton(text="ЗАНИМАТЬСЯ МУЗЫКОЙ", callback_data="play_music")
    btn9 = types.InlineKeyboardButton(text="ИГРАТЬ В ИГРЫ", callback_data="play_games")
    btn10 = types.InlineKeyboardButton(text="ТАНЦЕВАТЬ", callback_data="dance")
    menu.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)

    return menu


def choose_wishes():
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="СЛУШАТЬСЯ РОДИТЕЛЕЙ", callback_data="obey_parents")
    btn2 = types.InlineKeyboardButton(text="ХОРОШО КУШАТЬ", callback_data="good_to_eat")
    btn3 = types.InlineKeyboardButton(text="ХОРОШО УЧИТЬСЯ", callback_data="study_well")
    btn4 = types.InlineKeyboardButton(text="НАЙТИ НОВЫХ ДРУЗЕЙ", callback_data="find_new_friends")
    btn5 = types.InlineKeyboardButton(text="ЧИТАТЬ БОЛЬШЕ КНИГ", callback_data="read_more_books")
    menu.add(btn1, btn2, btn3, btn4, btn5)

    return menu


def get_congrats():
    menu = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="ПОЛУЧИТЬ ПОЗДРАВЛЕНИЕ", callback_data="send_congrats")
    menu.add(btn1)

    return menu


def m_or_w():
    menu = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Мужское", callback_data="male")
    btn2 = types.InlineKeyboardButton(text="Женское", callback_data="female")
    menu.add(btn1, btn2)

    return menu


def show_paytypes(url: str):
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Да, ввести промокод", callback_data="promo")
    btn2 = types.InlineKeyboardButton(text="Нет, перейти к оплате (90₽)", url=url)
    btn3 = types.InlineKeyboardButton(text="Wildberries", callback_data="wildberries")
    menu.add(btn1, btn2, btn3)

    return menu


def share_button():
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Поделиться", url="https://t.me/share/url?url=Сотворите%20Новогоднее%20чудо%20для%20ребёнка.%20Попробуйте%20сейчас:%20@MorozRuBot")
    menu.add(btn1)

    return menu
