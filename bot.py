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
TOKEN = os.getenv ("8659283471:AAESk2nptd8f6ftX5KL5b9qLDgkW5kP6drM")

bot = Bot(token=TOKEN)
dp = Dispatcher()

ADMIN_ID = 6682364850

user_state = {}
admin_reply_state = {}


# =========================
# ?? ÌÅÍÞ
# =========================
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="?? Çàêàçàòü ðåìîíò")],
        [KeyboardButton(text="?? Ïðàéñ")],
        [KeyboardButton(text="????? Íàøè óñëóãè")],
        [KeyboardButton(text="?? Âûåçä ìàñòåðà")],
        [KeyboardButton(text="?? Ïîääåðæêà")]
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
        "?? Äîáðî ïîæàëîâàòü â AIRFIX!",
        reply_markup=main_menu
    )


# =========================
# ?? ÏÐÀÉÑ (ÏÎËÍÛÉ ÒÂÎÉ)
# =========================
@dp.message(F.text == "?? Ïðàéñ")
async def price(message: Message):

    await message.answer("""
?? ÏÐÀÉÑ AIRFIX

?? Òðóáà ìåäíàÿ äèàìåòð 6/9/12 — 17$ / ìåòð
?? Òðóáà ìåäíàÿ äèàìåòð 16/18 — 23$ / ìåòð

?? Îòâåðñòèå:
• êèðïè÷ — 100 000 ñóì
• áåòîí — 150 000 ñóì

?? Îòâåðñòèå ïîä äðåíàæ — 30 000 ñóì

?? Øòðîáà:
• êèðïè÷ — 100 000 ñóì / ì
• áåòîí — 130 000 ñóì / ì
• ïîä äðåíàæ — 50 000 ñóì / ì

?? Ïðîêëàäêà òðóáû — 5$ / ì
?? Ñâàðî÷íûé ñòûê — 40 000 ñóì

?? Ôðåîí:
• R410 / R32 — 60 000 / 100ãð
• R22 — 80 000 / 100ãð

?? Ïðîôèëàêòèêà — 300 000 ñóì

?? Óñòàíîâêà:
• 9/12 — 550 000 ñóì
• 18 — 650 000 ñóì
• 24 — 750 000 ñóì
• êîëîííûé — 120$

?? Ðåìîíò — ïî ôàêòó íåèñïðàâíîñòè
""")


# =========================
# ????? ÓÑËÓÃÈ
# =========================
@dp.message(F.text == "????? Íàøè óñëóãè")
async def services(message: Message):

    await message.answer("""
?? ÓÑÒÀÍÎÂÊÀ ÊÎÍÄÈÖÈÎÍÅÐÎÂ
?? ÐÅÌÎÍÒ ËÞÁÎÉ ÑËÎÆÍÎÑÒÈ
?? ÏÐÎÔÅÑÑÈÎÍÀËÜÍÀß ×ÈÑÒÊÀ
?? ÇÀÏÐÀÂÊÀ ÔÐÅÎÍÎÌ
?? ÄÈÀÃÍÎÑÒÈÊÀ ÍÅÈÑÏÐÀÂÍÎÑÒÅÉ
?? ÄÅÌÎÍÒÀÆ È ÏÅÐÅÍÎÑ
?? ÎÁÑËÓÆÈÂÀÍÈÅ ÊÂÀÐÒÈÐ È ÎÔÈÑÎÂ
?? ÁÛÑÒÐÛÉ ÂÛÅÇÄ ÏÎ ÒÀØÊÅÍÒÓ
""")


# =========================
# ?? ÂÛÅÇÄ ÌÀÑÒÅÐÀ
# =========================
@dp.message(F.text == "?? Âûåçä ìàñòåðà")
async def master_visit(message: Message):

    user_state[message.from_user.id] = "waiting_contact"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="?? Îòïðàâèòü íîìåð", request_contact=True)],
            [KeyboardButton(text="?? Îòïðàâèòü ãåîëîêàöèþ", request_location=True)],
            [KeyboardButton(text="?? Â ìåíþ")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "?? ÂÛÅÇÄ ÌÀÑÒÅÐÀ\n\nÑíà÷àëà îòïðàâüòå íîìåð > ïîòîì ãåîëîêàöèþ",
        reply_markup=kb
    )


# =========================
# ?? ÊÎÍÒÀÊÒ
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
?? ÍÎÂÀß ÇÀßÂÊÀ

?? {message.from_user.full_name}
?? {message.contact.phone_number}
"""
    )

    await message.answer(
        "? Íîìåð ïðèíÿò!\nÒåïåðü îòïðàâüòå ãåîëîêàöèþ ??",
        reply_markup=ReplyKeyboardRemove()
    )


# =========================
# ?? ÃÅÎËÎÊÀÖÈß
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
?? ÃÅÎËÎÊÀÖÈß

?? {message.from_user.full_name}
?? {loc.latitude}, {loc.longitude}

https://www.google.com/maps?q={loc.latitude},{loc.longitude}
"""
    )

    await message.answer(
        "? Çàÿâêà îòïðàâëåíà!",
        reply_markup=main_menu
    )


# =========================
# ?? ÇÀÊÀÇ ÐÅÌÎÍÒÀ (ÏÐÎÁËÅÌÛ)
# =========================
@dp.message(F.text == "?? Çàêàçàòü ðåìîíò")
async def order(message: Message):

    user_state[message.from_user.id] = "waiting_problem"

    await message.answer("""
?? ÎÏÈØÈÒÅ ÏÐÎÁËÅÌÓ:

?? Íå õîëîäèò
?? Øóìèò
?? Òå÷¸ò âîäà
?? Íå âêëþ÷àåòñÿ
?? Âûáèâàåò àâòîìàò
?? Ñëàáûé ïîòîê âîçäóõà

?? Èëè îïèøèòå ñâîèìè ñëîâàìè
""")


# =========================
# ?? ÏÎÄÄÅÐÆÊÀ
# =========================
@dp.message(F.text == "?? Ïîääåðæêà")
async def support(message: Message):

    user_state[message.from_user.id] = "support"

    await message.answer("?? Íàïèøèòå âàø âîïðîñ:")


# =========================
# ?? ÃËÀÂÍÛÉ ÐÎÓÒÅÐ
# =========================
@dp.message()
async def router(message: Message):

    uid = message.from_user.id
    state = user_state.get(uid)

    # -------------------------
    # ÀÄÌÈÍ ÎÒÂÅÒ
    # -------------------------
    if uid == ADMIN_ID:

        target = admin_reply_state.pop(uid, None)

        if target:
            await bot.send_message(
                target,
                f"?? Îòâåò ìàñòåðà:\n\n{message.text}"
            )
            await message.answer("? Îòâåò îòïðàâëåí êëèåíòó")
        else:
            await message.answer("? Ñíà÷àëà íàæìè «Îòâåòèòü»")
        return


    # -------------------------
    # ÐÅÌÎÍÒ
    # -------------------------
    if state == "waiting_problem":

        user_state.pop(uid, None)

        await bot.send_message(
            ADMIN_ID,
            f"""
?? ÐÅÌÎÍÒ

?? {message.from_user.full_name}
?? {message.text}
"""
        )

        await message.answer("? Çàÿâêà îòïðàâëåíà", reply_markup=main_menu)
        return


    # -------------------------
    # ÏÎÄÄÅÐÆÊÀ
    # -------------------------
    if state == "support":

        user_state.pop(uid, None)

        sent = await bot.send_message(
            ADMIN_ID,
            f"""
?? ÏÎÄÄÅÐÆÊÀ

?? {message.from_user.full_name}
?? {uid}

? {message.text}
"""
        )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="?? Îòâåòèòü", callback_data=f"reply_{uid}")]
            ]
        )

        await bot.edit_message_reply_markup(
            chat_id=ADMIN_ID,
            message_id=sent.message_id,
            reply_markup=kb
        )

        await message.answer("? Îòïðàâëåíî â ïîääåðæêó", reply_markup=main_menu)
        return


    # -------------------------
    # ÌÅÍÞ
    # -------------------------
    if message.text == "?? Â ìåíþ":
        user_state.pop(uid, None)
        await message.answer("?? Ãëàâíîå ìåíþ", reply_markup=main_menu)
        return


# =========================
# ?? ÊÍÎÏÊÀ ÎÒÂÅÒÈÒÜ
# =========================
@dp.callback_query(F.data.startswith("reply_"))
async def reply(call: CallbackQuery):

    uid = int(call.data.split("_")[1])

    admin_reply_state[call.from_user.id] = uid

    await call.message.answer("?? Íàïèøèòå îòâåò êëèåíòó")
    await call.answer()


# =========================
# ?? ÇÀÏÓÑÊ
# =========================
async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
