import logging

from aiogram import F, Router, types, Bot
from aiogram.types import LabeledPrice
from aiogram.fsm.context import FSMContext

from bot_app.modules import messages
from bot_app.tg.callbacks.lessons import BuyLessonData
from bot_app.application.lesson_service import LessonService
from bot_app.application.user_service import UserService
from bot_app.application.payment_service import PaymentService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
import bot_app.tg.keyboards.lessons as lessons_kb

from shared.settings import YOO_KASSA_TOKEN, S3_BUCKET
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
    order_media_minio: OrderMediaRepository,
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
    await message.answer(
        text=messages.WAIT_FOR_SENDING_MESSAGE.format(name=lesson.name)
    )

    for doc_url in lesson.doc_urls:
        media, metadata = await order_media_minio.get_safe_objects_by_name(
            bucket_id=S3_BUCKET, object_name=doc_url
        )
        await message.answer_document(
            document=types.BufferedInputFile(file=media, filename=doc_url),
            protect_content=True,
        )

    await message.answer(
        text=messages.THANKS_MESSAGE, reply_markup=lessons_kb.choose_lang_mode()
    )
