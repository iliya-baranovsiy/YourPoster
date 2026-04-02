from config.configurations import settings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from botLogic.handlers.start_handler import router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

WEBHOOK_PATH = f"/bot/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{settings.APP_URL}{WEBHOOK_PATH}"

dp.include_routers(router)
