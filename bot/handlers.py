from bot.saas import saas_client
from aiogram import Router
from bot.http_client import NotFoundException
from aiogram.types import CallbackQuery, Message
import logging
from bot.keyboards import main_menu_keyboard, registration_keyboard
from bot.saas.models import UserCreate

logger = logging.getLogger(__name__)
router = Router()


@router.message()
async def start(message: Message):
    try:
        user = await saas_client().get_user(telegram_id=message.from_user.id)
    except NotFoundException:
        user = None
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        await message.answer("⚠️ Временные проблемы с сервисом. Попробуйте позже.")
        return

    if not user:
        await message.answer(
            f"Привет! Для доступа к меню зарегистрируйся.",
            reply_markup=registration_keyboard(),
        )
    else:
        await message.answer(
            f"Добро пожаловать, {user.telegram_username}!\nТвой тарифф {user.tariff.name}:",
            reply_markup=main_menu_keyboard(),
        )


@router.callback_query(lambda c: c.data == "about_us")
async def about_us(query: CallbackQuery):
    await query.answer()
    await query.message.answer(
        "Краткий текст с описанием возможностей сервиса",
        reply_markup=registration_keyboard(),
    )


@router.callback_query(lambda c: c.data == "register")
async def register_user(query: CallbackQuery):
    await query.answer()
    try:
        user = await saas_client().create_user(
            user=UserCreate(
                telegram_id=query.from_user.id,
                telegram_username=query.from_user.username,
            )
        )
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        await query.message.answer(
            "❌ Не удалось завершить регистрацию. Попробуйте еще раз через несколько минут."
        )
        return
    await query.message.edit_text(
        f"🎉 Регистрация пройдена, {user.telegram_username}!\n"
        f"Теперь у тебя {user.tariff.name} тариф и есть доступ к меню.",
        reply_markup=main_menu_keyboard(),
    )


@router.message()
async def echo(message: Message):
    user_id = message.from_user.id
    await message.answer(
        f"Ты написал: {message.text} Твой Telegram ID: {user_id}\n Такой команды нет!"
    )
