
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.aggrement import aggre
from keyboards.inline.vacancy_btn import vacancy_btn, vacancy_btn_user
from loader import dp, db, bot

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
        inline_keyboard = await vacancy_btn_user(page, len(active_vacancies), vakansiya[7])

        # Rasmni yuborish
        await bot.send_photo(chat_id=user_id, photo=vakansiya[-1], caption=caption,
                             reply_markup=inline_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text="Aktiv vakansiyalar mavjud emas")
@dp.message_handler(Text(equals='📖 Vakansiyalar'))
async def create_category(message: types.Message):

    await vac_page(user_id=message.from_user.id)


# Pagination tugmasi bosilganda ishlaydigan handler
@dp.callback_query_handler(lambda c: c.data in ["prev_user", "next_user"])
async def paginate_vacancies(callback_query: types.CallbackQuery):
    global page

    if callback_query.data == "prev_user" and page > 1:
        page -= 1
    elif callback_query.data == "next_user":
        page += 1

    await vac_page(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)
#intersest
@dp.callback_query_handler(lambda c: "interest_user" in c.data)
async def paginate_vacancies(callback_query: types.CallbackQuery, state: FSMContext):
    res = f"<b>Sizning vakansiyaga qiziqishiz qayd etilsinmi? </b>"
    btn = await aggre(foo="interest_aggre")
    await callback_query.message.answer(res,reply_markup=btn)
    await state.set_state("interest_state")
    await state.update_data(
        {"vac_id": callback_query.data.split("_")[-1]}
    )
    print(callback_query.message.text.split("_")[-1])
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)

######################################################################################
@dp.callback_query_handler(lambda c: "interest_aggre" in c.data, state="interest_state")
async def get_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    data = await state.get_data()
    vacancy_id = data.get("vac_id")
    vacant_id = query.from_user.id
    if a == "yes":

        vacansies0 = db.select_vacant_by_id(vacant_id)
        vacansies = []
        for i in vacansies0:
            vacansies.append(i[0])

        if vacancy_id not in vacansies:
            db.add_vacant(
                vacant_id=vacant_id,
                vacancy_id=vacancy_id
            )
            await query.message.answer(f"<b>✅Sizning vakansiyaga qiziqishingiz qayd etildi!</b>")
        else:
            await query.message.answer(f"<b>⚠️Siz bu vakansiyaga qiziqish bildirgansiz!</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Sizning vakansiyaga qiziqishingiz qayd etilmadi!</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)




