from aiogram.fsm.state import State, StatesGroup


class Add_next_message(StatesGroup):
    mes = State()


class Delete_next_message(StatesGroup):
    mes = State()