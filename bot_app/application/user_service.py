from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Users


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Users:
        stmt = select(Users).where(Users.id == user_id)
        response = await self.session.scalars(stmt)
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

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_lessons_id_list(self, telegram_id: int) -> None:
        bought_lessons_id_get_stmt = select(Users.bought_lessons_id).where(
            Users.id == telegram_id
        )
        bought_lessons_ids = await self.session.scalars(bought_lessons_id_get_stmt)
        bought_lessons_ids: list[int] = bought_lessons_ids.one_or_none()
        return bought_lessons_ids

    async def update_user_lessons_list(self, telegram_id: int, lesson_id: int) -> None:

        bought_lessons_ids: list[int] = await self.get_user_lessons_id_list(
            telegram_id=telegram_id
        )
        bought_lessons_ids.append(lesson_id)

        bought_lessons_id_upd_stmt = (
            update(Users)
            .where(Users.id == telegram_id)
            .values(bought_lessons_id=bought_lessons_ids)
        )
        await self.session.execute(bought_lessons_id_upd_stmt)
