from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.requests import get_users


control_panel_text = 'Панель управления v0.3'


creator_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Админ панель'), KeyboardButton(text='Панель управления ботом')],
    [KeyboardButton(text='Добавить ДЗ'), KeyboardButton(text='Добавить КР/Тест/Зачёт')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)


admin_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Админ панель')],
    [KeyboardButton(text='Добавить ДЗ'), KeyboardButton(text='Добавить КР/Тест/Зачёт')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

editor_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить ДЗ')],
                                             [KeyboardButton(text='Добавить КР/Тест/Зачёт')],
                                             [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

user_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

banned_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Запросить амнистию')],
    [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Замутить пользователя', callback_data='mute')],
    [InlineKeyboardButton(text='Размутить пользователя', callback_data='unmute')],
    [InlineKeyboardButton(text='Забанить пользователя', callback_data='ban')],
    [InlineKeyboardButton(text='Разбанить пользователя', callback_data='unban')],
    [InlineKeyboardButton(text='Кикнуть пользователя', callback_data='kick')],
    [InlineKeyboardButton(text='Добавить админа', callback_data='admin_add')],
    [InlineKeyboardButton(text='Удалить админа', callback_data='admin_remove')]])



async def users_list(sender_id, metadata):
    all_users = await get_users()
    user_list = InlineKeyboardBuilder()

    for user in all_users:
        if(user.id != sender_id):
            user_list.add(InlineKeyboardButton(text=user.name, callback_data=f"{metadata}{user.id}"))
    user_list.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return user_list.adjust(2).as_markup()

async def amnesty(banned_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Да', callback_data=f"user_amnesty_yes_{banned_id}"))
    keyboard.add(InlineKeyboardButton(text='Нет', callback_data=f"user_amnesty_no_{banned_id}"))
    return keyboard.as_markup()

