from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def vacancy_btn(page: int, total_pages: int, id):
    markup = InlineKeyboardMarkup(row_width=2)
    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_page"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_page"))
    markup.add(InlineKeyboardButton(text="🗑O'chirish", callback_data=f"del_act"))
    markup.insert(InlineKeyboardButton(text="✏️Tahrirlash", callback_data=f"change_act"))
    markup.insert(InlineKeyboardButton(text="📋Nomzodlar ro'yxati", callback_data=f"vacants_list_{id}"))
    return markup

async def vacancy_btn_passive(page: int, total_pages: int, id):
    markup = InlineKeyboardMarkup(row_width=2)
    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_passive"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_passive"))
    markup.add(InlineKeyboardButton(text="🗑O'chirish", callback_data=f"del_pass"))
    markup.insert(InlineKeyboardButton(text="✏️Tahrirlash", callback_data=f"change_pass"))
    markup.insert(InlineKeyboardButton(text="📋Nomzodlar ro'yxati", callback_data=f"vacants_list_{id}"))
    return markup
async def vacancy_btn_nomzod(page, total_pages, vac_id):
    id = vac_id
    markup = InlineKeyboardMarkup(row_width=2)
    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"p_page_{id}"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"n_page_{id}"))

    return markup

async def vacancy_btn_user(page: int, total_pages: int, vac_id):
    markup = InlineKeyboardMarkup(row_width=2)

    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_user"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_user"))
    markup.add(InlineKeyboardButton(text="🔺Qiziqish bildirish🔻", callback_data=f"interest_user_{vac_id}"))

    return markup
async def vacancy_btn_interest(page: int, total_pages: int):
    markup = InlineKeyboardMarkup(row_width=2)

    if page > 1:
        markup.insert(InlineKeyboardButton(text="⬅️ Ortga", callback_data="prev_user_interest"))
    if page < total_pages:
        markup.insert(InlineKeyboardButton(text="Keyingi ➡️", callback_data="next_user_interest"))

    return markup
