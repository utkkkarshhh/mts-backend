import sys
import redis
from rq import Worker, Queue

redis_url = "redis://localhost:6379/0"
conn = redis.from_url(redis_url)

if __name__ == "__main__":
    queue_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    queue = Queue(queue_name, connection=conn)
    worker = Worker([queue], connection=conn)
    worker.work()
