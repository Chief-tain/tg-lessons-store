from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Lessons

import logging


class LessonService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_lesson(self, lesson_id: int) -> Lessons:
        stmt = select(Lessons).where(Lessons.id == lesson_id)

        lesson = await self.session.scalars(stmt)
        lesson = lesson.fetchall()[0]

        return lesson

    async def get_lessons(self):
        stmt = select(Lessons)

        lessons = await self.session.scalars(stmt)
        lessons = lessons.fetchall()

        return lessons

    async def create_lessons(
        self,
        name: str,
        description: str,
        voice_urls: list[str],
        doc_urls: list[str],
        price: float,
    ):
        values = {
            "name": name,
            "description": description,
            "voice_urls": voice_urls,
            "doc_urls": doc_urls,
            "price": price,
        }
        stmt = insert(Lessons)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()

        await self.session.execute(stmt)
        await self.session.commit()
