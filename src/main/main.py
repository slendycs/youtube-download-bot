import asyncio

from config.bot_config import bot, dp
from config.logger_config import logger


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())