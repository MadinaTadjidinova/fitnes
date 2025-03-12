import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command 

# Токен бота (замените на ваш)
TOKEN = "7776078242:AAE4JRhawvT_vCgjRJ_bxyjlmadux5iole4"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Логирование
logging.basicConfig(level=logging.INFO)

# База данных пользователей
user_data = {}

# Клавиатура для начала работы
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Ввести данные")],
        [KeyboardButton(text="📊 Прогресс"), KeyboardButton(text="🔄 Обновить данные")]
    ],
    resize_keyboard=True
)

# Уровни активности
activity_levels = {
    "Малоподвижный": 1.2,
    "Слабая активность": 1.375,
    "Средняя активность": 1.55,
    "Высокая активность": 1.725,
    "Очень высокая активность": 1.9
}

# Цели пользователя
goals = {
    "Похудение": -300,
    "Поддержание веса": 0,
    "Набор массы": 300
}

# Словарь рекомендаций
recommendations = {
    "low_cal": ["🥗 Больше овощей и белка", "🚶 10 000 шагов в день", "💧 Пейте больше воды"],
    "maintain": ["🍽 Сбалансированное питание", "🏋️ 3-4 тренировки в неделю", "😴 7-8 часов сна"],
    "gain": ["🍗 Увеличьте потребление белка", "🏋️‍♂️ Силовые тренировки", "🥑 Ешьте полезные жиры"]
}

# Функция создания inline-кнопок
def create_task_buttons(user_id):
    buttons = []
    completed_tasks = user_data.get(user_id, {}).get("completed_tasks", set())

    for task in user_data[user_id]["tasks"]:
        status = "✅" if task in completed_tasks else "❌"
        buttons.append([InlineKeyboardButton(text=f"{status} {task}", callback_data=f"task_{task}")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Хендлер команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"completed_tasks": set()}
    
    await message.answer(
        "Привет! Я помогу тебе с фитнес-программой. Сначала введи свои данные.",
        reply_markup=main_menu
    )

# Хендлер для ввода данных
@router.message(F.text == "📋 Ввести данные")
async def request_user_data(message: types.Message):
    await message.answer("Введите ваш возраст, вес, рост (в см) через запятую (пример: `25, 70, 175`):")

# Хендлер обработки данных пользователя
@router.message(F.text.regexp(r"^\d{1,2},\s*\d{2,3},\s*\d{2,3}$"))
async def process_user_data(message: types.Message):
    user_id = message.from_user.id
    age, weight, height = map(int, message.text.split(","))

    user_data[user_id]["age"] = age
    user_data[user_id]["weight"] = weight
    user_data[user_id]["height"] = height

    # Спрашиваем уровень активности
    activity_buttons = [[InlineKeyboardButton(text=level, callback_data=f"activity_{level}")] for level in activity_levels]
    keyboard = InlineKeyboardMarkup(inline_keyboard=activity_buttons)
    
    await message.answer("Выберите ваш уровень активности:", reply_markup=keyboard)

# Обработчик выбора активности
@router.callback_query(F.data.startswith("activity_"))
async def set_activity(call: types.CallbackQuery):
    user_id = call.from_user.id
    level = call.data.replace("activity_", "")

    user_data[user_id]["activity_level"] = level

    # Спрашиваем цель
    goal_buttons = [[InlineKeyboardButton(text=goal, callback_data=f"goal_{goal}")] for goal in goals]
    keyboard = InlineKeyboardMarkup(inline_keyboard=goal_buttons)
    
    await call.message.edit_text("Какая у вас цель?", reply_markup=keyboard)

# Обработчик выбора цели
@router.callback_query(F.data.startswith("goal_"))
async def set_goal(call: types.CallbackQuery):
    user_id = call.from_user.id
    goal = call.data.replace("goal_", "")

    user_data[user_id]["goal"] = goal

    # Рассчитываем калорийность
    bmr = 10 * user_data[user_id]["weight"] + 6.25 * user_data[user_id]["height"] - 5 * user_data[user_id]["age"] + 5
    tdee = bmr * activity_levels[user_data[user_id]["activity_level"]]
    calorie_goal = tdee + goals[goal]

    # Генерируем индивидуальные рекомендации
    if goal == "Похудение":
        tasks = recommendations["low_cal"]
    elif goal == "Поддержание веса":
        tasks = recommendations["maintain"]
    else:
        tasks = recommendations["gain"]

    user_data[user_id]["tasks"] = tasks

    keyboard = create_task_buttons(user_id)
    
    await call.message.edit_text(
        f"Ваш суточный калораж: {calorie_goal:.0f} ккал.\nВот ваши рекомендации:",
        reply_markup=keyboard
    )

# Обработчик выполнения задачи
@router.callback_query(F.data.startswith("task_"))
async def mark_task_done(call: types.CallbackQuery):
    user_id = call.from_user.id
    task = call.data.replace("task_", "")

    if task in user_data[user_id]["completed_tasks"]:
        user_data[user_id]["completed_tasks"].remove(task)
    else:
        user_data[user_id]["completed_tasks"].add(task)

    keyboard = create_task_buttons(user_id)
    await call.message.edit_text("Выберите выполненные задачи:", reply_markup=keyboard)

# Хендлер прогресса
@router.message(F.text == "📊 Прогресс")
async def show_progress(message: types.Message):
    user_id = message.from_user.id
    completed = len(user_data.get(user_id, {}).get("completed_tasks", set()))
    total = len(user_data[user_id]["tasks"])

    progress_percent = (completed / total) * 100
    await message.answer(f"📈 Прогресс: {completed} из {total} задач выполнено ({progress_percent:.1f}%)")

# Запуск бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
