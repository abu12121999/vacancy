
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.aggrement import aggre
from keyboards.inline.vacancy_btn import vacancy_btn, vacancy_btn_user, vacancy_btn_interest
from loader import dp, db, bot


page = 1

async def interest_vac_page(user_id):
    vacant_id = user_id
    vacansies_id = db.select_vacant_by_id(vacant_id=vacant_id)
    vacansies = []
    for i in vacansies_id:
        vacansies.append(
            db.select_vacancy_by_id(i[0])[0]
        )
        print(vacansies)
    if vacansies:
        global page  # Foydalanish uchun global o'zgaruvchi
        # Sahifalash uchun kerakli qismi ajratib olish
        start_index = page - 1
        vakansiya = vacansies[start_index]
        caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                  f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                  f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                  f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                  f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n" \
                  f"<b>📌Status:</b> {vakansiya[6]}\n\n" \
                  f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"

        # Inline keyboard yaratish
        inline_keyboard = await vacancy_btn_interest(page, len(vacansies))

        # Rasmni yuborish
        await bot.send_photo(chat_id=user_id, photo=vakansiya[7], caption=caption,
                             reply_markup=inline_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text="Sizda qiziqish bildirilgan vakansiyalar mavjud emas!")
@dp.message_handler(Text(equals='💠Qiziqish bildirgan vakansiyalarim💠'))
async def interest_vac_page_main(message: types.Message):

    await interest_vac_page(user_id=message.from_user.id)


# Pagination tugmasi bosilganda ishlaydigan handler
@dp.callback_query_handler(lambda c: c.data in ["prev_user_interest", "next_user_interest"])
async def paginate_vacancies(callback_query: types.CallbackQuery):
    global page

    if callback_query.data == "prev_user_interest" and page > 1:
        page -= 1
    elif callback_query.data == "next_user_interest":
        page += 1

    await interest_vac_page(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)
