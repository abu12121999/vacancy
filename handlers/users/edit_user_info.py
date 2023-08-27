from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.default import menu
from loader import dp, db
from states.edit_info import EDIT

@dp.message_handler(Text(equals='👤 Ma\'lumotlarim'))
async def about_user(messages: types.Message):
    try:
        user = db.select_user(telegram_id=messages.from_user.id)
        res = f"👤<b> Sizning ma'lumotlaringiz</b>\n\n\n" \
              f"👉<b>️ Ism: </b><code>{user[1]}</code>\n\n" \
              f"👉<b> Familiya: </b><code>{user[2]}</code>\n\n" \
              f"☎️<b> Telefon raqam: </b><code>{user[4]}</code>\n\n\n"
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(types.InlineKeyboardButton(text="📝Ma'lumotlarni tahrirlash",callback_data="edit_info_user"))
        await messages.answer(res, reply_markup=keyboard)
    except:
        await messages.answer(f"<b>❌Ma'lumotlar bazasidan ma'lumotlaringiz topilmadi. Iltimos /start tugmasini bosing</b>")
########################################################################################################################
@dp.callback_query_handler(text="edit_info_user")
async def edit_user_info(query: types.CallbackQuery):
    await query.answer(text="Faqatgina Ism va Familiyani o'zgartira olasiz! Bekor qilish uchun /cancel buyrug'ini yuboring", show_alert=True )
    await query.message.answer(f"<b>✏️Ismingizni kiriting</b>\n<i>Misol uchun:</i> <code>Abdulla</code>")
    await EDIT.edit_name.set()
    await query.message.delete()
    await query.answer(cache_time=60)
########################################################################################################################
#ism olish uchun handler
@dp.message_handler(state=EDIT.edit_name)
async def get_edit_name(message: types.Message, state: FSMContext):
    text = message.text.lower()
    if text == "/cancel":
        await state.finish()
        await message.answer("👇 Bosh menyu: ", reply_markup=menu.menuStart)
    else:
        name = text.capitalize()
        if (name.isalpha() or "'" in name) and len(name) >= 3:
            await state.update_data(
                {'edit_name': name}
            )
            await message.answer(f"<b>✏️Familiyangizni kiriting</b>\n<i>Misol uchun:</i> <code>Yusupov</code>")
            await EDIT.edit_surname.set()
        else:
            await message.answer(f"❌{name}<b> ism xato kiritildi.\n\n"
                                 f"✏️Ismingizni qaytadan kiriting</b>\n<i>Misol uchun:</i> <code>Abdulla</code>")
            await EDIT.edit_name.set()
########################################################################################################################
#familiya olish uchun handler
@dp.message_handler(state=EDIT.edit_surname)
async def get_edit_surname(message: types.Message, state: FSMContext):
    text = message.text.lower()
    if text == "/cancel":
        await state.finish()
        await message.answer("👇 Bosh menyu: ", reply_markup=menu.menuStart)
    else:
        surname = text.capitalize()
        tg_id = message.from_user.id

        if (surname.isalpha() or "'" in surname) and len(surname) >= 5 and (surname.endswith('va') or surname.endswith('v')):
            await state.update_data(
                {'edit_surname': surname}
            )
            #state dan o'qish
            data = await state.get_data()
            edited_name = data.get('edit_name')
            edited_surname = data.get('edit_surname')
            #databasega update qilsih
            db.edit_user_info(first_name=edited_name, last_name=edited_surname, telegram_id=tg_id)
            await message.answer(f"<b>✅Ma'lumotlaringiz muvaffaqiyatli o'zgartirildi</b>")
            await state.finish()
        else:
            await message.answer(f"❌{surname}<b> familiya xato kiritildi.\n\n"
                                 f"✏️Familiyangizni qaytadan kiriting</b>\n<i>Misol uchun:</i> <code>Yusupov</code>")
            await EDIT.edit_surname.set()



