import logging
from aiogram import Bot, Dispatcher
from handlers import router, form_router
from config_reader import config
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = config.bot_token.get_secret_value()
WEB_SERVER_HOST = '0.0.0.0'
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = '/webhook'
WEBHOOK_SECRET = 'my-secret'
BASE_WEBHOOK_URL = 'https://f8ef-37-214-56-135.ngrok.io'


async def on_startup(bot: Bot):
    await bot.set_webhook(
        url=f'{BASE_WEBHOOK_URL}{WEBHOOK_PATH}',
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query"],
    )


def main() -> None:
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(form_router)

    dp.startup.register(on_startup)

    bot = Bot(token=TOKEN)
    app = web.Application()

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_request_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()