from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.keyboards import kb
import app.database.requests as rq


router = Router()


class CreateTask(StatesGroup):
    task = State()


class DelTask(StatesGroup):
    task = State()


@router.message(CommandStart())
async def bot_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply(
        "Привет!\nСоздадим первую задачу?\nНажимай на /add", reply_markup=kb
    )


# Обработчик команды /add для добавления задачи
@router.message(Command("add"))
async def create_task(message: Message, state: FSMContext):
    await state.set_state(CreateTask.task)
    await message.answer("Введите текст задачи:", reply_markup=kb)


@router.message(CreateTask.task)
async def add_task(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id
    task: str = message.text
    await rq.set_task(tg_id=tg_id, task=task)
    await message.answer(f"Задача:\n{task}\nCохранена.", reply_markup=kb)
    await state.clear()


# Обработчик команды /tsk для добавления задачи
@router.message(Command("tsk"))
async def get_tasks(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id
    tasks_generator = rq.get_task(tg_id=tg_id)

    async for tasks in tasks_generator:
        if not tasks:
            await message.answer("Текущих задач нет.", reply_markup=kb)
            break
        for obj_task in tasks:
            number: int = obj_task.id
            task: str = obj_task.task
            await message.answer(f"Задача: № {number}\n{task}.",
                                 reply_markup=kb)

    await state.clear()


# Обработчик команды /del для добавления задачи
@router.message(Command("del"))
async def delete_task(message: Message, state: FSMContext):
    await state.set_state(DelTask.task)
    await message.answer("Введите задачи для удаления через пробел:",
                         reply_markup=kb)


@router.message(DelTask.task)
async def del_tasks(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id
    tasks: list = list(map(int, message.text.split()))
    await rq.del_task(tg_id=tg_id, id_tasks=tasks)
    await message.answer("Задачи удалены.", reply_markup=kb)
    await state.clear()
