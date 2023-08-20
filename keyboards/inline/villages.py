from loader import db

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
async def village_list(foo: str, reg_id: str):
    villages = db.select_village(reg_id=reg_id)
    btn = InlineKeyboardMarkup(row_width=2)
    for village_id, village_name in villages:
        btn.insert(
            InlineKeyboardButton(text=village_name, callback_data=f"{foo}_{village_id}")
        )
    return btn