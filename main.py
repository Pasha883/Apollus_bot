import asyncio
from aiogram import Bot, Dispatcher

from Modules.handlers import router
from Database.models import async_main


async def main():
    await async_main()

    bot = Bot(token='6569356204:AAEazNBICS_4rqy9Db4eZ2qv7r25A096Ib8')
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down...')