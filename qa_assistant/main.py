import asyncio
import sys
import fastapi
from contextlib import asynccontextmanager
from loguru import logger

from qa_assistant.utils.db import create_pool
from qa_assistant.settings import settings
from qa_assistant.repositories.user import user_repository
from qa_assistant.bot import bot, dp


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    logger.add(sys.stdout, serialize=True, level="INFO")
    logger.info("Creating Pool for DB", dsn=settings.postgres_dsn)
    logger.info("Setup DB connection")
    pool = await create_pool(settings.postgres_dsn)
    await user_repository.set_pool(pool)

    await dp.start_polling(bot)
    yield

    dp.stop_polling()
    await pool.close()


app = fastapi.FastAPI(title="QA Assistant", lifespan=lifespan)


@app.get("/health")
async def healcheck():
    return {"status": "ok"}


def create_app() -> fastapi.FastAPI:
    return app
