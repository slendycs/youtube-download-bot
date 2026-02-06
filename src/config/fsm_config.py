from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    link_waiting = State()
    resolution_choice = State()
    