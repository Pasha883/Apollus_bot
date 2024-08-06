from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.requests import get_users


control_panel_text = 'Панель управления v1.0'


creator_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Админ панель')],
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)


admin_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
    [KeyboardButton(text='Админ панель')],
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

editor_markup = ReplyKeyboardMarkup(keyboard=[
                                             [KeyboardButton(text='ДЗ')],
                                             [KeyboardButton(text='Добавить ДЗ')],
                                             [KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

user_markup = ReplyKeyboardMarkup(keyboard=[
                                           [KeyboardButton(text='ДЗ')],
                                           [KeyboardButton(text='Помощь'), KeyboardButton(text='Статистика')]],
                                   resize_keyboard=True,
                                   input_field_placeholder=control_panel_text)

banned_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ДЗ')],
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
    [InlineKeyboardButton(text='Алгебра', callback_data='sub_1')],
    [InlineKeyboardButton(text='Геометрия', callback_data='sub_2')],
    [InlineKeyboardButton(text='Русский язык', callback_data='sub_3')],
    [InlineKeyboardButton(text='Литература', callback_data='sub_4')],
    [InlineKeyboardButton(text='Обществознание', callback_data='sub_5')],
    [InlineKeyboardButton(text='ОБЖ', callback_data='sub_6')],
    [InlineKeyboardButton(text='Английский язык', callback_data='sub_7')],
    [InlineKeyboardButton(text='Информатика', callback_data='sub_8')],
    [InlineKeyboardButton(text='Физика', callback_data='sub_9')],
    [InlineKeyboardButton(text='Химия', callback_data='sub_10')],
    [InlineKeyboardButton(text='География', callback_data='sub_11')],
    [InlineKeyboardButton(text='История', callback_data='sub_12')],
    [InlineKeyboardButton(text='Музыка(МХК)', callback_data='sub_13')],
    [InlineKeyboardButton(text='Технология', callback_data='sub_14')],
    [InlineKeyboardButton(text='Родной язык(Родная литература)', callback_data='sub_15')],
    [InlineKeyboardButton(text='Физ-ра', callback_data='sub_16')],
])



async def users_list(sender_id, metadata):
    all_users = await get_users()
    user_list = InlineKeyboardBuilder()

    for user in all_users:
        if(user.id != sender_id ):
            user_list.add(InlineKeyboardButton(text=user.name, callback_data=f"{metadata}{user.id}"))
    user_list.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return user_list.adjust(2).as_markup()

async def amnesty(banned_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Да', callback_data=f"user_amnesty_yes_{banned_id}"))
    keyboard.add(InlineKeyboardButton(text='Нет', callback_data=f"user_amnesty_no_{banned_id}"))
    return keyboard.as_markup()

