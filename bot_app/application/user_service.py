from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from shared.dbs.postgresql import async_session
from shared.models import Users


class UserService:
    def __init__(self, pool: async_sessionmaker = async_session) -> None:

        self.pool = pool

    async def get_user(self, user_id: int) -> Users:
        stmt = select(Users).where(Users.id == user_id)

        async with self.pool() as session:
            response = await session.scalars(stmt)

        return response.one_or_none()

    async def create_user(
        self,
        telegram_id: int,
        username: str,
        first_name: str,
        last_name: str,
        language_code: str,
    ):
        values = {
            "id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language_code": language_code,
        }
        stmt = insert(Users)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()

        async with self.pool() as session:
            await session.execute(stmt)
            await session.commit()

    async def update_user_lessons_list(self, telegram_id: int, lesson_id: int) -> None:

        bought_lessons_id_get_stmt = select(Users.bought_lessons_id).where(
            Users.id == telegram_id
        )

        async with self.pool() as session:
            bought_lessons_id = await session.scalars(bought_lessons_id_get_stmt)
            bought_lessons_id: list = bought_lessons_id.one_or_none()

            bought_lessons_id.append(lesson_id)

            bought_lessons_id_upd_stmt = update(Users).values(
                bought_lessons_id=bought_lessons_id
            )
            await session.execute(bought_lessons_id_upd_stmt)
            await session.commit()
