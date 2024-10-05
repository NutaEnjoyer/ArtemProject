from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import User

import re

BOT_TOKEN = "7711412652:AAGidxb29rfpdbi0lDDhHPdbLsf2PZJJ35Y"  # Bot Token
ADMINS_ID = [866023953, 5922769257, 5344758315] # ID of the admin user

PHOTO_URL = "https://sun9-43.userapi.com/impg/x5LD1r8-v0RvxAN6V3GCusQvU7XjVLi11yqZVw/JuQTjJkDkjw.jpg?size=818x558&quality=95&sign=2d3f7acea3f5ab88c9294be54daad7de&type=album"


GREETING_TEXT = """<i><b>⠀⠀⠀⠀⠀⠀˗ˏˋ༻ʚ♡ɞ༺ˎˊ˗
Добро пожаловать , тут ты можешь приобрести мой VIP /приватик !! 🤍</b>

💌 ты получишь доступ к моему эксклюзивному контенту 18+ , которого нет в свободном доступе !

﻿﻿💌 так же будет ссылочка для общения со мной лично , подписывайся и напиши мне</i>"""

SEMI_MESSAGE = "Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку"

class Tariff:
    def __init__(self, title, price, price_usd, about, resources):
        self.title = title
        self.price = price
        self.price_usd = price_usd
        self.about = about
        self.resources = resources


TARIFFS = [
    Tariff(
        title = "⭐️ ПРОБНЫЙ VIP", price = 300, price_usd =3.5, about = "этот канал, для тех кто сомневается, тут ты сможешь попробовать меня на вкус 👅", resources = " • ⭐️ ПРОБНЫЙ VIP - канал"
    ),
    Tariff(
        title = "🔥 ПРЕМИУМ VIP", price = 2400, price_usd = 260, about = """<i>тут все мои тайные и3вращени9, много контента, который регулярно пополняется

получишь от меня приятный бонус за подписку в виде эксклюзивной фотосессии или видео 🔥</i>""", resources = " • 🔥 ПРЕМИУМ VIP - канал"
    ),
    Tariff(
        title = "👑 ЭКСКЛЮЗИВ VIP", price = 6000, price_usd =70, about = """<i>тут все мои тайные эксклюзивные и3вращени9, много контента, который регулярно пополняется

тебя ждет мои приятные моменты с подругами и партнерами и много другого интересного 😛 только для истинных шалунов

получишь от меня приятный бонус за подписку в виде эксклюзивной фотосессии или видео 🔥</i>""", resources = " • 👑 ЭКСКЛЮЗИВ VIP - канал"
    ),
    Tariff(
        title = "🔞 ВИРТ", price = 1800, price_usd =20, about = """<b>Дорогой, мы можем провести Вирт в совершенно разных вариантах: 😛</b>

- переписка с моими кружками для тебя 
- устроить жаркий разговор по телефону 
- созвониться по видео""", resources = " • 🔞 ВИРТ - канал"
    ),
]


requisites = {
    "card": "2204240129569432",
    "usdt": "EQBSjuWXqDtrisVtYDYJrX70Xf-SzTtRR-qgaUwAYCBJ29KD"
}


def STAT_TEXT():
    user = User.select()
    return f"""Всего пользователей: {len(user)}"""


def MAIL_TEXT():
    return f"""Отправьте сообщение для рассылки"""


def MAIL_STAT_MESSAGE(suc, err):
    return f"""<b>Успешно отправлено: {suc}</b>
<b>Не отправлено: {err}</b>"""

def tariff_text(tariff: Tariff):
    return f"""
<b>Тариф: {tariff.title}</b>

<b>Стоимость: <s>{tariff.price * 2}</s>  {tariff.price} </b>🇷🇺RUB

<b>Срок действия: </b> бессрочно

<b>Вы получите доступ к следующим  ресурсам: 
{tariff.resources}</b>

{tariff.about}
"""

def tariff_pay_text(tariff: Tariff):
    return f"""
<b>Тариф: {tariff.title}</b>

<b>Стоимость: <s>{tariff.price * 2}</s>  {tariff.price} </b>🇷🇺RUB

<b>Срок действия: </b> бессрочно

<b>Выберите способ оплаты:</b>"""

def crypto_pay_text(tariff: Tariff, user_id: int):
    return f"""Способ оплаты: <b>Крипта 💰USDT</b>
К оплате: <b>{tariff.price}🇷🇺RUB</b>
Ваш ID: <b>{user_id}</b>
Реквезиты для оплаты:

USDT

{requisites["usdt"]}

⚠️ Сети TRC 20 или TON 

После перевода скрин присылать в бота

1$ = 90₽
_______________________________
<i>Вы платите физическому лицу.
Деньги поступят на счет получателя.</i>"""



def card_pay_text(tariff: Tariff, user_id: int):
    return f"""Способ оплаты: <b>Банковская карта 💳</b>
К оплате: <b>{tariff.price}🇷🇺RUB</b>
Ваш ID: <b>{user_id}</b>
Реквезиты для оплаты:

📌 <i>Карта:</i> {requisites["card"]}

❗️ Переводите сумму указанную в тарифе и после перевода скрин присылать в бота
_______________________________
<i>Вы платите физическому лицу.
Деньги поступят на счет получателя.</i>"""


def requests_photo():
    return f"""💁🏻‍♂️ Оплатили?

👌🏻 Тогда отправьте сюда картинкой (не документом!) квитанцию платежа: скриншот или фото.

На квитанции должны быть четко видны: дата, время и сумма платежа.
______
За спам вы можете быть заблокированы!"""

def get_photo():
    return f"""✅ Квитанция отправлена на проверку.

Пожалуйста, ожидайте. Бот вам сообщит об успешном платеже."""

def admin_text(tariff_id: int, username, user_id, user_first_name):
    tariff = TARIFFS[tariff_id]
    return f"""<b>Тариф: {tariff.title}

Ссылка: @{username}
ID: {user_id}
Имя: {user_first_name}</b>"""

def tariffs_menu_keyboard():
    keys = []
    for i in range(len(TARIFFS)):  # Включаем все тарифы
        keys.append([InlineKeyboardButton(text=TARIFFS[i].title, callback_data=f"tariff_{i}")])  # Списки списков

    return InlineKeyboardMarkup(inline_keyboard=keys)


def tariff_keyboard(tariff_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", callback_data=f"pay_{tariff_id}")],
            [InlineKeyboardButton(text="👈 Назад", callback_data=f"back")],
        ]
    )

def tariff_pay_keyboard(tariff_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Крипта 💰", callback_data=f"crypto_pay_{tariff_id}")],
            [InlineKeyboardButton(text="Банковская карта 💳", callback_data=f"card_pay_{tariff_id}")],
            [InlineKeyboardButton(text="👈 Назад", callback_data=f"back_to_tariff_{tariff_id}")],
        ]
    )

def pay_keyboard(tariff_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏳ Я оплатил", callback_data=f"i_pay_{tariff_id}")],
            [InlineKeyboardButton(text="👈 Назад", callback_data=f"back_to_pay_tariff_{tariff_id}")],
        ]
    )

def cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data=f"cancel")],
        ]
    )

def parse_keyboard(text: str) -> InlineKeyboardMarkup:
    """
    Функция принимает строку текста и возвращает объект InlineKeyboardMarkup.

    Формат текста:
    - Кнопки в строке разделяются символом |
    - Разные строки кнопок разделяются символом новой строки \n
    Пример:
    [Кнопка 1](callback_1) | [Кнопка 2](callback_2)
    [Кнопка 3](callback_3)
    """
    # Регулярное выражение для парсинга текста вида [текст кнопки](callback_data)
    pattern = re.compile(r'\[(.*?)\]\((.*?)\)')

    # Разбиваем текст по строкам (каждая строка кнопок разделена \n)
    rows = text.split('|')

    # Создаем список для строк кнопок
    inline_keyboard = []

    for row in rows:
        # Разбиваем строку на кнопки по символу "|"
        buttons = []
        for button_text in row.split(','):
            match = pattern.findall(button_text.strip())
            if match:
                # Каждая кнопка должна быть в формате [текст](callback_data)
                for button_data in match:
                    button_text, callback_data = button_data
                    buttons.append(InlineKeyboardButton(text=button_text.strip(), callback_data=callback_data.strip()))

        if buttons:
            # Добавляем строку кнопок в итоговую клавиатуру как отдельную строку
            inline_keyboard.append(buttons)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def is_valid_keyboard_format(text: str) -> bool:
    """
    Проверяет, можно ли распарсить текст как объект InlineKeyboardMarkup.

    Формат:
    - Кнопки должны быть в формате [Текст кнопки](callback_data)
    - Кнопки в строке разделяются символом |
    - Строки разделяются символом новой строки \n

    Возвращает True, если текст можно распарсить, иначе False.
    """
    # Регулярное выражение для парсинга текста вида [текст](callback_data)
    pattern = re.compile(r'\[(.*?)\]\((.*?)\)')

    # Разбиваем текст на строки (каждая строка кнопок разделена \n)
    rows = text.split('\n')

    for row in rows:
        # Разбиваем строку на кнопки по символу |
        buttons = row.split('|')

        for button in buttons:
            # Проверяем, что каждая кнопка соответствует шаблону [текст](callback_data)
            match = pattern.fullmatch(button.strip())
            if not match:
                print(button)
                return False  # Если хотя бы одна кнопка не соответствует шаблону, возвращаем False

    return True
