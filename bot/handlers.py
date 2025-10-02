# bot/handlers.py
from aiogram import Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards import main_menu_keyboard, registration_keyboard

router = Router()


@router.message()
async def start(message: Message):
    tg_id = str(message.from_user.id)
    user = False

    if not user or not user.is_registered:
        await message.answer(
            "Привет! Для доступа к меню зарегистрируйся.",
            reply_markup=registration_keyboard(),
        )
    else:
        await message.answer("Добро пожаловать! Вот твое меню:", reply_markup=main_menu_keyboard())


@router.callback_query(lambda c: c.data == "register")
async def register_user(query: CallbackQuery):
    tg_id = str(query.from_user.id)
    # user, created = User.objects.get_or_create(
    #     telegram_id=tg_id,
    #     defaults={"nickname": query.from_user.username, "is_registered": True},
    # )
    # if not created:
    #     user.is_registered = True
    #     user.save()

    await query.message.edit_text(
        "Регистрация пройдена! Теперь у тебя есть доступ к меню.",
        reply_markup=main_menu_keyboard(),
    )


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")
