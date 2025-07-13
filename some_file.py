from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F
from random import randint

Bot_Token = '8043113226:AAF9OOKb947Tydxy4mERYH1fUkygRqWRPmI'

bot = Bot(Bot_Token)
dp = Dispatcher()

user = {
    'in_game': False,
    'secret_num': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}

def get_random_num() -> int:
    return randint(1,100)


ATTEMPTS = 5

@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )

@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(
        'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )

@dp.message(Command(commands='stat'))
async def stat_command(message: Message):
    await message.answer(
         f'Всего игр сыграно: {user["total_games"]}\n'
        f'Игр выиграно: {user["wins"]}'
    )

@dp.message(Command(commands='cancel'))
async def cancel_command(message: Message):
    if user['in_game'] == True:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом')
    else: 
        await message.answer(
            'Вы итак не играете \n'
            'А может вы хотите?')


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть'])) 
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['attempts'] = ATTEMPTS
        user['secret_num'] = get_random_num()
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_num']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer('Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?')
            
        elif int(message.text) > user['secret_num']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')

        elif int(message.text) < user['secret_num']:
            user['attempts'] -= 1
            await message.answer('Мое число больше')
        
        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] +=1
            await message.answer('К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_num"]}\n\nДавайте '
                'сыграем еще?')
    else: 
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def other_answer(message: Message):
    if user['in_game']:
        await message.reply('Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)