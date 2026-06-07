import redis.asyncio as redis

r = redis.from_url("redis://:YOURE_PASSWORD_REDIS@127.0.0.1:6379/0", decode_responses=True)