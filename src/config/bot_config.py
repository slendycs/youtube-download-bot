from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config

from config.redis_config import storage
from bot.command_handlers import command_router

# Устанавливаем токен бота и диспетчер
bot = Bot(token=config('BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)


# Включаем обработку роутеров
dp.include_router(command_router)