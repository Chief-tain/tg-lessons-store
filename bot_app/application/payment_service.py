from sqlalchemy import desc, func, select, update, text, between
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from shared.dbs.postgresql import async_session
from shared.models import Payments


class PaymentService:
    def __init__(self, pool: async_sessionmaker = async_session) -> None:

        self.pool = pool

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

        async with self.pool() as session:
            await session.execute(stmt)
            await session.commit()
