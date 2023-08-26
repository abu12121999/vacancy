from aiogram.dispatcher.filters import state

class change_category(state.StatesGroup):
    type = state.State()
    name = state.State()
    aggre = state.State()

class change_villa(state.StatesGroup):
    reg = state.State()
    vil = state.State()
    type = state.State()
    name = state.State()
    aggre = state.State()