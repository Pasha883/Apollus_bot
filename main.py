import asyncio
from aiogram import Bot, Dispatcher

from Modules.handlers import router
from Database.models import async_main

import os, shutil


async def main():
    folder = 'Photo'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

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