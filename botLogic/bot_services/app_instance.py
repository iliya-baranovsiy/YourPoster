from config.configurations import settings
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from botLogic.routers import router

dp = Dispatcher(storage=MemoryStorage())

WEBHOOK_PATH = f"/bot/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{settings.APP_URL}{WEBHOOK_PATH}"

dp.include_router(router)
