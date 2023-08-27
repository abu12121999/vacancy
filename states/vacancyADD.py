from aiogram.dispatcher.filters import state

class vacancy_add(state.StatesGroup):
    location1 = state.State()
    location2 = state.State()
    category = state.State()
    name = state.State()
    salary = state.State()
    description = state.State()
    file = state.State()
    deadline = state.State()
    rozi = state.State()

class vacancy_edit(state.StatesGroup):
    category = state.State()
    name = state.State()
    salary = state.State()
    description = state.State()
    file = state.State()
    deadline = state.State()
    rozi = state.State()


