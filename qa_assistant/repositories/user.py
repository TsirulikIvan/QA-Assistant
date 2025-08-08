from asyncpg import create_pool, Pool


class UserRepository:
    def __init__(self, pool: Pool | None = None):
        self._pool = pool

    async def set_pool(self, pool: Pool):
        self._pool = pool

    async def create(self, user_id: int, user_name: str, phone: int, first_name: str, last_name: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO users (id, name, number, first_name, last_name) VALUES ($1, $2, $3, $4, $5)""",
                user_id,
                user_name,
                phone,
                first_name,
                last_name,
            )


user_repository = UserRepository()
