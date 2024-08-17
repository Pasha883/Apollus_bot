import random
from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.client import bot
from aiogram.types import Message, CallbackQuery, ChatMemberAdministrator,  FSInputFile
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

import Modules.keyboards as kb
import Modules.States as st
import Database.requests as rq

router = Router()


dz_text = 'Дз не установлено'
dz_photo_list = list()
stable_build_date = '16.08.2024 15:25'

#Отлавливание команд
@router.message(CommandStart())
async def cmd_start(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Banned'):
            await message.reply('Выберите пункт меню:', reply_markup=kb.banned_markup)
        if (user.rights == 'User'):
            await message.reply('Выберите пункт меню:', reply_markup=kb.user_markup)
        if (user.rights == 'Editor'):
            await message.reply('Выберите пункт меню:', reply_markup=kb.editor_markup)
        if (user.rights == 'Admin'):
            await message.reply('Выберите пункт меню:', reply_markup=kb.admin_markup)
        if (user.rights == 'Creator'):
            await message.reply('Выберите пункт меню:', reply_markup=kb.creator_markup)
    else:
        await message.answer("Пожалуйста, зарегистрируйтесь")


@router.message(Command('register'))
async def cmd_register(message: Message, state: FSMContext):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        await message.reply('Вы уже зарегистрированы')
    else:
        await state.set_state(st.Register.name)
        await message.reply('Введите Ваше имя')


@router.message(Command('give_op'))
async def cmd_register(message: Message, state: FSMContext):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Creator'):
            await message.bot.promote_chat_member(message.chat.id, message.from_user.id, False, True,
                                                  True, True, True,
                                                  True, True,
                                                  True, True,
                                                  True, True)
            
            await message.reply('Успешно')
        else:
            await message.reply('Ошибка запроса права доступа')
    else:
        await state.set_state(st.Register.name)
        await message.reply('Введите Ваше имя')


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer('Apollus Bot v1.09\nLast stable build date: ' + stable_build_date +
                         '\nVersion comments: Added command /users')


@router.message(Command('users'))
async def cmd_users(message: Message, state: FSMContext):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Creator'):
            text = 'Зарегистрированные пользователи:\n'
            all_users = await rq.get_users()

            for user in all_users:
                text += '•'
                text += str(user.name)
                text += '\n'

            await message.reply(text)
        else:
            await message.reply('Ошибка запроса права доступа')
    else:
        await state.set_state(st.Register.name)
        await message.reply('Введите Ваше имя')


#Отлавливание состояний
@router.message(st.Register.name)
async def register_name(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = bot.GetChatMember(chat_id=message.chat.id, user_id=message.from_user.id)
    name = message.text
    user = await message.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    status = ''

    if isinstance(user, ChatMemberAdministrator):
        status = 'Admin'
    else:
        status = 'User'

    await rq.register(user_id, name, status)
    await message.reply('Успешная регистрация. Добро пожаловать ' + name + '!')
    await state.clear()


@router.message(st.Muting.time)
async def muting_time(message: Message, state: FSMContext):
    time = message.text

    if time.isnumeric():
        await state.update_data(time=int(time))

        await state.set_state(st.Muting.reason)

        await message.reply('Укажите причину мута')
    else:
        await message.reply('Некоректное значение, попробуйте снова')

@router.message(st.Muting.reason)
async def muting_reason(message: Message, state: FSMContext):
    reason = message.text
    user = await rq.set_user(message.from_user.id)
    sender_name = user.name

    await state.update_data(reason=reason)

    data = await state.get_data()

    delta_time = int(data['time'])
    user_id = int(data['user'])

    user2 = await rq.set_user(user_id)

    dt = datetime.now() + timedelta(minutes=delta_time)
    timestamp = dt.timestamp()

    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                           permissions=types.ChatPermissions(can_send_messages=False),
                                           until_date=int(timestamp))

    await message.reply('Пользователь замучен на ' + str(delta_time) + ' минут по причине ' + str(data['reason']))

    try:
        await message.bot.send_message(chat_id=user_id, text='Уважаемый ' + user2.name +
                                       ', Вы были замучены администратором ' + sender_name + ' на ' + str(delta_time) +
                                       ' минут ' + ' по причине ' + str(data['reason']))
    except:
        print('Can t send message to user')

    await state.clear()


@router.message(st.AddingDZ.text)
async def adding_dz(message: Message, state: FSMContext):
    global dz_photo_list
    dz_photo_list.clear()
    if message.photo:
        file_name = f"Photo/{message.photo[-1].file_id}.jpg"
        await message.bot.download(message.photo[-1], destination=file_name)
        dz_photo_list.append(file_name)
        await message.reply('Фото сохранено')
    else:
        global dz_text
        dz_text = message.text
        await message.reply('ДЗ сохранено')

    await state.clear()




#Отлавливание reply buttons
@router.message(F.text == 'Статистика')
async def btn_stats(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        await message.reply('Ваше имя: ' + str(user.name) + '\n' +
                            'Ваши права: ' + str(user.rights) + '\n' +
                            'Ваши сообщения: ' + str(user.messages) + '\n')
    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'Админ панель')
async def btn_admin_panel(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await message.reply('Админ панель v1.0', reply_markup=kb.admin_panel)
        else:
            await message.reply('У вас нет прав')

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'Запросить амнистию')
async def btn_unban_trying(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Banned'):
            users = await rq.get_users()

            admins = list()

            for userr in users:
                if userr.rights == 'Admin' or userr.rights == 'Creator':
                    admins.append(userr)

            user2 = random.choice(admins)
            print(user2.name)

            await message.reply(user.name + ', Ваше дело было отправлено администратору')

            try:
                await message.bot.send_message(user2.id,  user.name + ' запросил у Вас амнистию. '
                                                                      'Вы готовы его разбанить?',
                                               reply_markup=await kb.amnesty(user.id))
            except:
                print('Can t send message to user')
        else:
            await message.reply('Вы не забанены')

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'Добавить ДЗ')
async def btn_add_dz(message: Message, state: FSMContext):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator' or user.rights == 'Editor'):
            await message.reply('Отправьте текст или изображение')
            await state.set_state(st.AddingDZ.text)
        else:
            await message.reply('У вас нет прав, запросите права у админа')

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'ДЗ')
async def btn_dz(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        if dz_photo_list:
            for photo in dz_photo_list:
                picture = FSInputFile(photo)
                await message.bot.send_photo(message.chat.id, picture)
        else:
            await message.reply(dz_text)

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'Сколько осталось до 1 сентября?')
async def btn_que(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        if(datetime.now() < datetime(2024, 9, 1)):
            td = datetime(2024, 9, 1) - datetime.now()
            await message.reply(str(td.days) + ' дней')
        else:
            await message.reply('Баран, первое сентября уже наступило. Выходи из спячки и иди в школу!')

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')


@router.message(F.text == 'Добавить КР/Тест/Зачёт')
async def btn_events(message: Message, state: FSMContext):
    is_user = await rq.in_database(message.from_user.id)

    if (is_user):
        user = await rq.set_user(message.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator' or user.rights == 'Editor'):
            await message.reply('Выберите тип события:')

        else:
            await message.reply('У вас нет прав, запросите права у админа')

    else:
        await message.reply('Пожалуйста, зарегистрируйтесь')



#Отлавливание callback query

@router.callback_query(F.data == 'admin_add')
async def admin_add_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для назначения:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_admin_add_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'admin_remove')
async def admin_remove_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для снятия:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_admin_remove_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'mute')
async def mute_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для мута:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_mute_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'unmute')
async def unmute_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для размута:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_unmute_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'ban')
async def ban_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для бана:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_ban_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'unban')
async def unban_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для разбана:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_unban_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data == 'back')
async def back_handler(query: CallbackQuery):
    await query.answer()
    await query.message.reply('Админ панель v1.0', reply_markup=kb.admin_panel)

@router.callback_query(F.data == 'editor_add')
async def editor_add_handler(query: CallbackQuery):
    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        user = await rq.set_user(query.from_user.id)

        if (user.rights == 'Admin' or user.rights == 'Creator'):
            await query.answer()
            await query.message.reply('Выберите пользователя для повышения:',
                                      reply_markup=await kb.users_list(query.from_user.id, "user_editor_add_"))
        else:
            await query.answer('У вас нет прав!', show_alert=True)

    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_mute_'))
async def mute_handler(query: CallbackQuery, state: FSMContext):
    user_id = query.data.split('_')[2]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator'):
            if (user.rights != 'Admin' or user.rights == 'Creator'):
                await query.answer()

                await state.set_state(st.Muting.user)
                await state.update_data(user=user_id)

                await state.set_state(st.Muting.time)

                await query.message.reply('Введите время мута в минутах')
            else:
                await query.answer('Нельзя замутить администратора')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_unmute_'))
async def unmute_handler(query: CallbackQuery):
    user_id = query.data.split('_')[2]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator'):
            if (user.rights != 'Admin' or user.rights == 'Creator'):
                await query.bot.restrict_chat_member(chat_id=query.message.chat.id, user_id=int(user_id),
                                                     permissions=types.ChatPermissions(can_send_messages=True,
                                                                                       can_send_media_messages=True,
                                                                                       can_send_other_messages=True,
                                                                                       can_send_polls=True,
                                                                                       can_add_reactions=True,
                                                                                       can_send_photos=True,
                                                                                       can_send_audios=True,
                                                                                       can_send_documents=True,
                                                                                       can_send_videos=True,
                                                                                       can_send_video_notes=True,
                                                                                       can_send_voice_notes=True,
                                                                                       can_add_web_page_previews=True))
                await query.answer('Пользователь ' + name + ' размучен')
                await query.message.reply('Пользователь ' + name + ' размучен')
            else:
                await query.answer('Нельзя замутить администратора')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_ban_'))
async def ban_handler(query: CallbackQuery):
    user_id = query.data.split('_')[2]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if ((sender.rights == 'Admin' or sender.rights == 'Creator') & user.rights != 'Creator'):
            await rq.set_rights(user_id, 'Banned')
            await query.answer('Пользователь ' + name + ' забанен')
            await query.message.reply('Пользователь ' + name + ' забанен')

            try:
                await query.bot.send_message(user_id, 'Уважаемый ' + name +
                                             ', Вы были забанены администратором ' + sender.name +
                                             'Вы можете попытаться обжаловать бан, нажав на кнопку "Запросить амнистию"'
                                             ' (чтобы обновить меню введите команду /start)')
            except:
                print('Can t send message to user')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_unban_'))
async def unban_handler(query: CallbackQuery):
    user_id = query.data.split('_')[2]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if ((sender.rights == 'Admin' or sender.rights == 'Creator') & user.rights != 'Creator'):
            await rq.set_rights(user_id, 'User')
            await query.answer('Пользователь ' + name + ' разбанен')
            await query.message.reply('Пользователь ' + name + ' разбанен')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_amnesty_no_'))
async def amnesty_no_handler(query: CallbackQuery):
    user_id = query.data.split('_')[3]
    user = await rq.set_user(user_id)
    name = user.name

    await query.answer()

    try:
        await query.bot.send_message(user_id, 'К сожалению, администратор отклонил вашу заявку')
    except:
        print('Can t send message to user')


@router.callback_query(F.data.startswith('user_amnesty_yes_'))
async def amnesty_yes_handler(query: CallbackQuery):
    user_id = query.data.split('_')[3]
    user = await rq.set_user(user_id)
    name = user.name

    await query.answer('Пользователь ' + name + ' разбанен')
    await rq.set_rights(user_id, 'User')

    try:
        await query.bot.send_message(user_id, 'Ваша заявка одобрена')
    except:
        print('Can t send message to user')


@router.callback_query(F.data.startswith('user_admin_add'))
async def admin_add_handler(query: CallbackQuery):
    user_id = query.data.split('_')[3]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator' and user.rights != 'Creator'):
            try:
                await query.answer('Пользователь назначен администратором')
                await rq.set_rights(user_id, 'Admin')

                await query.message.reply('Пользователь ' + user.name + ' назначен администратором')
            except:
                await query.answer('Ошибка')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_editor_add'))
async def editor_add_handler(query: CallbackQuery):
    user_id = query.data.split('_')[3]
    user = await rq.set_user(user_id)

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator' and user.rights != 'Creator'):
            try:
                await query.answer('Пользователь назначен редактором')
                await rq.set_rights(user_id, 'Editor')

                await query.message.reply('Пользователь ' + user.name + ' назначен редактором')
            except:
                await query.answer('Ошибка')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('user_admin_remove'))
async def admin_remove_handler(query: CallbackQuery):
    user_id = query.data.split('_')[3]
    user = await rq.set_user(user_id)
    name = user.name

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator' and user.rights != 'Creator'):
            try:
                await query.answer('Пользователь ' + user.name + ' больше не администратор')
                await rq.set_rights(user_id, 'User')

                await query.message.reply('Пользователь больше не администратор')
            except:
                await query.answer('Ошибка')
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('ev_'))
async def ev_handler(query: CallbackQuery, state: FSMContext):
    event_id = query.data.split('_')[1]

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator' or sender.rights == 'Editor'):
            await state.set_state(st.AddingEvent.event_type)
            if(event_id == '1'):
                await state.update_data(event_type='Контрольная работа')
            if (event_id == '2'):
                await state.update_data(event_type='Самостоятельная работа')
            if (event_id == '3'):
                await state.update_data(event_type='Тест')
            if (event_id == '4'):
                await state.update_data(event_type='Пятиминутка')
            if (event_id == '5'):
                await state.update_data(event_type='Зачёт')
            if (event_id == '6'):
                await state.update_data(event_type='Чтение наизусть')
            if (event_id == '7'):
                await state.update_data(event_type='Другое')

            await state.set_state(st.AddingEvent.subject)
            await query.message.reply('Выберите предмет:', reply_markup=kb.subjects_markup)
            await query.answer()
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)


@router.callback_query(F.data.startswith('sub_'))
async def sub_handler(query: CallbackQuery, state: FSMContext):
    event_id = query.data.split('_')[1]

    is_user = await rq.in_database(query.from_user.id)

    if (is_user):
        sender = await rq.set_user(query.from_user.id)
        if (sender.rights == 'Admin' or sender.rights == 'Creator' or sender.rights == 'Editor'):
            if(event_id == '1'):
                await state.update_data(subject='Алгебра')
            if (event_id == '2'):
                await state.update_data(subject='Геометрия')
            if (event_id == '4'):
                await state.update_data(subject='Русский язык')
            if (event_id == '5'):
                await state.update_data(subject='Литература')
            if (event_id == '6'):
                await state.update_data(subject='Обществознание')
            if (event_id == '7'):
                await state.update_data(subject='ОБЖ')
            if (event_id == '8'):
                await state.update_data(subject='Английский язык')
            if (event_id == '9'):
                await state.update_data(subject='Информатика')
            if (event_id == '10'):
                await state.update_data(subject='Физика')



            await state.set_state(st.AddingEvent.subject)
            await query.message.reply('Выберите предмет:', reply_markup=kb.subjects_markup)
            await query.answer()
        else:
            await query.answer('У вас нет прав!', show_alert=True)
    else:
        await query.answer('Пожалуйста, зарегистрируйтесь', show_alert=True)

#Все сообщения(кроме команд)
@router.message()
async def all_mess(message: Message):
    is_user = await rq.in_database(message.from_user.id)

    user_id = message.from_user.id
    message_id = message.message_id

    if (not is_user):
        await message.bot.delete_message(message.chat.id, message_id)
        try:
            await message.bot.send_message(user_id, 'Для продолжения общения, зарегистрируйтесь. Для этого введите'
                                                    ' команду /register и следуйте инструкциям.')
        except:
            print('Can t send message to user')

    else:
        user = await rq.set_user(user_id)
        if (user.rights != 'Banned'):
            await rq.messages_counter_update(user_id)
        else:
            await message.bot.delete_message(message.chat.id, message_id)
