import redis
from rq import Worker, Queue

# Redis connection
redis_conn = redis.Redis()

listen = [Queue('default', connection=redis_conn)]

if __name__ == '__main__':
    worker = Worker(listen, connection=redis_conn)
    worker.work()
