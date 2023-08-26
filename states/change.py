from aiogram.dispatcher.filters import state

class change_category(state.StatesGroup):
    type = state.State()
    name = state.State()
    aggre = state.State()
