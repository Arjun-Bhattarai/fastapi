import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect("postgresql://postgres:974526@localhost:5431/bookly_db")
    print("Connected successfully!")
    await conn.close()

asyncio.run(test())