from dataclasses import dataclass

from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Lessons


@dataclass
class LessonStructure:
    id: int
    language: str
    name: str
    description: str
    demo_urls: list[str]
    doc_urls: list[str]
    price: float
    is_available: bool


class LessonService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_lesson(self, lesson_id: int) -> Lessons:
        stmt = select(Lessons).where(Lessons.id == lesson_id)

        lesson = await self.session.scalars(stmt)
        lesson = lesson.fetchall()[0]

        return lesson

    async def get_lessons(self, language: str) -> list[LessonStructure]:
        stmt = (
            select(Lessons)
            .where(Lessons.is_available == True)
            .where(Lessons.language == language)
        )

        lessons = await self.session.scalars(stmt)
        lessons = lessons.fetchall()

        return [
            LessonStructure(
                id=lesson.id,
                language=lesson.language,
                name=lesson.name,
                description=lesson.description,
                demo_urls=lesson.demo_urls,
                doc_urls=lesson.doc_urls,
                price=lesson.price,
                is_available=lesson.is_available,
            )
            for lesson in lessons
        ]

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
