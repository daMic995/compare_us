import os
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()
redis_url = os.getenv('UPSTASH_REDIS_REST_URL')
token = os.getenv('UPSTASH_REDIS_REST_TOKEN')

upstash_redis_client = Redis(url=redis_url, token=token)

upstash_redis_client.set('no_of_comparisons', 0)

print(upstash_redis_client.get('no_of_comparisons'))