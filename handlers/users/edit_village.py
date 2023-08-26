from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.categories import category_list
from keyboards.inline.aggrement import aggre
from data.config import ADMINS
from keyboards.inline.districst import district_list
from keyboards.inline.edit import edit
from keyboards.inline.villages import village_list
from loader import db, dp
from states.change import change_villa

from utils.db_api.districts import districts
@dp.message_handler(commands=["village_list"])
async def create_vacancy(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        btn = await district_list(foo="chvv")
        await message.answer(text="📌 Qaysi tuman mahallasini ko'rmoqchisiz", reply_markup=btn)
        await change_villa.reg.set()
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
##
@dp.callback_query_handler(lambda c: "chvv" in c.data, state=change_villa.reg)
async def get_regg_id(query: CallbackQuery, state: FSMContext):
    await query.answer()
    location1 = query.data.split("_")[-1]
    await state.update_data(
        {"tuman": districts[int(location1)]}
    )
    btn = await village_list(foo="chanvil", reg_id=location1)
    if btn["inline_keyboard"]:
        await query.message.answer(f"Mahallani tanlang", reply_markup=btn)
        await change_villa.vil.set()
        await query.message.delete()
        await query.answer(cache_time=60)
    else:
        await query.message.answer("Keltirilgan tumanga mahalla biriktirilmagan iltimos mahalla biriktirib keyin urunib ko'ring")
        await state.finish()
        await query.message.delete()
        await query.answer(cache_time=60)


######################################################################################
@dp.callback_query_handler(lambda c: "chanvil" in c.data, state=change_villa.vil)
async def get_category_id(query: CallbackQuery,state: FSMContext):
    await query.answer()
    village_id = query.data.split("_")[-1]
    old_village_name = db.get_village_name(village_id=village_id)[0]
    btn = await edit(foo="vil")
    await query.message.answer(f"<b>Nomi: {old_village_name}\n"
                               f"Amallardan birini tanlang</b>",
                               reply_markup=btn)
    await change_villa.type.set()
    await state.update_data(
        old_name=old_village_name,
        village_id=village_id
    )

    await query.message.delete()
    await query.answer(cache_time=60)
######################################################################################
@dp.callback_query_handler(lambda c: "delete_vil" in c.data, state=change_villa.type)
async def del_vil(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    vil_name = data.get("old_name")
    btn = await aggre(foo="delvillaa")
    await query.message.answer(f"{vil_name} ni o'chirasizmi", reply_markup=btn)
    await change_villa.aggre.set()
    await query.message.delete()
    await query.answer(cache_time=60)
##
@dp.callback_query_handler(lambda c: "delvillaa" in c.data, state=change_villa.aggre)
async def get_del_cat_aggrement(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        village_id = data.get("village_id")
        db.delete_village(village_id=village_id)
        await query.message.answer(f"<b>✅Mahalla muvaffaqiyatli o'chirildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Mahalla o'chirilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)
####

@dp.callback_query_handler(lambda c: "change_vil" in c.data, state=change_villa.type)
async def change_cat(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    v_name = data.get("old_name")
    await query.message.answer(f"{v_name} uchun yangi nom yuboring")
    await change_villa.name.set()
    await query.message.delete()
    await query.answer(cache_time=60)


@dp.message_handler(state=change_villa.name)
async def get_new_cat_name(message: types.Message, state: FSMContext):
    village_name = message.text.capitalize()
    data = await state.get_data()
    await state.update_data(
        {"village_name": village_name}
    )
    res = f"<b>{data.get('old_name')} nomi {village_name} ga o'zgartirilsinmi?</b>"
    btn = await aggre(foo="cangvil")
    await message.answer(text=res, reply_markup=btn)
    await change_villa.aggre.set()


######################################################################################
@dp.callback_query_handler(lambda c: "cangvil" in c.data, state=change_villa.aggre)
async def cahnge_cat(query: CallbackQuery, state: FSMContext):
    await query.answer()
    a = query.data.split("_")[-1]
    if a == "yes":
        data = await state.get_data()
        village_id = data.get("village_id")
        village_name = data.get("village_name")
        db.edit_village_name(village_id=village_id, village_name=village_name)
        await query.message.answer(f"<b>✅Mahalla nomi muvaffaqiyatli o'zgartirildi</b>")
        await state.finish()
    else:
        await query.message.answer(f"<b>❌Mahalla nomi o'zgartirilmadi</b>")
        await state.finish()

    await query.message.delete()
    await query.answer(cache_time=60)


