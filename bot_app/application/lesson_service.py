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

    async def get_lessons(self, language: str):
        stmt = (
            select(Lessons)
            .where(Lessons.is_available == True)
            .where(Lessons.language == language)
        )

        lessons = await self.session.scalars(stmt)
        lessons = lessons.fetchall()

        return lessons

    async def create_lessons(
        self,
        name: str,
        language: str,
        description: str,
        voice_urls: list[str],
        doc_urls: list[str],
        price: float,
        is_available: bool = True,
    ):
        values = {
            "name": name,
            "language": language,
            "description": description,
            "voice_urls": voice_urls,
            "doc_urls": doc_urls,
            "price": price,
            is_available: is_available,
        }
        stmt = insert(Lessons)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()

        await self.session.execute(stmt)
        await self.session.commit()
