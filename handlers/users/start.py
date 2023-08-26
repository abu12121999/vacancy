import sqlite3
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from data.config import CHANNELS, ADMINS
from loader import bot, dp, db
from utils.misc import subscription
from keyboards.default import menu
from states.getInfo import GETINFO
from aiogram.dispatcher import FSMContext

########################################################################################################################
# start handler
@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    id = message.from_user.id
    all_tg_id = [x[0] for x in db.select_all_users()]
    if id in all_tg_id:
        if id in ADMINS:
            await message.answer("Admin xush kelibsiz! Admin buyruqlar ro'yxati /admin")
        else:
            await message.answer("👇 Bosh menyu: ", reply_markup=menu.menuStart)
    else:
        check_button = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            channel = await bot.get_chat(channel)
            invite_link = await channel.export_invite_link()
            check_button.insert(InlineKeyboardButton(text=f"{channel.title}", url=f"{invite_link}"))
        check_button.insert(InlineKeyboardButton(text="A'zo bo'ldim", callback_data="check_subs"), )
        await message.answer(f"Assalomu alaykum, {message.from_user.first_name} ! Botimizga xush kelibsiz. "
                             f"Sizni bu yerda ko'rib turganimizdan xursandmiz. Davom etish uchun"
                             f" quyidagi 👇 {len(CHANNELS)} ta kanalga "
                             f"a'zo bo'ling va <b>A'zo bo'ldim</b> tugmasini bosing",
                             reply_markup=check_button)
########################################################################################################################
# check_subs handler
@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    check_button = InlineKeyboardMarkup(row_width=1)
    status_all_done = 0
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            status_all_done += 1
            invite_link = await channel.export_invite_link()
            check_button.insert(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{invite_link}"))
        else:
            invite_link = await channel.export_invite_link()
            check_button.insert(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{invite_link}"))
    check_button.insert(InlineKeyboardButton(text="A'zo bo'ldim", callback_data="check_subs"), )

    user_id = call.from_user.id
    all_tg_id = [x[0] for x in db.select_all_users()]
    if status_all_done == len(CHANNELS):  
        if user_id in all_tg_id:
            await call.message.answer("👇 Bosh menyu: ", reply_markup=menu.menuStart)
        else:
            await call.message.answer(f"<b>✏️Ismingizni kiriting</b>\n<i>Misol uchun:</i> <code>Abbos</code>")
            await GETINFO.ism.set()
    else:
        await call.message.answer(f"❌ Kanallarga to'liq a'zo emassiz! "
                                  f"Botdan to'liq foydalanish uchun ko'rsatilgan "
                                  f"barcha kanallarga a'zo bo'ling! ",
                                  reply_markup=check_button,
                                  disable_web_page_preview=True)
    await call.message.delete()
    await call.answer(cache_time=60)
########################################################################################################################
#ism olish uchun handler
@dp.message_handler(state=GETINFO.ism)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.capitalize()

    if name.isalpha() and len(name) >= 3:
        await state.update_data(
            {'ism': name}
        )
        await message.answer(f"<b>✏️Familiyangizni kiriting</b>\n<i>Misol uchun:</i> <code>Yusupov</code>")
        await GETINFO.next()
    else:
        await message.answer(f"❌{name}<b> ism xato kiritildi.\n\n"
                             f"✏️Ismingizni qaytadan kiriting</b>\n<i>Misol uchun:</i> <code>Abdulla</code>")
        await GETINFO.ism.set()
########################################################################################################################
#familiya olish uchun handler
@dp.message_handler(state=GETINFO.familiya)
async def get_surname(message: types.Message, state: FSMContext):
    surname = message.text.capitalize()

    if surname.isalpha() and len(surname) >= 5 and (surname.endswith('va') or surname.endswith('v')):
        await state.update_data(
            {'familiya': surname}
        )
        await message.answer(f"<b>👇Pastdagi tugma orqali raqamingizni yuboring</b>", reply_markup=menu.sendPhone)
        await GETINFO.next()
    else:
        await message.answer(f"❌{surname}<b> familiya xato kiritildi.\n\n"
                             f"✏️Familiyangizni qaytadan kiriting</b>\n<i>Misol uchun:</i> <code>Yusupov</code>")
        await GETINFO.familiya.set()
########################################################################################################################
#kontakt olish uchun handler
@dp.message_handler(content_types='contact', state=GETINFO.phone)
async def get_phone(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    phone_number = message.contact["phone_number"]
    phone_user_id = message.contact["user_id"]

    if tg_id == phone_user_id:
        phone_number = message.contact["phone_number"]
        await state.update_data(
            {'tg_id': tg_id, 'phone': phone_number}
        )
        data = await state.get_data()
        telegram_id = data.get('tg_id')
        first_name = data.get('ism')
        last_name = data.get('familiya')
        phone = data.get('phone')
        username = message.from_user.username

        #check user exist
        users = db.select_all_users()
        all_tg_id = []
        for i in users:
            all_tg_id.append(i[0])

        # add user information to DB
        if telegram_id not in users:
            db.add_user(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                username=username
            )
        await state.finish()
        await message.answer(f"<b>📝Ma'lumotlaringiz qayd qilindi</b>", reply_markup=ReplyKeyboardRemove())
        await message.answer("👇 Bosh menyu: ", reply_markup=menu.menuStart)
    else:
        await message.answer(f"<b>❌Bu raqam sizning raqamingiz emas</b>\n\n"
                             f"<b>✏️Qaytadan raqamingizni yuboring</b>", reply_markup=menu.sendPhone)
        await GETINFO.phone.set()
######################################################################################################################
@dp.message_handler(content_types=types.ContentType.ANY, state=GETINFO.phone)
async def wrong_phone(message: types.Message):
    await message.answer(f"<b>👇Pastdagi tugma orqali raqamingizni yuboring</b>",reply_markup=menu.sendPhone)
    await GETINFO.phone.set()