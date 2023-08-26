from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def edit(foo:str):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="❌O'chirish", callback_data=f"delete_{foo}"))
    markup.insert(InlineKeyboardButton(text="✏️Tahrirlash", callback_data=f"change_{foo}"))
    return markup