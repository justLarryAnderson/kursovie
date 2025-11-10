import asyncpg
from typing import Optional, List, Dict

class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def create_pool(cls):
        cls._pool = await asyncpg.create_pool(
            "postgresql://user:password@localhost/housing"
        )

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            await cls.create_pool()
        return cls._pool

    async def get_user_apartment_info(self, user_id: int) -> Dict:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT apartment_number, full_name, phone_number FROM users WHERE telegram_id = $1",
                user_id
            )

    async def get_debt(self, user_id: int) -> float:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT debt FROM payments WHERE user_id = (SELECT id FROM users WHERE telegram_id = $1) ORDER BY id DESC LIMIT 1",
                user_id
            )

    async def get_user_applications(self, user_id: int) -> List[Dict]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(
                "SELECT type, description, status FROM applications WHERE user_id = (SELECT id FROM users WHERE telegram_id = $1) ORDER BY id DESC",
                user_id
            )

    async def create_application(self, user_id: int, app_type: str, description: str):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO applications (user_id, type, description) VALUES ((SELECT id FROM users WHERE telegram_id = $1), $2, $3)",
                user_id, app_type, description
            )

    async def get_user_meters(self, user_id: int) -> List[Dict]:
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(
                "SELECT type, value FROM meters WHERE user_id = (SELECT id FROM users WHERE telegram_id = $1) ORDER BY date DESC LIMIT 3",
                user_id
            )

    async def update_meter(self, user_id: int, meter_type: str, value: float):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO meters (user_id, type, value) VALUES ((SELECT id FROM users WHERE telegram_id = $1), $2, $3)",
                user_id, meter_type, value
            )