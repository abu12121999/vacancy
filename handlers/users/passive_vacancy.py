from keyboards.inline.vacancy_btn import vacancy_btn_passive
from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types

######################################passive_vacancy####################################################################
page_passive = 1
async def vac_page_passive(user_id):
    passive_vacancies = db.select_passive_vacancy()
    if passive_vacancies:
        global page_passive  # Foydalanish uchun global o'zgaruvchi
        # Sahifalash uchun kerakli qismi ajratib olish
        vakansiya = passive_vacancies[page_passive - 1]
        caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                  f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                  f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                  f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                  f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                  f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"

        # Inline keyboard yaratish
        inline_keyboard = await vacancy_btn_passive(page_passive, len(passive_vacancies), vakansiya[-2])

        # Rasmni yuborish
        await bot.send_photo(chat_id=user_id, photo=vakansiya[-1], caption=caption,
                             reply_markup=inline_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text="Muddati tugagan vakansiyalar mavjud emas")
@dp.message_handler(commands=["passive_vacancy"])
async def p_passive(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await vac_page_passive(user_id=message.from_user.id)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
# Pagination tugmasi bosilganda ishlaydigan handler
@dp.callback_query_handler(lambda c: c.data in ["prev_passive", "next_passive"])
async def paginate_vacancies_passive(callback_query: types.CallbackQuery):
    global page_passive

    if callback_query.data == "prev_passive" and page_passive > 1:
        page_passive -= 1
    elif callback_query.data == "next_passive":
        page_passive += 1

    await vac_page_passive(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)

