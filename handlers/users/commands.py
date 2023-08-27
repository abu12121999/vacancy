from keyboards.inline.vacancy_btn import vacancy_btn, vacancy_btn_passive, vacancy_btn_nomzod
from data.config import ADMINS
from loader import db, dp, bot
from aiogram import types
###################################numbers_of_members############################################################
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

###################################numbers_of_vacancy##################################################
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

#########################################vacants_list#######################################################
p = 1
async def vacants_page(id, user_id):
    vacants = db.select_vacants_id(id=id)
    if vacants:
        vacants_id = [v[0] for v in tuple(set(vacants))]
        users = [db.select_user(telegram_id=user) for user in vacants_id]
        user = users[p-1]
        res = f"👤<b> Nomzod ma'lumotlari</b>\n\n" \
              f"👉<b>️ Ism: </b><code>{user[1]}</code>\n" \
              f"👉<b> Familiya: </b><code>{user[2]}</code>\n" \
              f"☎️<b> Telefon raqam: </b><code>{user[4]}</code>\n"
        btn = await vacancy_btn_nomzod(p, len(users), id)
        await bot.send_message(chat_id=user_id, text=res,reply_markup=btn)
    else:
        await bot.send_message(chat_id=user_id, text=f"<b>❗️Bu vakansiya bo'yicha nomzodlar ro'yxati topilmadi</b>")
######
@dp.callback_query_handler(lambda c: "vacants_list" in c.data )
async def vacant_list(callback_query: types.CallbackQuery):
    await callback_query.answer()
    id = callback_query.data.split("_")[-1]
    await vacants_page(id, callback_query.from_user.id)
######
@dp.callback_query_handler(lambda c: ("p_page" in c.data) or "n_page" in c.data)
async def page_vacancies(callback_query: types.CallbackQuery):
    global p
    await callback_query.answer()
    id = callback_query.data.split("_")[-1]

    if "p_page" in callback_query.data and p > 1:
        p -= 1
    elif "n_page" in callback_query.data:
        p += 1
    await vacants_page(id=id, user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.answer(cache_time=60)
############################################################################################################