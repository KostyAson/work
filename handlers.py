import aiogram
import aiogram.fsm
import aiogram.fsm.context
import aiogram.fsm.state
import answers
import keyboards
import states
import datetime as dt
import utils

router = aiogram.Router()


admins = [
    1294019160,
    761247611,
    392092274
]


@router.message(aiogram.F.text == '/start')
async def start(message : aiogram.types.Message):
    await message.answer(
        text=answers.start,
        reply_markup=keyboards.start_keyboard
    )


@router.callback_query(aiogram.F.data == 'support')
async def support_chat(callback : aiogram.types.CallbackQuery, state : aiogram.fsm.context.FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=answers.support_start,
        reply_markup=keyboards.exit_chat_keyboard
    )
    await state.set_state(states.SupportState.messaging)


@router.callback_query(aiogram.F.data == 'errors')
async def error_chat(callback : aiogram.types.CallbackQuery, state : aiogram.fsm.context.FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=answers.errors,
        reply_markup=keyboards.exit_chat_keyboard
    )
    await state.set_state(states.ErrorState.messaging)


@router.callback_query(aiogram.F.data == 'instructions')
async def choose_instruction(callback : aiogram.types.CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    text, keyboard = utils.make_instructions_message()
    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(aiogram.F.data.split()[0] == 'get_instruction')
async def get_instructions(callback : aiogram.types.CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    instruction = utils.get_instruction(callback.data.split()[1])
    if 'document' in instruction:
        await callback.message.answer_document(document=instruction['document'], caption=instruction['text'])
    elif 'photo' in instruction:
        await callback.message.answer_photo(photo=instruction['photo'], caption=instruction['text'])
    elif 'media_group' in instruction:
        await callback.message.answer_media_group(media=instruction['media_group'], caption=instruction['text'])
    elif 'video' in instruction:
        await callback.message.answer_video(video=instruction['video'], caption=instruction['text'])
    else:
        await callback.message.answer(text=instruction['text'])
    await callback.message.answer(
        text='Главное меню',
        reply_markup=keyboards.start_keyboard
    )


@router.callback_query(aiogram.F.data.split()[0] == 'del_instruction')
async def del_instruction(callback : aiogram.types.CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    utils.delete_instruction(callback.data.split()[1])
    await callback.message.answer('Инструкция удалена')


@router.message(states.SupportState.messaging)
async def support(message : aiogram.types.Message, bot : aiogram.Bot, state : aiogram.fsm.context.FSMContext):
    if message.text == 'Выйти из чата':
        await state.set_state(None)
        await message.answer(
            text='Вы вышли из чата',
            reply_markup=aiogram.types.ReplyKeyboardRemove()
        )
        await message.answer(
            text='Главное меню',
            reply_markup=keyboards.start_keyboard
        )
        return
    user = 'id: ' + str(message.from_user.id)
    if message.from_user.username is not None:
        user += '\n@' + message.from_user.username
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text=f'Сообщение от пользователя\n{user}\nТип обращения: сотрудник тех поддержки\n\n' + message.text
        )
    date = dt.datetime.now()
    if dt.time(hour=9) <= date.time() <= dt.time(hour=18):
        await message.answer(answers.send_message, reply_markup=keyboards.exit_chat_keyboard)
    else:
        await message.answer(answers.send_message_error, reply_markup=keyboards.exit_chat_keyboard)


@router.message(states.ErrorState.messaging)
async def error(message : aiogram.types.Message, bot : aiogram.Bot, state : aiogram.fsm.context.FSMContext):
    if message.text == 'Выйти из чата':
        await state.set_state(None)
        await message.answer(
            text='/start',
            reply_markup=aiogram.types.ReplyKeyboardRemove()
        )
        await message.answer(
            text='Главное меню',
            reply_markup=keyboards.start_keyboard
        )
        return
    user = 'id: ' + str(message.from_user.id)
    if message.from_user.username is not None:
        user += '\n@' + message.from_user.username
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text=f'Сообщение от пользователя {user}\nТип обращения: Неполная комплектация/повреждения\n\n' + message.text
        )
    date = dt.datetime.now()
    if dt.time(hour=9) <= date.time() <= dt.time(hour=18):
        await message.answer(answers.send_message, reply_markup=keyboards.exit_chat_keyboard)
    else:
        await message.answer(answers.send_message_error, reply_markup=keyboards.exit_chat_keyboard)


@router.message(states.AddInstructionState.add)
async def add_instruction(message : aiogram.types.Message, state : aiogram.fsm.context.FSMContext):
    utils.add_instruction(message)
    await state.set_state(None)
    await message.answer('Инструкция добавлена')


@router.message(aiogram.F.text == '/admin')
async def admin_panel(message : aiogram.types.Message):
    if message.from_user.id in admins:
        await message.answer(
            text='Выберите действие',
            reply_markup=keyboards.admin_panel
        )


@router.callback_query(aiogram.F.data == 'add')
async def add(callback : aiogram.types.CallbackQuery, state : aiogram.fsm.context.FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text='Отправьте новую инстуркцию в формате:\nпервая строка - название инструкции\nвсе последующие строки - сама инструкция'
    )
    await state.set_state(states.AddInstructionState.add)


@router.callback_query(aiogram.F.data == 'del')
async def delete(callback : aiogram.types.CallbackQuery, state : aiogram.fsm.context.FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    text, keyboard = utils.make_instructions_message(True)
    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(aiogram.F.data == 'back')
async def back(callback : aiogram.types.CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text='Главное меню',
        reply_markup=keyboards.start_keyboard
    )


@router.message()
async def admin_answer(message : aiogram.types.Message, bot : aiogram.Bot):
    if message.from_user.id in admins and message.reply_to_message is not None:
        id = int(message.reply_to_message.text.split('\n')[1].split()[1])
        await bot.send_message(id, message.text)
