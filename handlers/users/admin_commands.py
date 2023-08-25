from data.config import ADMINS
from loader import dp
from aiogram import types
@dp.message_handler(commands=["admin"])
async def create_category(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        res = f"<b>Admin buyruqlari:</b>\n\n" \
              f"<b>/create_category</b> - Vakansiya uchun kategoriya yaratish\n\n" \
              f"<b>/create_vacancy</b> - Vakansiya yaratish\n\n" \
              f"<b>/create_village</b> - Tumanga mahalla yaratib qo'shish\n\n" \
              f"<b>/active_vacancy</b> - Aktiv vakansiyalar\n\n" \
              f"<b>/passive_vacancy</b> - Muddati o'tgan vakansiyalar\n\n" \
              f"<b>/numbers_of_members</b> - Bot a'zolari soni\n\n" \


        await message.answer(res)
    else:
        await message.answer(f"⚠️Bu buyruq faqat adminlar uchun!")
