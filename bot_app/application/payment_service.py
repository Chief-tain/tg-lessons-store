from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Payments


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(
        self,
        telegram_id: int,
        lesson_id: int,
        price: float,
    ):
        values = {
            "user_id": telegram_id,
            "lesson_id": lesson_id,
            "price": price,
        }
        stmt = insert(Payments)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing()

        await self.session.execute(stmt)
        await self.session.commit()
