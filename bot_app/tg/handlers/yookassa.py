import logging

from aiogram import F, Router, types, Bot
from aiogram.types import LabeledPrice
from aiogram.fsm.context import FSMContext

from bot_app.tg.callbacks.lessons import BuyLessonData
from bot_app.application.lesson_service import LessonService
from bot_app.application.user_service import UserService
from bot_app.application.payment_service import PaymentService

from shared.settings import YOO_KASSA_TOKEN
from shared.models import Lessons

yookass_router = Router()


@yookass_router.callback_query(BuyLessonData.filter())
async def manager(
    callback: types.CallbackQuery,
    callback_data: BuyLessonData,
    lesson_service: LessonService,
    state: FSMContext,
    bot: Bot,
):
    logging.info("Manager get contact")
    logging.info(YOO_KASSA_TOKEN)

    lesson: Lessons = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Оплата урока {lesson.name}",
        description=lesson.description,
        payload="test-invoice-payload",
        provider_token=YOO_KASSA_TOKEN,
        currency="rub",
        prices=[LabeledPrice(label=f"{lesson.price} руб.", amount=lesson.price * 100)],
        start_parameter="ads",
        protect_content=True,
    )

    data = await state.update_data({"currnt_lesson_id": lesson.id})
    logging.info(f"data: {data}")


@yookass_router.pre_checkout_query()
async def processing_pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery, bot: Bot
):
    # await bot.send_message(
    #     chat_id=pre_checkout_query.from_user.id, text="adsa sas dsda dsa as d"
    # )
    await pre_checkout_query.answer(ok=True)


@yookass_router.message(types.ContentType.SUCCESSFUL_PAYMENT == F.content_type)
async def processing_pay(
    message: types.Message,
    state: FSMContext,
    lesson_service: LessonService,
    user_service: UserService,
    payment_service: PaymentService,
):
    """Main payment processing function"""
    invoice_payload = message.successful_payment.invoice_payload
    # await message.answer(str(invoice_payload) + "DAA")
    await message.answer(text="✅ Оплата успешно произведена! ✅")

    currnt_lesson_id = (await state.get_data())["currnt_lesson_id"]

    lesson = await lesson_service.get_lesson(lesson_id=currnt_lesson_id)

    await user_service.update_user_lessons_list(
        telegram_id=message.from_user.id, lesson_id=lesson.id
    )

    await payment_service.create_payment(
        telegram_id=message.from_user.id, lesson_id=lesson.id, price=lesson.price
    )

    for i in range(1, 4):
        await message.answer(text=f"Документ №{i} из урока {lesson.name}")
