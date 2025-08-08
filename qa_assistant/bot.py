import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram import Router

from qa_assistant.settings import settings
from qa_assistant.repositories.user import user_repository

if not settings.bot_token:
    raise SystemExit("BOT_TOKEN is missing in environment (.env)")


router = Router()


def share_contact_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
    )


def programs_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Искусственный интеллект (AI)",
                    url="https://abit.itmo.ru/program/master/ai",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Управление ИИ-продуктами (AI Product)",
                    url="https://abit.itmo.ru/program/master/ai_product",
                )
            ],
        ]
    )


@router.message(CommandStart())
async def on_start(message: Message):
    # Если пользователь уже делился контактом — можно не просить заново
    # но для простоты всегда предлагаем поделиться
    await message.answer(
        "Привет! Я помогу определить, какая из двух магистерских программ тебе подходит. "
        "Пожалуйста, поделись контактом, чтобы я сохранил тебя в системе.",
        reply_markup=share_contact_kb(),
    )


@router.message(F.contact)
async def on_contact(message: Message):
    contact = message.contact
    # Если контакт прислал не сам пользователь (теоретически возможно), возьмём id/данные из contact
    user_id = contact.user_id or message.from_user.id
    phone = contact.phone_number
    first_name = contact.first_name or (message.from_user.first_name or None)
    last_name = contact.last_name or (message.from_user.last_name or None)
    username = message.from_user.username or None

    await user_repository.create(user_id, username, int(phone), first_name, last_name)

    await message.answer(
        "Спасибо! Контакт сохранён ✅\n\n"
        "Я помогаю определиться с выбором магистратуры из двух направлений ITMO:\n"
        "• «Искусственный интеллект»\n"
        "• «Управление ИИ-продуктами»\n\n"
        "Открой страницы программ или просто спроси меня о содержании, учебном плане, элективах и поступлении.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer("Страницы программ:", reply_markup=programs_kb())


@router.message()
async def fallback(message: Message):
    # На случай, если юзер пишет что-то до контакта
    await message.answer(
        "Для начала, пожалуйста, поделись контактом.",
        reply_markup=share_contact_kb(),
    )


bot = Bot(settings.bot_token)
dp = Dispatcher()
dp.include_router(router)
