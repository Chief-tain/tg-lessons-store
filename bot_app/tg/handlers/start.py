import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.payment_service import PaymentService
from bot_app.modules import messages
from bot_app.tg.states.states import States
from bot_app.tg.keyboards.manager import manager_and_help


start_router = Router()


@start_router.message(Command(commands=["start"]))
async def greetings(
    message: types.Message,
    user_service: UserService,
    state: FSMContext,
    lesson_service: LessonService,
    payment_service: PaymentService,
):

    logging.info("User pressed /start")

    data = await state.get_data()
    from_user = message.from_user
    if not data.get("locale"):
        locale = from_user.language_code
        await state.update_data({"locale": locale})
    else:
        locale = data.get("locale")

    await user_service.create_user(
        telegram_id=from_user.id,
        username=from_user.username,
        first_name=from_user.first_name,
        last_name=from_user.last_name,
        language_code=from_user.language_code,
    )

    # await lesson_service.create_lessons(
    #     name="test",
    #     description="sample",
    #     voice_urls=["sasdasdsa", "dasdas"],
    #     doc_urls=["sasdasdsa", "dasdas"],
    #     price=400,
    # )

    # await payment_service.create_payment(
    #     telegram_id=from_user.id, lesson_id=1, price=400
    # )

    await message.answer(messages.START_MESSAGE, reply_markup=manager_and_help())
    await state.set_state(States.help)
