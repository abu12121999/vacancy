from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuStart = ReplyKeyboardMarkup(
    keyboard = [

        [
            KeyboardButton(text='📖 Vakansiyalar'),
            KeyboardButton(text='👤 Ma\'lumotlarim'),
        ]
    ],
    resize_keyboard=True
)

sendPhone = ReplyKeyboardMarkup(
    keyboard = [
        [
          KeyboardButton(text="📞 Raqamni ulashish",request_contact=True)
        ],
    ],
    resize_keyboard=True
)
