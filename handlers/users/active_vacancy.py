from keyboards.inline.vacancy_btn import vacancy_btn
from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types
######################################active_vacancy###################################################################
page = 1
async def vac_page(user_id):
    active_vacancies = db.select_active_vacancy()
    if active_vacancies:
        global page  # Foydalanish uchun global o'zgaruvchi
        # Sahifalash uchun kerakli qismi ajratib olish
        start_index = page - 1
        vakansiya = active_vacancies[start_index]
        caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                  f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                  f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                  f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                  f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                  f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"

        # Inline keyboard yaratish
        inline_keyboard = await vacancy_btn(page, len(active_vacancies), vakansiya[-2])

        # Rasmni yuborish
        await bot.send_photo(chat_id=user_id, photo=vakansiya[-1], caption=caption,
                             reply_markup=inline_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text="Aktiv vakansiyalar mavjud emas")
@dp.message_handler(commands=["active_vacancy"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await vac_page(user_id=message.from_user.id)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

# Pagination tugmasi bosilganda ishlaydigan handler
@dp.callback_query_handler(lambda c: c.data in ["prev_page", "next_page"])
async def paginate_vacancies(callback_query: types.CallbackQuery):
    global page

    if callback_query.data == "prev_page" and page > 1:
        page -= 1
    elif callback_query.data == "next_page":
        page += 1

    await vac_page(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)
######################################active_vacancy###################################################################
