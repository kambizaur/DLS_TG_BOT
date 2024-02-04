import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from model import Model
# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = getenv("TG_BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(BOT_TOKEN)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer("Здравствуй, странник! Просто отправь мне фото кота...")

@dp.message(F.photo)
async def echo_handler(message: types.Message) -> None:
    await message.answer("Получил фото, начинаю колдовать...")

    file_id = message.photo[-1].file_id

    file_in = await bot.get_file(file_id)
    file_path = file_in.file_path

    model_path = "model.pt"
    file_in_path = "photos/file_in.jpg"
    file_out_path = "photos/file_out.jpg"
    
    await bot.download_file(file_path, file_in_path)

    Model(model_path).process_image(file_in_path, file_out_path)
    
    file_out = types.input_file.FSInputFile(file_out_path)

    await message.answer_photo(file_out)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer("Просто отправь мне фото кота...")

async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())