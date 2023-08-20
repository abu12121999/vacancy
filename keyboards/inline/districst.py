from utils.db_api.districts import districts
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
async def district_list(foo: str):
    btn = InlineKeyboardMarkup(row_width=2)
    for index, district in districts.items():
        btn.insert(
            InlineKeyboardButton(text=district, callback_data=f"{foo}_{index}")
        )
    return btn