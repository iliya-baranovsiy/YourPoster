from fastapi import FastAPI, Request
from botLogic.bot_services.bot_instance import bot, dp, WEBHOOK_PATH, WEBHOOK_URL
import contextlib
import uvicorn
import asyncio
from redisWork.autopostingCash.user_id_cashing import redis_q
from redisWork.autopostingCash.cash_cleaner import cash_cleaner


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot=bot, update=update)
    return {"ok": True}


async def start_bot():
    await redis_q.clear_users_set()
    await cash_cleaner.drop_counter()
    await cash_cleaner.drop_cash()
    uvicorn.run("main_bot:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(start_bot())
