from datetime import datetime
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards.inline.categories import category_list
from keyboards.inline.aggrement import aggre
from loader import db, dp, bot
from states.vacancyADD import vacancy_edit
######################
async def edit_vacancyy(id):
    try:
        db.edit_vacancy_status_by_id(status="passive", vacancy_id=id)
    except:
        pass
######################################################################################
@dp.callback_query_handler(lambda c: "change_vac" in c.data)
async def change_vacancy(query: CallbackQuery, state: FSMContext):
    await query.answer("Yuqoridagi vakansiyani tahrirlamoqdasiz!", show_alert=True)
    id = query.data.split('_')[-1]
    btn = await category_list(foo="hcange")
    if btn["inline_keyboard"]:
        await query.message.answer(f"Vakansiya uchun kategoriyalaridan birini tanlang", reply_markup=btn)
        await vacancy_edit.category.set()
        await state.update_data(id=id)
        await query.answer(cache_time=60)
    else:
        await query.message.answer("Kategoriya topilmadi. Kategoriya yaratib keyin urunib ko'ring")
        await state.finish()
        await query.answer(cache_time=60)
######################################################################################
@dp.callback_query_handler(lambda c: "hcange" in c.data, state=vacancy_edit.category)
async def get_category_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    category_id = query.data.split("_")[-1]
    await state.update_data(
        {"category": db.select_category(category_id=category_id)[0]}
    )
    await query.message.answer(f"Vakansiyaga yangi nom bering")
    await vacancy_edit.name.set()
    await query.message.delete()
    await query.answer(cache_time=60)
######################################################################################
@dp.message_handler(state=vacancy_edit.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {"name": name}
    )
    await message.answer(f"Vakansiya uchun yangi narx belgilang ")
    await vacancy_edit.salary.set()

######################################################################################
@dp.message_handler(state=vacancy_edit.salary)
async def salary(message: types.Message, state: FSMContext):
    salary = message.text
    await state.update_data(
        {"salary": salary}
    )
    await message.answer(f"Vakansiya haqida yangi ma'lumot bering. Ma'lumot ichida aloqa uchun telefon raqam qoldiring")
    await vacancy_edit.description.set()

######################################################################################
@dp.message_handler(state=vacancy_edit.description)
async def description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {"description": description}
    )
    await message.answer(f"Vakansiya uchun yangi rasm yuboring")
    await vacancy_edit.file.set()

######################################################################################
@dp.message_handler(content_types=types.ContentType.ANY, state=vacancy_edit.file)
async def photo(message: types.Message, state: FSMContext):
        if message.photo:
            file_id = message.photo[-1].file_id
            await state.update_data(
                {"file_id": file_id}
            )
            res = f"Vakansiya yopilish vaqtini belgilang\n" \
                  f"<i>Format:dd/mm/yy hh:mm </i>  " \
                  f"<b>Masalan: 20/10/2023 12:00</b>"
            await message.answer(res)
            await vacancy_edit.deadline.set()
        else:
            await message.answer(f"Vakansiya uchun rasm yuboring")
            await vacancy_edit.file.set()

# ######################################################################################
@dp.message_handler(state=vacancy_edit.deadline)
async def photo(message: types.Message, state: FSMContext):
        date_time_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4} (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        date_time_string = message.text.strip()

        if re.match(date_time_pattern, date_time_string):
            await state.update_data(
                {"deadline": date_time_string}
            )
            data = await state.get_data()
            category = data["category"]
            name = data["name"]
            salary = data["salary"]
            description = data["description"]
            file_id = data["file_id"]
            deadline = date_time_string

            caption = f"<b>📁Kategoriya: {category}\n\n</b>" \
                      f"<b>📝Nomi:</b> {name}\n" \
                      f"<b>💰Ish haqqi:</b> {salary}\n" \
                      f"<b>🖇Ta'rif:</b> {description}\n\n" \
                      f"<b>⏳Vakansiya muddati:</b> {deadline}"
            await bot.send_photo(chat_id=message.from_user.id, photo=file_id, caption=caption)

            btn = await aggre(foo="publish")
            await message.answer("Tahrirlangan vakansiya chop etilsinmi?", reply_markup=btn)
            await vacancy_edit.rozi.set()

        else:
            res = f"Vakansiya yopilish vaqtini to'g'ri yuboring\n" \
                  f"<i>Format:dd/mm/yy hh:mm </i>  " \
                  f"<b>Masalan: 20/10/2023 12:00</b>"
            await message.answer(res)
            await vacancy_edit.deadline.set()
# ######################################################################################
@dp.callback_query_handler(lambda c: "publish" in c.data, state=vacancy_edit.rozi)
async def get_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        id = data["id"]
        category = data["category"]
        name = data["name"]
        salary = data["salary"]
        description = data["description"]
        file_id = data["file_id"]
        deadline = data["deadline"]

        now = datetime.now(pytz.timezone("Asia/Tashkent"))
        plantime = pytz.timezone("Asia/Tashkent").localize(datetime.strptime(deadline, "%d/%m/%Y %H:%M"))

        if now < plantime:
            status = "active"
        else:
            status = "passive"
            print(status)

        db.edit_vacancy(
            vacancy_id=id,
            category=category,
            name=name,
            salary=salary,
            description=description,
            file_id=file_id,
            deadline=deadline,
            status=status
        )
        if status == "active":
            scheduled_datetime = datetime.strptime(deadline, "%d/%m/%Y %H:%M")
            scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tashkent"))
            scheduler.add_job(edit_vacancyy, 'date', run_date=scheduled_datetime, args=[id])
            scheduler.start()
        await query.message.answer(f"<b>✅Vakansiya muvaffaqiyatli tahrirlandi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Vakansiya tahrirlanmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)

################# del vac ############################################
@dp.callback_query_handler(lambda c: "del_vac" in c.data)
async def del_vacancy(query: CallbackQuery, state: FSMContext):
    await query.answer("Yuqoridagi vakansiyani o'chirmoqdasiz!", show_alert=True)
    id = query.data.split('_')[-1]
    await state.set_state("del_aggre_p")
    await state.update_data(
        {"id": id}
    )
    vakansiya = db.select_vacancy_by_id(vacancy_id=id)[0]
    caption = f"<b><i>Bu vakansiya o'chirilsinmi ?</i></b>\n\n" \
              f"<b>📁Kategoriya: {vakansiya[0]}\n</b>" \
              f"<b>📝Nomi:</b> {vakansiya[1]}\n" \
              f"<b>💰Ish haqqi:</b> {vakansiya[2]}\n" \
              f"<b>📍Manzil:</b> {vakansiya[3]}\n" \
              f"<b>🖇Ta'rif:</b> {vakansiya[4]}\n" \
              f"<b>📌Status:</b> {vakansiya[6]}\n\n" \
              f"<b>⏳Vakansiya muddati:</b> {vakansiya[5]}"
    btn = await aggre(foo="del_a_p")
    await bot.send_photo(chat_id=query.from_user.id, photo=vakansiya[7], caption=caption, reply_markup=btn)
    await query.answer(cache_time=60)

@dp.callback_query_handler(lambda c: "del_a_p" in c.data, state="del_aggre_p")
async def get_aggrement_delete(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]

    if a == "yes":
        data = await state.get_data()
        id = data.get("id")
        db.delete_vacancy(id)
        await query.message.answer(f"<b>✅Vakansiya muvaffaqiyatli o'chirildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Vakansiya o'chirilmadi</b>")
        await state.finish()
    await query.message.delete()
    await query.answer(cache_time=60)


