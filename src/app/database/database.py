from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from config import (
    USER,
    PASSWORD,
    DB,
    HOST,
    PORT,
)

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
ECHO = True


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_scope_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(DATABASE_URL, ECHO)
