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
