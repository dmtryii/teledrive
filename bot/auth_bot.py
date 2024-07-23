import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

import config
from handlers import commands


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def on_startup() -> None:
    await bot.set_webhook(f"{config.BOT_WEBHOOK_URL}{config.BOT_WEBHOOK_PATH}")


def main():
    logging.basicConfig(level=logging.DEBUG)
    dp.include_routers(
        commands.router
    )

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_requests_handler.register(app, path=config.BOT_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, port=int(config.BOT_WEBHOOK_PORT))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
