from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

async def category_list(foo: str):
    categories = db.select_all_category()
    print("categories", categories)
    btn = InlineKeyboardMarkup(row_width=3)
    for index, category in categories:
        btn.insert(
            InlineKeyboardButton(text=category, callback_data=f"{foo}_{index}")
        )
    return btn