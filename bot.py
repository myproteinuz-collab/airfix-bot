import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import os
TOKEN = os.getenv "8659283471:AAESk2nptd8f6ftX5KL5b9qLDgkW5kP6drM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

ADMIN_ID = 6682364850

user_state = {}
admin_reply_state = {}


# =========================
# ?? МЕНЮ
# =========================
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="?? Заказать ремонт")],
        [KeyboardButton(text="?? Прайс")],
        [KeyboardButton(text="????? Наши услуги")],
        [KeyboardButton(text="?? Выезд мастера")],
        [KeyboardButton(text="?? Поддержка")]
    ],
    resize_keyboard=True
)


# =========================
# ?? START
# =========================
@dp.message(CommandStart())
async def start(message: Message):
    user_state.pop(message.from_user.id, None)

    await message.answer(
        "?? Добро пожаловать в AIRFIX!",
        reply_markup=main_menu
    )


# =========================
# ?? ПРАЙС (ПОЛНЫЙ ТВОЙ)
# =========================
@dp.message(F.text == "?? Прайс")
async def price(message: Message):

    await message.answer("""
?? ПРАЙС AIRFIX

?? Труба медная диаметр 6/9/12 — 17$ / метр
?? Труба медная диаметр 16/18 — 23$ / метр

?? Отверстие:
• кирпич — 100 000 сум
• бетон — 150 000 сум

?? Отверстие под дренаж — 30 000 сум

?? Штроба:
• кирпич — 100 000 сум / м
• бетон — 130 000 сум / м
• под дренаж — 50 000 сум / м

?? Прокладка трубы — 5$ / м
?? Сварочный стык — 40 000 сум

?? Фреон:
• R410 / R32 — 60 000 / 100гр
• R22 — 80 000 / 100гр

?? Профилактика — 300 000 сум

?? Установка:
• 9/12 — 550 000 сум
• 18 — 650 000 сум
• 24 — 750 000 сум
• колонный — 120$

?? Ремонт — по факту неисправности
""")


# =========================
# ????? УСЛУГИ
# =========================
@dp.message(F.text == "????? Наши услуги")
async def services(message: Message):

    await message.answer("""
?? УСТАНОВКА КОНДИЦИОНЕРОВ
?? РЕМОНТ ЛЮБОЙ СЛОЖНОСТИ
?? ПРОФЕССИОНАЛЬНАЯ ЧИСТКА
?? ЗАПРАВКА ФРЕОНОМ
?? ДИАГНОСТИКА НЕИСПРАВНОСТЕЙ
?? ДЕМОНТАЖ И ПЕРЕНОС
?? ОБСЛУЖИВАНИЕ КВАРТИР И ОФИСОВ
?? БЫСТРЫЙ ВЫЕЗД ПО ТАШКЕНТУ
""")


# =========================
# ?? ВЫЕЗД МАСТЕРА
# =========================
@dp.message(F.text == "?? Выезд мастера")
async def master_visit(message: Message):

    user_state[message.from_user.id] = "waiting_contact"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="?? Отправить номер", request_contact=True)],
            [KeyboardButton(text="?? Отправить геолокацию", request_location=True)],
            [KeyboardButton(text="?? В меню")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "?? ВЫЕЗД МАСТЕРА\n\nСначала отправьте номер > потом геолокацию",
        reply_markup=kb
    )


# =========================
# ?? КОНТАКТ
# =========================
@dp.message(F.contact)
async def contact(message: Message):

    uid = message.from_user.id

    if user_state.get(uid) != "waiting_contact":
        return

    user_state[uid] = "waiting_location"

    await bot.send_message(
        ADMIN_ID,
        f"""
?? НОВАЯ ЗАЯВКА

?? {message.from_user.full_name}
?? {message.contact.phone_number}
"""
    )

    await message.answer(
        "? Номер принят!\nТеперь отправьте геолокацию ??",
        reply_markup=ReplyKeyboardRemove()
    )


# =========================
# ?? ГЕОЛОКАЦИЯ
# =========================
@dp.message(F.location)
async def location(message: Message):

    uid = message.from_user.id

    if user_state.get(uid) != "waiting_location":
        return

    loc = message.location

    user_state.pop(uid, None)

    await bot.send_message(
        ADMIN_ID,
        f"""
?? ГЕОЛОКАЦИЯ

?? {message.from_user.full_name}
?? {loc.latitude}, {loc.longitude}

https://www.google.com/maps?q={loc.latitude},{loc.longitude}
"""
    )

    await message.answer(
        "? Заявка отправлена!",
        reply_markup=main_menu
    )


# =========================
# ?? ЗАКАЗ РЕМОНТА (ПРОБЛЕМЫ)
# =========================
@dp.message(F.text == "?? Заказать ремонт")
async def order(message: Message):

    user_state[message.from_user.id] = "waiting_problem"

    await message.answer("""
?? ОПИШИТЕ ПРОБЛЕМУ:

?? Не холодит
?? Шумит
?? Течёт вода
?? Не включается
?? Выбивает автомат
?? Слабый поток воздуха

?? Или опишите своими словами
""")


# =========================
# ?? ПОДДЕРЖКА
# =========================
@dp.message(F.text == "?? Поддержка")
async def support(message: Message):

    user_state[message.from_user.id] = "support"

    await message.answer("?? Напишите ваш вопрос:")


# =========================
# ?? ГЛАВНЫЙ РОУТЕР
# =========================
@dp.message()
async def router(message: Message):

    uid = message.from_user.id
    state = user_state.get(uid)

    # -------------------------
    # АДМИН ОТВЕТ
    # -------------------------
    if uid == ADMIN_ID:

        target = admin_reply_state.pop(uid, None)

        if target:
            await bot.send_message(
                target,
                f"?? Ответ мастера:\n\n{message.text}"
            )
            await message.answer("? Ответ отправлен клиенту")
        else:
            await message.answer("? Сначала нажми «Ответить»")
        return


    # -------------------------
    # РЕМОНТ
    # -------------------------
    if state == "waiting_problem":

        user_state.pop(uid, None)

        await bot.send_message(
            ADMIN_ID,
            f"""
?? РЕМОНТ

?? {message.from_user.full_name}
?? {message.text}
"""
        )

        await message.answer("? Заявка отправлена", reply_markup=main_menu)
        return


    # -------------------------
    # ПОДДЕРЖКА
    # -------------------------
    if state == "support":

        user_state.pop(uid, None)

        sent = await bot.send_message(
            ADMIN_ID,
            f"""
?? ПОДДЕРЖКА

?? {message.from_user.full_name}
?? {uid}

? {message.text}
"""
        )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="?? Ответить", callback_data=f"reply_{uid}")]
            ]
        )

        await bot.edit_message_reply_markup(
            chat_id=ADMIN_ID,
            message_id=sent.message_id,
            reply_markup=kb
        )

        await message.answer("? Отправлено в поддержку", reply_markup=main_menu)
        return


    # -------------------------
    # МЕНЮ
    # -------------------------
    if message.text == "?? В меню":
        user_state.pop(uid, None)
        await message.answer("?? Главное меню", reply_markup=main_menu)
        return


# =========================
# ?? КНОПКА ОТВЕТИТЬ
# =========================
@dp.callback_query(F.data.startswith("reply_"))
async def reply(call: CallbackQuery):

    uid = int(call.data.split("_")[1])

    admin_reply_state[call.from_user.id] = uid

    await call.message.answer("?? Напишите ответ клиенту")
    await call.answer()


# =========================
# ?? ЗАПУСК
# =========================
async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())