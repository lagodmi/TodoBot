from app.database.database import db_helper
from app.database.models import User, Task
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with db_helper.get_scope_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_task(tg_id: int, task: str) -> None:
    async with db_helper.get_scope_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )
        session.add(Task(user_id=user.id, task=task))
        await session.commit()


async def get_task(tg_id: int):
    async with db_helper.get_scope_session() as session:
        user: User = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )
        if user is None:
            yield []
        else:
            result = await session.execute(
                select(Task).where(Task.user_id == user.id)
            )
            tasks: list[Task] = result.scalars().all()
            await session.commit()
            yield tasks


async def del_task(tg_id: int, id_tasks: list) -> None:
    async with db_helper.get_scope_session() as session:
        user: User = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )

        if user is None:
            return

        try:
            for id in id_tasks:
                task = await session.get(Task, id)
                if task:
                    await session.delete(task)
            await session.commit()
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
            await session.rollback()
