from aiogram.dispatcher.filters import state

class EDIT(state.StatesGroup):
    edit_name = state.State()
    edit_surname = state.State()
    edit_phone = state.State()
