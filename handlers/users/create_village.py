from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.districst import district_list
from keyboards.inline.aggrement import aggre
from data.config import ADMINS
from loader import db, dp
from states.villageADD import village_add
from utils.db_api.districts import districts
@dp.message_handler(commands=["create_village"])
async def create_village(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        btn = await district_list(foo="illa")
        await message.answer(text="📌Mahalla biriktirmoqchi bo'lgan tumanni tanlang", reply_markup=btn)
        await village_add.reg_id.set()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")

######################################################################################
@dp.callback_query_handler(lambda c: "illa" in c.data, state=village_add.reg_id)
async def get_reg_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    reg_id = query.data.split("_")[-1]
    await state.update_data(
        {"reg_id": reg_id}
    )
    await query.message.answer(f"Mahalla nomini yuboring")
    await village_add.name.set()
    await query.message.delete()
    await query.answer(cache_time=60)
######################################################################################
@dp.message_handler(state=village_add.name)
async def get_village(message: types.Message, state: FSMContext):
    village_name = message.text.capitalize()
    await state.update_data(
        {"village_name": village_name}
    )
    data = await state.get_data()
    reg_id = data["reg_id"]
    village_name = data["village_name"]
    district = districts[int(reg_id)]

    res = f"<b>{district} tumaniga {village_name} qo'shilsinmi</b>"
    btn = await aggre(foo="v_aggre")
    await message.answer(text=res, reply_markup=btn)
    await village_add.aggre.set()
######################################################################################
@dp.callback_query_handler(lambda c: "v_aggre" in c.data, state=village_add.aggre)
async def get_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        reg_id = data["reg_id"]
        village_name = data["village_name"]
        district = districts[int(reg_id)]
        db.add_village(village_name=village_name, reg_id=reg_id)
        await query.message.answer(f"<b>✅Mahalla muvaffaqiyatli yaratildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Mahalla yaratilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)



