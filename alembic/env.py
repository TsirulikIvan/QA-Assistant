import asyncio
import os

import asyncpg
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context


config = context.config

if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

connectable = create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)


async def run_migrations_online() -> None:
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: asyncpg.Connection) -> None:
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
