from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("cancel", "Amallarni bekor qilish"),
            types.BotCommand("admin", "Admin buyruqlar ro'yxati"),
        ]
    )
