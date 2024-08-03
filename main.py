import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

bot = Bot(token='6569356204:AAEazNBICS_4rqy9Db4eZ2qv7r25A096Ib8')
dp = Dispatcher()

@dp.message(CommandStart())
async def startCommand(message: Message):
    await message.answer("Команда start")

@dp.message(Command('help'))
async def  hello(message: Message):
    await message.answer("Команда help")

@dp.message(F.text == "Кто такой Тайлер Дерден?")
async def text(message: Message):
    await message.answer("Это не важно...")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down...')