language_smile = {"en": "🇬🇧", "zh": "🇨🇳"}

START_MESSAGE = (
    "<b>👋 Добро пожаловать в бот для изучения языков!</b>\n\n"
    "Здесь вы можете приобрести и пройти уроки по китайскому и английскому языкам, которые помогут вам освоить:\n"
    "- Основы китайского и английского языков;\n"
    "- Произношение и фонетику;\n"
    "- Грамматику и синтаксис;\n"
    "- Расширение словарного запаса;\n"
    "- Навыки разговорной речи.\n\n"
    "<b>Что вы можете сделать в этом боте:</b>\n"
    "- Просмотреть доступные уроки и их описание;\n"
    "- Приобрести уроки по интересующим темам;\n"
    "- Получить доступ к ранее купленным урокам.\n\n"
    "<b>🌟 Начните свой путь к изучению китайского или английского языка прямо сейчас!</b>"
)

HELP_MESSAGE = (
    "<b>🛠 Помощь по использованию бота:</b>\n\n"
    "<b>Доступные команды:</b>\n\n"
    "<b>1. /lessons</b> - Перейти к выбору уроков.\n"
    "<b>2. /personal_account</b> - Перейти в личный кабинет.\n"
    "<b>3. /english_lessons</b> - Просмотреть список доступных уроков по английскому языку.\n"
    "<b>4. /chinese_lessons</b> - Просмотреть список доступных уроков по китайскому языку.\n"
    "<b>🌟 Приятного и эффективного обучения!</b>\n"
)

LESSONS_MODE_MESSAGE = (
    "<b>🌍 Выберите язык обучения:</b>\n\n"
    "Пожалуйста, выберите язык, на котором хотите начать/продолжить обучение:\n"
    "- 🇬🇧 Английский язык;\n"
    "- 🇨🇳 Китайский язык.\n\n"
    "<b>Нажмите на выбранный язык, чтобы продолжить.</b>\n"
)

LESSONS_MESSAGE = (
    "<b>📚 Выберите урок из списка:</b>\n\n"
    "Нажмите на интересующий вас урок, чтобы узнать подробнее и приобрести его:\n"
)

LESSON_DETAILS_MESSAGE = (
    "<b>📘 Урок: {name}</b>\n\n"
    "<b>Описание:</b> {description}\n\n"
    "<b>💰 Стоимость:</b> {price} руб.\n\n"
    "<b>👉 Готовы приобрести? Нажмите на кнопку ниже!</b>\n"
)

PERSONAL_ACCOUNT_MESSAGE = (
    "👋 Добро пожаловать в <b>личный кабинет</b>! 👋\n\n"
    "<b>📘 Имя:</b> {username}\n"
    "<b>🌍 Язык:</b> {language_code}\n"
    "<b>📅 Дата регистрации:</b> {registered_at}\n"
    "<b>💰 Куплено уроков:</b> {bouhgt_amount} шт.\n\n"
    "<b>👇 Ваши уроки! 👇</b>"
)

WAIT_FOR_SENDING_MESSAGE = (
    "⏳ Пожалуйста, подождите, <b>отправляем материал</b> урока <b>«{name}»</b> ⚡"
)

ENGLISH_LANGUAHE_MESSAGE = "🇬🇧 Английский 🇬🇧"
CHINESE_LANGUAGE_MESSAGE = "🇨🇳 Китайский 🇨🇳"
PA_MESSAGE = "🧍‍♂ Личный кабинет 🧍‍♀"
QUESTIONS_MESSAGE = "❓ Вопросы ❓"
SUPPORT_MESSAGE = "🆘 Поддержка 🆘"
BACK_MESSAGE = "🔙 Назад 🔙"
DEMO_VERSION_MESSAGE = "❓ Демо-версия ❓"
BUY_MESSAGE = "✅ Купить ✅"
BEGIN_MESSAGE = "✅ Начать ✅"
THANKS_MESSAGE = "⚡ Спасибо за покупку! <b>Приятного изучения!</b> 😊"

ADMIN_START_MESSAGE = (
    "👋 Привет, <b>{name}</b>! Вы перешли в <b>режим администрирования</b>... 💻"
)
ADD_LESSON_MESSAGE = "✅✅✅ Добавить урок ✅✅✅"
EDIT_LESSON_MESSAGE = "🛠 Выберите поле для <b>редактирования</b> 🛠"
