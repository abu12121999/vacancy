from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.categories import category_list
from keyboards.inline.aggrement import aggre
from data.config import ADMINS
from loader import db, dp
from states.categoryADD import category_add

from utils.db_api.districts import districts
@dp.message_handler(commands=["create_category"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(text="Yaratmoqchi bo'lgan kategoriya nomini yuboring")
        await category_add.name.set()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

######################################################################################
@dp.message_handler(state=category_add.name)
async def get_village(message: types.Message, state: FSMContext):
    category_name = message.text.capitalize()
    await state.update_data(
        {"category_name": category_name}
    )
    res = f"<b>Kategoriyalar bo'limiga {category_name} qo'shilsinmi?</b>"
    btn = await aggre(foo="c_aggre")
    await message.answer(text=res, reply_markup=btn)
    await category_add.aggre.set()


######################################################################################
@dp.callback_query_handler(lambda c: "c_aggre" in c.data, state=category_add.aggre)
async def get_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        category_name = data["category_name"]
        db.add_category(category_name=category_name)
        await query.message.answer(f"<b>✅Kategoriya muvaffaqiyatli yaratildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Kategoriya yaratilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)



