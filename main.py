import logging
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from config_reader import config
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from handlers import main_router, form_router
from states import TeacherForm
from bot import get_bot


WEB_SERVER_HOST = config.web_server_host
WEB_SERVER_PORT = config.web_server_port
WEBHOOK_PATH = config.webhook_path
WEBHOOK_SECRET = config.webhook_secret
BASE_WEBHOOK_URL = config.base_webhook_url


bot = get_bot()
app = web.Application()


async def on_startup():
    await bot.set_webhook(
        url=f'{BASE_WEBHOOK_URL}{WEBHOOK_PATH}',
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query"],
    )


def main() -> None:
    dp = Dispatcher()

    dp.include_router(main_router)
    dp.include_router(form_router)

    dp.startup.register(on_startup)

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