from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Register(StatesGroup):
    name = State()


class Muting(StatesGroup):
    user = State()
    time = State()
    reason = State()


class AddingDZ(StatesGroup):
    text = State()


class AddingEvent(StatesGroup):
    event_type = State()
    subject = State()
    is_this_month = State()
    date = State()