import asyncio
import os

from aiogram import Dispatcher
from bot.handlers.viewer import viewer_router
from types.bot import BotAI

dispatcher = Dispatcher()
dispatcher.include_router(viewer_router)

TOKEN = os.environ["BOT_TOKEN"]


async def main():
    bot = BotAI(TOKEN)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
