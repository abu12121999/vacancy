from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.categories import category_list
from keyboards.inline.aggrement import aggre
from data.config import ADMINS
from keyboards.inline.edit import edit
from loader import db, dp
from states.change import change_category

from utils.db_api.districts import districts
@dp.message_handler(commands=["category_list"])
async def list_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        btn =await category_list(foo="edit_cat")
        await message.answer(text="Kategoriyalar ro'yxati", reply_markup=btn)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

######################################################################################
@dp.callback_query_handler(lambda c: "edit_cat" in c.data)
async def get_category_id(query: CallbackQuery,state: FSMContext):
    await query.answer()
    category_id = query.data.split("_")[-1]
    category_name = db.select_category(category_id=category_id)[0]
    btn = await edit(foo="cat")
    await query.message.answer(f"<b>ID: {category_id}, Nomi: {category_name}\n"
                               f"Amallardan birini tanlang</b>",
                               reply_markup=btn)
    await change_category.type.set()
    await state.update_data(
        category_id=category_id,
        category_name=category_name
    )

    await query.message.delete()
    await query.answer(cache_time=60)
######################################################################################
@dp.callback_query_handler(lambda c: "delete_cat" in c.data, state=change_category.type)
async def del_cat(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    category_name = data.get("category_name")
    btn = await aggre(foo="del_a_cat")
    await query.message.answer(f"{category_name} ni o'chirasizmi", reply_markup=btn)
    await change_category.aggre.set()
    await query.message.delete()
    await query.answer(cache_time=60)
##
@dp.callback_query_handler(lambda c: "del_a_cat" in c.data, state=change_category.aggre)
async def get_del_cat_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        category_id = data.get("category_id")
        db.delete_category(category_id=category_id)
        await query.message.answer(f"<b>✅Kategoriya muvaffaqiyatli o'chirildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Kategoriya o'chirilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)
####

@dp.callback_query_handler(lambda c: "change_cat" in c.data, state=change_category.type)
async def change_cat(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    category_name = data.get("category_name")
    await query.message.answer(f"{category_name} uchun yangi nom yuboring")
    await change_category.name.set()
    await query.message.delete()
    await query.answer(cache_time=60)


@dp.message_handler(state=change_category.name)
async def get_new_cat_name(message: types.Message, state: FSMContext):
    category_name = message.text.capitalize()
    data = await state.get_data()
    old_category_name = data.get("category_name")
    await state.update_data(
        {"category_name": category_name, "old": old_category_name}
    )
    res = f"<b>{old_category_name} nomi {category_name} ga o'zgartirilsinmi?</b>"
    btn = await aggre(foo="change_ag_cat")
    await message.answer(text=res, reply_markup=btn)
    await change_category.aggre.set()


######################################################################################
@dp.callback_query_handler(lambda c: "change_ag_cat" in c.data, state=change_category.aggre)
async def cahnge_cat(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        category_id = data.get("category_id")
        category_name = data.get("category_name")
        db.edit_category_name(category_id=category_id, category_name=category_name)
        db.edit_category_from_vacancy(category_name=category_name, category_old=data.get("old"))
        await query.message.answer(f"<b>✅Kategoriya nomi muvaffaqiyatli o'zgartirildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Kategoriya nomi o'zgartirilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)


