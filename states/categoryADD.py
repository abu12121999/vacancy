from aiogram.dispatcher.filters import state

class category_add(state.StatesGroup):
    name = state.State()
    aggre = state.State()

