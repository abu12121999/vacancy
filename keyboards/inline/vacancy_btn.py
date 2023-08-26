from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def vacancy_btn(page: int, total_pages: int):
    markup = InlineKeyboardMarkup(row_width=4)
    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_page"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_page"))
    return markup

async def vacancy_btn_passive(page: int, total_pages: int):
    markup = InlineKeyboardMarkup(row_width=4)
    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_passive"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_passive"))
    return markup
