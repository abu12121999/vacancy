from keyboards.inline.vacancy_btn import vacancy_btn, vacancy_btn_passive
from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types


#############
# @dp.message_handler(commands=["active_vacancy"])
# async def create_category(message: types.Message):
#     if str(message.from_user.id) in ADMINS:
#
#         for vakansiya in db.select_active_vacancy():
#             caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
#                       f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
#                       f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
#                       f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
#                       f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
#                       f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
#             await bot.send_photo(chat_id=message.from_user.id, photo=vakansiya[-1], caption=caption)
#     else:
#         await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
##########################################################################################################
page_passive = 1


async def vac_page_passive(user_id):
    passive_vacancies = db.select_passive_vacancy()
    if passive_vacancies:
        global page_passive  # Foydalanish uchun global o'zgaruvchi
        # Sahifalash uchun kerakli qismi ajratib olish
        start_index = page_passive - 1
        vakansiya = passive_vacancies[start_index]
        caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                  f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                  f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                  f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                  f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                  f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"

        # Inline keyboard yaratish
        inline_keyboard = await vacancy_btn_passive(page, len(passive_vacancies))

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
        page -= 1
    elif callback_query.data == "next_passive":
        page += 1

    await vac_page_passive(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)


#########################################################################################################
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
        inline_keyboard = await vacancy_btn(page, len(active_vacancies))

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


###############################################################################################
@dp.message_handler(commands=["numbers_of_members"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        res = db.select_all_users()
        if res:
            await message.answer(f"Bot a'zolari soni = {len(res)} ta")
        else:
            await message.answer(f"/start bosib qaytadan urunib ko'ring")
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

#####################################################################################
@dp.message_handler(commands=["numbers_of_vacancy"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        active = db.select_active_vacancy()
        passive = db.select_passive_vacancy()
        res = f"Botdagi vakansiyalar soni = {len(active) + len(passive)} ta\n\n" \
              f"Aktiv: {len(active)} ta \n" \
              f"Muddati o'tgan: {len(passive)} ta\n"
        await message.answer(res)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
############################################################################################################
@dp.message_handler(commands=["vacants_list"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        pass
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

#####################################################################################


