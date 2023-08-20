import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNELS
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        final_status = True
        check_button = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            status = await subscription.check(user_id=user,channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                check_button.insert(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{invite_link}"))
        check_button.insert(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
        if not final_status:
            await update.message.answer(f"Kechirasiz siz botdan kanallarga to'liq a'zo bo'lmasdan foydalanyapsiz."
                                        f" Iltimos kannallarga a'zo bo'ling va botdan foydalanishda davom eting!",reply_markup=check_button, disable_web_page_preview=True)
            raise CancelHandler()
