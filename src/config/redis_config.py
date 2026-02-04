from aiogram.fsm.storage.redis import RedisStorage
from decouple import config

redis_url = (f'redis://default:{config('REDIS_PASSWORD')}@'
             f'{config('REDIS_HOST')}:{config('REDIS_PORT')}/0')

storage = RedisStorage.from_url(redis_url)
