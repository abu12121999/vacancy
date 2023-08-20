from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types
@dp.message_handler(commands=["active_vacancy"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:

        for vakansiya in db.select_active_vacancy():
            caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                      f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                      f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                      f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                      f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                      f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
            await bot.send_photo(chat_id=message.from_user.id, photo=vakansiya[-1], caption=caption)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")\

@dp.message_handler(commands=["numbers_of_members"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        res = db.select_all_users()
        await message.answer(f"Bot a'zolari soni = {len(res)} ta")
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")\


@dp.message_handler(commands=["numbers_of_members"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        pass
        await message.answer()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")



