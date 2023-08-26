from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data.config import CHANNELS, ADMINS
from loader import bot, dp, db


@dp.message_handler(commands=['start'])
async def admin_start(message: types.Message):
    id = message.from_user.id
    all_tg_id = [x[0] for x in db.select_all_users()]
    if id in all_tg_id and id in ADMINS:
        await message.answer(f"Admin xush kelibsiz! Admin buyruqlar ro'yxati - /admin",
                             reply_markup=types.ReplyKeyboardRemove())
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