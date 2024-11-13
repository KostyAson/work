import json
import aiogram


def add_instruction(message : aiogram.types.Message):
    instructions = json.loads(open('instructions.json').read())
    if message.text is not None:
        messaget = message.text.split('\n')
    elif message.caption is not None:
        messaget = message.caption.split('\n')
    else:
        return
    key = len(instructions) + 1
    instructions[key] = {
        'name': messaget[0],
        'text': '\n'.join(messaget[1:])
    }
    if message.document is not None:
        instructions[key]['document'] = message.document.file_id
    if message.media_group_id is not None:
        instructions[key]['media_group'] = message.media_group_id
    if message.photo is not None:
        instructions[key]['photo'] = message.photo[0].file_id
    file = open('instructions.json', 'w')
    file.write(json.dumps(instructions))
    file.close()


def make_instructions_message(admin=False):
    instructions = json.loads(open('instructions.json').read())
    message = 'Какая инструкция вас интересует?\n'
    data = 'get_instruction '
    if admin:
        message = 'Выберите инструкцию для удаления\n'
        data = 'del_instruction '
    keyboard = []
    for x in instructions:
        message += str(x) + ') ' + instructions[x]['name'] + '\n'
        keyboard.append(
            [aiogram.types.InlineKeyboardButton(text=str(x), callback_data=data + str(x))]
        )
    keyboard.append(
        [aiogram.types.InlineKeyboardButton(text='Назад', callback_data='back')]
    )
    return message, aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_instruction(id):
    instructions = json.loads(open('instructions.json').read())[id]
    return instructions


def delete_instruction(id):
    instructions = json.loads(open('instructions.json').read())
    del instructions[id]
    instructions2 = {}
    for i, x in zip(range(1, len(instructions) + 1), instructions):

        instructions2[str(i)] = instructions[x]
    file = open('instructions.json', 'w')
    file.write(json.dumps(instructions2))
    file.close()
