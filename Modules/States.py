from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Register(StatesGroup):
    name = State()

class Muting(StatesGroup):
    user = State()
    time = State()
    reason = State()