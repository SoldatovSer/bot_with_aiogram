import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


BOT_TOKEN = ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

user = {
    "in game": False,
    "secret_number": None,
    "attempts": None,
    "total_games": 0,
    "wins": 0,
}


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands="start"))
async def procces_start_comman(message: Message) -> Message:
    await message.answer(
        """Привет!
Меня зовут Бот-Дюэль!
Давай сыграем в игру "Угадай число"?)
Чтобы узнать правила игры и получить список доступных команд - отправь
команду "/help"!"""
    )


@dp.message(Command(commands="help"))
async def procces_help_command(message: Message) -> Message:
    await message.answer(
        f"""Правила игры:
Я загадываю число от 1 до 100, а тебе нужно его угадать!:)
У тебя есть {ATTEMPTS} попыток.
Список доступных команд:
"/help" - правила игры
"/cancel" - выйти из игры
"/stat" - посмотреть статистику игр.
Давай сыграем?!)"""
    )


@dp.message(Command(commands="stat"))
async def process_stat_command(message: Message) -> Message:
    await message.answer(
        f"""Всего сыграно игр - {user['total_games']}
Игр выйграно - {user['wins']}"""
    )


@dp.message(Command(commands="cancel"))
async def process_cancel_command(message: Message):
    if user["in game"]:
        user["in game"] = False
        await message.answer(
            """Вы вышли из игры,
если захотите сыграть снова - напишите об этом."""
        )
    else:
        await message.answer(
            """А мы итак не играем!:)
Может сыграем разок?"""
        )


@dp.message(
    F.text.lower().in_(["да", "давай", "сыграем", "игра", "играть", "хочу играть"])
)
async def process_positive_answer(message: Message) -> Message:
    if not user["in game"]:
        user["in game"] = True
        user["secret_number"] = get_random_number()
        user["attempts"] = ATTEMPTS
        await message.answer(
            """Ура! Я загадал число от 1 до 100,
Попробуй угадать!:)"""
        )
    else:
        await message.answer(
            """Пока мы играем в игру я могу
реагировать только на числа от 1 до 100
и команды /cancel и /stat"""
        )


@dp.message(F.text.lower().in_(["нет", "не хочу", "не", "не буду"]))
async def process_negative_answer(message: Message) -> Message:
    if not user["in game"]:
        await message.answer(
            """Если захочешь поиграть,
просто напиши об этом"""
        )
    else:
        await message.answer("""Мы же уже играем, присылай числа от 1 до 100""")


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> Message:
    if user["in game"]:
        if int(message.text) == user["secret_number"]:
            user["in game"] = False
            user["total_games"] += 1
            user["wins"] += 1
            await message.answer(
                """Ура!!! Ты угадал(а) число!
Сыграем ещё раз?"""
            )
        elif int(message.text) > user["secret_number"]:
            user["attempts"] -= 1
            await message.answer("Моё число меньше")
        elif int(message.text) < user["secret_number"]:
            user["attempts"] -= 1
            await message.answer("Моё число больше")
        if user["attempts"] == 0:
            user["in game"] = False
            user["total_games"] += 1
            await message.answer(
                f"""К сожалению у тебя больше не осталось
попыток. Ты проиграл(а):( Моё число было {user['secret_number']}
Сыграем ещё раз?"""
            )
    else:
        await message.answer(
            """Мы ещё не играем.
Хочешь сыграть?)"""
        )


@dp.message(Command(commands="support"))
async def send_user_id(message: Message) -> Message:
    await message.reply(f"Ваш ID: '{message.from_user.id}'", parse_mode="Markdown")


@dp.message()
async def process_other_answers(message: Message) -> Message:
    if user["in game"]:
        await message.answer(
            """Мы же с тобой сейчас играем
Присылай числа от 1 до 100)"""
        )
    else:
        await message.answer(
            """Я очень ограничен в ответах:(
Но можем сыграть в игру!)"""
        )


if __name__ == "__main__":
    dp.run_polling(bot)
# commit
