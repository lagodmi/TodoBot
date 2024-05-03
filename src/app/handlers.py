from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from .keyboards import kb


router = Router()


class Task(StatesGroup):
    task = State()


@router.message(CommandStart())
async def bot_start(message: Message):
    await message.reply('Привет', reply_markup=kb)


# Обработчик команды /add для добавления задачи
@router.message(Command('add'))
async def create_task(message: Message, state: FSMContext):
    await state.set_state(Task.task)
    await message.answer('Введите текст задачи:')


@router.message(Task.task)
async def add_task(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    data = await state.get_data()
    await message.answer(f'Задача:\n{data["task"]}\nCохранена.')
    await state.clear()

