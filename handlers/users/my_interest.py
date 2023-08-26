
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.aggrement import aggre
from keyboards.inline.vacancy_btn import vacancy_btn, vacancy_btn_user
from loader import dp, db, bot
@dp.message_handler(Text(equals='💠Mening vakansiyalarim💠'))
async def my_interests(message: types.Message):
    vacant_id = message.from_user.id
    vacansies_id = db.select_vacant_by_id(vacant_id=vacant_id)
    vacansies = [db.select_vacancy_by_id(vacansies_id=vac_id) for vac_id in vacansies_id]

    await message.answer(vacansies)
