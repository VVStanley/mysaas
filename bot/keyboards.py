from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def registration_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")],
        [InlineKeyboardButton(text="Описание возможностей", callback_data="about_us")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Функция 1", callback_data="func1")],
        [InlineKeyboardButton(text="Функция 2", callback_data="func2")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
