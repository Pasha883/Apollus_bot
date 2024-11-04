from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()


class Muting(StatesGroup):
    user = State()
    time = State()
    reason = State()


class AddingDZ(StatesGroup):
    subject = State()
    text = State()


class AddingEvent(StatesGroup):
    event_type = State()
    subject = State()
    is_this_month = State()
    date = State()