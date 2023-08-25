from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types
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

#############
# @dp.message_handler(commands=["active_vacancy"])
# async def create_category(message: types.Message):
#     if str(message.from_user.id) in ADMINS:
#         # Ma'lumotlar bazasidan olingan aktive vakansiyalar ro'yxatini olish
#         active_vacancies = db.select_active_vacancy()
#
#         # Sahifalash uchun kerakli o'zgaruvchilar
#         page = 1
#         per_page = 1  # Har bir sahifa uchun ko'rsatiladigan vakansiyalar soni
#         total_pages = (len(active_vacancies) + per_page - 1) // per_page
#
#         # Foydalanuvchiga faqat kerakli sahifani ko'rsatish
#         active_vacancies = active_vacancies[(page - 1) * per_page:page * per_page]
#
#         for vakansiya in active_vacancies:
#             caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
#                       f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
#                       f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
#                       f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
#                       f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
#                       f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
#             await bot.send_photo(chat_id=message.from_user.id, photo=vakansiya[-1], caption=caption)
#
#         # Pagination tugmalari yaratish
#         markup = InlineKeyboardMarkup(row_width=2)`
#         if page > 1:
#             markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_page"))
#         if page < total_pages:
#             markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_page"))
#
#         await message.answer("Vakansiyalar ro'yxati", reply_markup=markup)
#     else:
#         await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
#
#
# # Pagination tugmasi bosilganda ishlaydigan handler
# @dp.callback_query_handler(lambda c: c.data in ["prev_page", "next_page"])
# async def paginate_vacancies(callback_query: types.CallbackQuery):
#     active_vacancies = db.select_active_vacancy()
#     page = 1  # O'zgartirish uchun sahifani yaxshi saqlang
#     per_page = 1  # O'zgartirish uchun har bir sahifa uchun ko'rsatiladigan vakansiyalar soni
#     total_pages = (len(active_vacancies) + per_page - 1) // per_page
#
#     if callback_query.data == "prev_page" and page > 1:
#         page -= 1
#     elif callback_query.data == "next_page" and page < total_pages:
#         page += 1
#
#     active_vacancies = active_vacancies[(page - 1) * per_page:page * per_page]
#
#     # Yangi sahifa o'zgartirilgan ma'lumotlar bilan yangilanadi
#     for vakansiya in active_vacancies:
#         caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
#                   f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
#                   f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
#                   f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
#                   f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
#                   f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
#         await bot.send_photo(chat_id=callback_query.from_user.id, photo=vakansiya[-1], caption=caption)
#
#     # Yangi tugmalar qo'shish
#     markup = InlineKeyboardMarkup(row_width=2)
#     if page > 1:
#         markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_page"))
#     if page < total_pages:
#         markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_page"))
#
#     await callback_query.message.edit_reply_markup(reply_markup=markup)
# ###########

@dp.message_handler(commands=["passive_vacancy"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:

        for vakansiya in db.select_passive_vacancy():
            caption = f"<b>📁Kategoriya: {vakansiya[0]}\n\n</b>" \
                      f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
                      f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
                      f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
                      f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n\n" \
                      f"<b>⏳Vakansiya yopilgan muddati:</b> {vakansiya[5]}"
            await bot.send_photo(chat_id=message.from_user.id, photo=vakansiya[-1], caption=caption)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

@dp.message_handler(commands=["numbers_of_members"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        res = db.select_all_users()
        await message.answer(f"Bot a'zolari soni = {len(res)} ta")
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")


@dp.message_handler(commands=["numbers_of_members"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        pass
        await message.answer()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")




