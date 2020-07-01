import redis 
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
QUEUE_NAME = 'my-queue:1'
 
def main(): 
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    while True:
        ### Producer uses BRPOP to grab an available message from the List (Queue)  
        ### Note: will block for specified timeout until a message is available (0=infinite) 
        res = r.brpop(QUEUE_NAME, timeout=0)

        if (res):
            print(f'List Blocking Consumer grabbed task {res}')
        # sleep to simulate processing of the item
        time.sleep(1)

if __name__ == "__main__":
    main()    