from aiogram.dispatcher.filters import state

class GETINFO(state.StatesGroup):
    ism = state.State()
    familiya = state.State()
    phone = state.State()
