#redis is a cashe database, yo blocklist ma jti store garne, jti ko expiry time set garne, jti blocklist ma xa ki xaina check garne function le blocklist ma jti xa ki xaina check garne, jti blocklist ma xa bhane token revoke bhayeko ho bhanne bujhna sakinchha.
from redis.asyncio import Redis
from src.config import config

JTI_EXPIRY = 3600

token_blocklist = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value='blacklisted',
        ex=JTI_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    result = await token_blocklist.get(jti)
    return result is not None
#admin ko kam
[
    "adding user",
    "change role",
    "crud on user",
    "book submission",
    "crud on review",
    "crud on book",
    "revoking access"
]

#user ko kam
[
    "view books",
    "submit review",
    "update profile"
]