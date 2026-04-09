from config.configurations import settings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from botLogic.routers import router

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

WEBHOOK_PATH = f"/bot/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{settings.APP_URL}{WEBHOOK_PATH}"

dp.include_router(router)
