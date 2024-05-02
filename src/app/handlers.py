from aiogram import Router
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import Message

from .keyboards import kb


router = Router()


# Обработчик команды /add для добавления задачи
@router.message_handler(commands=['add'])
async def add_task(message: Message):
    await message.answer('Введите текст задачи:')
    await TaskStates.adding_task.set()

# Обработчик ввода текста задачи
@router.message_handler(state=TaskStates.adding_task)
async def save_task(message: Message, state: FSMContext):
    task = message.text
    async with state.proxy() as data:
        data['task'] = task
    
    with conn.cursor() as cur:
        cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        conn.commit()
    
    await message.answer(f'Задача "{task}" успешно добавлена.')
    await state.finish()

# Обработчик команды /tsk для вывода списка задач
@router.message_handler(commands=['tsk'])
async def list_tasks(message: Message):
    with conn.cursor() as cur:
        cur.execute("SELECT task FROM tasks")
        tasks = [row[0] for row in cur.fetchall()]
    
    if tasks:
        task_list = '\n'.join(tasks)
        await message.answer(f'Список задач:\n{task_list}')
    else:
        await message.answer('Список задач пуст.')
