from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
async def aggre(foo: str):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text=f"✅ Ha", callback_data=f"{foo}_yes"))
    btn.insert(InlineKeyboardButton(text=f"❌ Yo'q", callback_data=f"{foo}_no"))
    return btn