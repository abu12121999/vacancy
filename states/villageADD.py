from aiogram.dispatcher.filters import state

class village_add(state.StatesGroup):
    reg_id = state.State()
    name = state.State()
    aggre = state.State()

