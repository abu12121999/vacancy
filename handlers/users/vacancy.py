from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import menu
from loader import dp, db, bot


@dp.message_handler(Text(equals='📖 Vakansiyalar'))
async def vacancy(message: types.Message):
    for vakansiya in db.select_active_vacancy():
        caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                  f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                  f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                  f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                  f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                  f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
        await bot.send_photo(chat_id=message.from_user.id, photo=vakansiya[-1], caption=caption)