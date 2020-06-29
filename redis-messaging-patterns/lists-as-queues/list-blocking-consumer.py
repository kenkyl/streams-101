import redis 
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
QUEUE_NAME = 'my-queues:1'
 
def main(): 
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    while True:
        ### Producer uses BRPOP to grab an available message from the List (Queue) ### 
        ### Note: will block for specified timeout until a message is available (0=infinite) ###
        res = r.brpop(QUEUE_NAME, timeout=0)

        # Print result and sleep
        if (res):
            print(f'List Blocking Consumer grabbed task {res}')
        time.sleep(1)

if __name__ == "__main__":
    main()    