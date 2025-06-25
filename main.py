from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import openai
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 Привіт! Я FullStackFriendBot. Напиши, що тебе цікавить в ІТ, і я підкажу, з чого почати!")

@dp.message_handler()
async def recommend(message: types.Message):
    prompt = f"Студент запитує: {message.text}. Дай коротку навчальну пораду українською."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти освітній помічник для ІТ-студентів."},
                {"role": "user", "content": prompt}
            ]
        )
        await message.answer(response['choices'][0]['message']['content'])
    except Exception as e:
        await message.answer("⚠️ Виникла помилка. Спробуй пізніше.")
        print(e)

if __name__ == '__main__':
    executor.start_polling(dp)
