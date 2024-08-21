from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from shared.dbs.postgresql import async_session
from shared.models import Lessons


class LessonService:
    def __init__(self, pool: async_sessionmaker = async_session) -> None:

        self.pool = pool

    async def get_lesson(self, lesson_id: int) -> Lessons:
        stmt = select(Lessons).where(Lessons.id == lesson_id)

        async with self.pool() as session:
            response = await session.scalars(stmt)

        return response.one_or_none()

    async def create_lessons(
        self,
        description: str,
        voice_urls: list[str],
        doc_urls: list[str],
        price: float,
    ):
        values = {
            "description": description,
            "voice_urls": voice_urls,
            "doc_urls": doc_urls,
            "price": price,
        }
        stmt = insert(Lessons)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()

        async with self.pool() as session:
            await session.execute(stmt)
            await session.commit()
