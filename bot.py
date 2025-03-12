import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Токен бота (замените на ваш)
TOKEN = "7776078242:AAE4JRhawvT_vCgjRJ_bxyjlmadux5iole4"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём Router
router = Router()

# Логирование
logging.basicConfig(level=logging.INFO)

# База данных (имитация хранения пользователей)
user_data = {}

# Клавиатура для команд
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Рекомендации")],
        [KeyboardButton(text="📊 Прогресс")]
    ],
    resize_keyboard=True
)

# Данные о питании и тренировках
diet_recommendations = [
    "🍳 Завтрак: Овсянка с ягодами и орехами",
    "🥗 Обед: Салат с курицей на гриле и овощами",
    "🍣 Ужин: Лосось с киноа и брокколи",
    "🥛 Перекус: Греческий йогурт с мёдом и миндалем"
]

exercise_recommendations = [
    "🏃 Кардио: 30 минут бега или велотренировки",
    "💪 Силовые: 3x10 приседания, отжимания, выпады",
    "🧘 Гибкость: 15 минут йоги",
    "📌 Кор: 3x20 планка, скручивания"
]

# Хендлер команды /start
@router.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"tasks_completed": 0, "total_tasks": len(diet_recommendations) + len(exercise_recommendations)}
    
    await message.answer(f"Привет, {message.from_user.first_name}! Я помогу тебе с фитнес-планом.\nВыбери действие:", reply_markup=main_menu)

# Хендлер для рекомендаций
@router.message(lambda message: message.text == "📋 Рекомендации")
async def send_recommendations(message: types.Message):
    recommendations = "\n".join(diet_recommendations + exercise_recommendations)
    await message.answer(f"Вот твои рекомендации:\n\n{recommendations}")

# Хендлер для отслеживания прогресса
@router.message(lambda message: message.text == "📊 Прогресс")
async def show_progress(message: types.Message):
    user_id = message.from_user.id
    tasks_completed = user_data.get(user_id, {}).get("tasks_completed", 0)
    total_tasks = user_data.get(user_id, {}).get("total_tasks", len(diet_recommendations) + len(exercise_recommendations))
    
    progress_percent = (tasks_completed / total_tasks) * 100
    await message.answer(f"📈 Прогресс: {tasks_completed} из {total_tasks} задач выполнено ({progress_percent:.1f}%)")

# Функция запуска бота
async def main():
    dp.include_router(router)  # Теперь добавляем Router, а не отдельные функции

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
