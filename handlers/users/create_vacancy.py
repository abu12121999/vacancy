from datetime import datetime
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards.inline.districst import district_list
from keyboards.inline.villages import village_list
from keyboards.inline.categories import category_list
from keyboards.inline.aggrement import aggre
from data.config import ADMINS
from loader import db, dp, bot
from states.vacancyADD import vacancy_add
from utils.db_api.districts import districts
import uuid
######################
async def edit_vacancy(u_id):
    u_id=u_id
    try:
        db.edit_vacancy_status(status="passive", uuid=u_id)
    except:
        pass
####################
@dp.message_handler(commands=["create_vacancy"])
async def create_vacancy(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        btn = await district_list(foo="vacant")
        await message.answer(text="📌 Qaysi tumanga vakansiya qo'shasiz", reply_markup=btn)
        await vacancy_add.location1.set()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
######################################################################################
@dp.callback_query_handler(lambda c: "vacant" in c.data, state=vacancy_add.location1)
async def get_reg_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    location1 = query.data.split("_")[-1]
    await state.update_data(
        {"location1": districts[int(location1)]}
    )
    btn = await village_list(foo="btnvilla", reg_id=location1)
    if btn["inline_keyboard"]:
        await query.message.answer(f"Mahallani tanlang", reply_markup=btn)
        await vacancy_add.location2.set()
        await query.message.delete()
        await query.answer(cache_time=60)
    else:
        await query.message.answer("Keltirilgan tumanga mahalla biriktirilmagan iltimos mahalla biriktirib keyin urunib ko'ring")
        await state.finish()
        await query.message.delete()
        await query.answer(cache_time=60)
######################################################################################
@dp.callback_query_handler(lambda c: "btnvilla" in c.data, state=vacancy_add.location2)
async def get_loacation2_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    location2 = query.data.split("_")[-1]
    await state.update_data(
        {"location2": db.get_village_name(village_id=location2)[0]}
    )
    btn = await category_list(foo="btncat")
    if btn["inline_keyboard"]:
        await query.message.answer(f"Ish kategoriyalaridan birini tanlang", reply_markup=btn)
        await vacancy_add.category.set()
        await query.message.delete()
        await query.answer(cache_time=60)
    else:
        await query.message.answer("Kategoriya mavjud emas. Kategoriya yaratib keyin urunib ko'ring")
        await state.finish()
        await query.message.delete()
        await query.answer(cache_time=60)
######################################################################################
@dp.callback_query_handler(lambda c: "btncat" in c.data, state=vacancy_add.category)
async def get_category_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    category_id = query.data.split("_")[-1]
    await state.update_data(
        {"category": db.select_category(category_id=category_id)[0]}
    )
    await query.message.answer(f"Vakansiyaga nom bering")
    await vacancy_add.name.set()
    await query.message.delete()
    await query.answer(cache_time=60)
######################################################################################
@dp.message_handler(state=vacancy_add.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {"name": name}
    )
    await message.answer(f"Vakansiya uchun narx belgilang ")
    await vacancy_add.salary.set()

######################################################################################
@dp.message_handler(state=vacancy_add.salary)
async def salary(message: types.Message, state: FSMContext):
    salary = message.text
    await state.update_data(
        {"salary": salary}
    )
    await message.answer(f"Vakansiya haqida ma'lumot bering. Ma'lumot ichida aloqa uchun telefon raqam qoldiring")
    await vacancy_add.description.set()

######################################################################################
@dp.message_handler(state=vacancy_add.description)
async def description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {"description": description}
    )
    await message.answer(f"Vakansiya uchun rasm yuboring")
    await vacancy_add.file.set()

######################################################################################
@dp.message_handler(content_types=types.ContentType.ANY, state=vacancy_add.file)
async def photo(message: types.Message, state: FSMContext):
        if message.photo:
            file_id = message.photo[-1].file_id
            await state.update_data(
                {"file_id": file_id}
            )
            res = f"Vakansiya yopilish vaqtini belgilang\n<i>Format:dd/mm/yy hh:mm </i>  <b>Masalan: 20/10/2023 12:00</b>"
            await message.answer(res)
            await vacancy_add.deadline.set()
        else:
            await message.answer(f"Vakansiya uchun rasm yuboring")
            await vacancy_add.file.set()

# ######################################################################################
@dp.message_handler(state=vacancy_add.deadline)
async def photo(message: types.Message, state: FSMContext):
        date_time_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4} (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        date_time_string = message.text.strip()
        await state.update_data(
            {"deadline": date_time_string}
        )
        if re.match(date_time_pattern, date_time_string):
            data = await state.get_data()
            location = data["location1"] + " tumani " + data["location2"] + " mahallasi"
            category = data["category"]
            name = data["name"]
            salary = data["salary"]
            description = data["description"]
            file_id = data["file_id"]
            deadline = date_time_string

            caption = f"<b>📁Kategoriya: {category}\n\n</b>" \
                      f"<b>📝Nomi:</b> {name}\n" \
                      f"<b>💰Ish haqqi:</b> {salary}\n" \
                      f"<b>📍Manzil:</b> {location}\n" \
                      f"<b>🖇Ta'rif:</b> {description}\n\n" \
                      f"<b>⏳Vakansiya muddati:</b> {deadline}"
            await bot.send_photo(chat_id=message.from_user.id, photo=file_id, caption=caption)

            btn = await aggre(foo="publish")
            await message.answer("Bu vakansiyani chop etmoqchimisiz?", reply_markup=btn)
            await vacancy_add.rozi.set()

        else:
            res = f"Vakansiya yopilish vaqtini to'g'ri yuboring\n<i>Format:dd/mm/yy hh:mm </i>  <b>Masalan: 20/10/2023 12:00</b>"
            await message.answer(res)
            await vacancy_add.deadline.set()
# ######################################################################################
@dp.callback_query_handler(lambda c: "publish" in c.data, state=vacancy_add.rozi)
async def get_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        location = data["location1"] + " tumani " + data["location2"] + " mahallasi"
        category = data["category"]
        name = data["name"]
        salary = data["salary"]
        description = data["description"]
        file_id = data["file_id"]
        deadline = data["deadline"]

        u_id= str(uuid.uuid4())
        db.add_vacancy(
            location=location,
            category=category,
            name=name,
            author_id=query.from_user.id,
            salary=salary,
            description=description,
            file_id=file_id,
            deadline=deadline,
            status="active",
            uuid=u_id
        )

        scheduled_datetime = datetime.strptime(deadline, "%d/%m/%Y %H:%M")
        scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tashkent"))
        scheduler.add_job(edit_vacancy, 'date', run_date=scheduled_datetime, args=[u_id])
        scheduler.start()
        await query.message.answer(f"<b>✅Vakansiya muvaffaqiyatli yaratildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Vakansiya yaratilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)

