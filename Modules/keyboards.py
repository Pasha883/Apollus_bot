from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.requests import get_users

control_panel_text = 'Панель управления v1.2'

creator_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Расписание')],
    [KeyboardButton(text='Админ панель')],
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Статистика')]],
    resize_keyboard=True,
    input_field_placeholder=control_panel_text)

admin_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Расписание')],
    [KeyboardButton(text='Админ панель')],
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Статистика')]],
    resize_keyboard=True,
    input_field_placeholder=control_panel_text)

editor_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Расписание')],
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Статистика')]],
    resize_keyboard=True,
    input_field_placeholder=control_panel_text)

user_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Расписание')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
    resize_keyboard=True,
    input_field_placeholder=control_panel_text)

banned_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Расписание')],
    [KeyboardButton(text='Запросить амнистию')],
    [KeyboardButton(text='Статистика')]],
    resize_keyboard=True,
    input_field_placeholder=control_panel_text)

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Замутить пользователя', callback_data='mute')],
    [InlineKeyboardButton(text='Размутить пользователя', callback_data='unmute')],
    [InlineKeyboardButton(text='Забанить пользователя', callback_data='ban')],
    [InlineKeyboardButton(text='Разбанить пользователя', callback_data='unban')],
    [InlineKeyboardButton(text='Добавить админа', callback_data='admin_add')],
    [InlineKeyboardButton(text='Удалить админа', callback_data='admin_remove')],
    [InlineKeyboardButton(text='Добавить редактора', callback_data='editor_add')]])

events_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Контрольная работа', callback_data='ev_1')],
    [InlineKeyboardButton(text='Самостоятельная работа', callback_data='ev_2')],
    [InlineKeyboardButton(text='Тест', callback_data='ev_3')],
    [InlineKeyboardButton(text='Пятиминутка', callback_data='ev_4')],
    [InlineKeyboardButton(text='Зачёт', callback_data='ev_5')],
    [InlineKeyboardButton(text='Чтение наизусть', callback_data='ev_6')],
    [InlineKeyboardButton(text='Другое', callback_data='ev_7')]
])

subjects_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Алгебра", callback_data='subjects_choice_Алгебра')],
    [InlineKeyboardButton(text="Геометрия", callback_data='subjects_choice_Геометрия')],
    [InlineKeyboardButton(text="Статистика", callback_data='subjects_choice_Статистика')],
    [InlineKeyboardButton(text="Русский язык", callback_data='subjects_choice_Русский язык')],
    [InlineKeyboardButton(text="Литература", callback_data='subjects_choice_Литература')],
    [InlineKeyboardButton(text="Химия", callback_data='subjects_choice_Химия')],
    [InlineKeyboardButton(text="Биология", callback_data='subjects_choice_Биология')],
    [InlineKeyboardButton(text="История", callback_data='subjects_choice_История')],
    [InlineKeyboardButton(text="Обществознание", callback_data='subjects_choice_Обществознание')],
    [InlineKeyboardButton(text="ОБЖ/ОБЗР", callback_data='subjects_choice_ОБЖ/ОБЗР')],
    [InlineKeyboardButton(text="Английский язык(гр 1)", callback_data='subjects_choice_Английский язык(гр 1)')],
    [InlineKeyboardButton(text="Английский язык(гр 2)", callback_data='subjects_choice_Английский язык(гр 2)')],
    [InlineKeyboardButton(text="Информатика(гр 1)", callback_data='subjects_choice_Информатика(гр 1)')],
    [InlineKeyboardButton(text="Информатика(гр 2)", callback_data='subjects_choice_Информатика(гр 2)')],
    [InlineKeyboardButton(text="Труд(гр 1)", callback_data='subjects_choice_Труд(гр 1)')],
    [InlineKeyboardButton(text="Труд(гр 2)", callback_data='subjects_choice_Труд(гр 2)')],
    [InlineKeyboardButton(text="Физика", callback_data='subjects_choice_Физика')],
    [InlineKeyboardButton(text="География", callback_data='subjects_choice_География')],

])


async def users_list(sender_id, metadata):
    all_users = await get_users()
    user_list = InlineKeyboardBuilder()

    for user in all_users:
        if (user.id != sender_id):
            user_list.add(InlineKeyboardButton(text=user.name, callback_data=f"{metadata}{user.id}"))
    user_list.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return user_list.adjust(2).as_markup()


async def amnesty(banned_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Да', callback_data=f"user_amnesty_yes_{banned_id}"))
    keyboard.add(InlineKeyboardButton(text='Нет', callback_data=f"user_amnesty_no_{banned_id}"))
    return keyboard.as_markup()
