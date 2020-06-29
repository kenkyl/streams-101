import redis 
import random
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
QUEUE_NAME = 'my-queues:1'
 
def main(): 
    # Connect to Redis client library
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    # Create endless producer loop 
    while True:
        # Generatre pseduo random task id 
        new_task_id = random.randint(1000,10000)

        ## Producer uses LPUSH to append to a List (Queue) ##
        res = r.lpush(QUEUE_NAME, new_task_id)

        # Print results and sleep
        print(f'List Producer added task # {new_task_id} to queue {QUEUE_NAME} with length {res}')
        time.sleep(3)

if __name__ == "__main__":
    main()    
