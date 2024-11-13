import aiogram
import handlers
import asyncio

bot = aiogram.Bot(token='8036211361:AAF2nXSVMMSuAXhzByaOWqGNgtdBjRZQb8s')

dp = aiogram.Dispatcher()
dp.include_router(handlers.router)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
