from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp
from aiogram.dispatcher.filters import Text

@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer("<b>Amaliyot bekor qilindi</b>")
    await state.finish()