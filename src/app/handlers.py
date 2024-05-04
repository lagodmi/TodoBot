from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import app.database.requests as rq


router = Router()


class Task(StatesGroup):
    task = State()


@router.message(CommandStart())
async def bot_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply(
        'Привет!\nСоздадим первую задачу?\nНажимай на /add',
        reply_markup=kb
    )


# Обработчик команды /add для добавления задачи
@router.message(Command('add'))
async def create_task(message: Message, state: FSMContext):
    await state.set_state(Task.task)
    await message.answer('Введите текст задачи:')


@router.message(Task.task)
async def add_task(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id
    task: str = message.text
    await rq.set_task(tg_id=tg_id, task=task)
    await message.answer(f'Задача:\n{task}\nCохранена.')
    await state.clear()
