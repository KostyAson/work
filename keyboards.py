import aiogram


start_keyboard = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            aiogram.types.InlineKeyboardButton(
                text='Служба поддержки ⚙️',
                callback_data='support'
            )
        ],
        [
            aiogram.types.InlineKeyboardButton(
                text='Неполная комплектация/повреждения❓',
                callback_data='errors'
            )
        ],
        [
            aiogram.types.InlineKeyboardButton(
                text='Инструкции 📄',
                callback_data='instructions'
            )
        ],
    ]
)

exit_chat_keyboard = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text='Выйти из чата')]
    ],
    resize_keyboard=True
)

admin_panel = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            aiogram.types.InlineKeyboardButton(
                text='Удалить инструкцию',
                callback_data='del'
            )
        ],
        [
            aiogram.types.InlineKeyboardButton(
                text='Добавить инструкцию',
                callback_data='add'
            )
        ]
    ]
)