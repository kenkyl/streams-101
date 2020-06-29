import redis
import time
import random

STREAM_NAME = ''

def main():
       r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    while True:
        # Generatre pseduo random task id 
        new_task_id = random.randint(1000,10000)
        message = f'process # {new_task_id} is complete'

        ### Publisher uses PUBLISH to send a message to Subscribers on the Channel ###
        res = r.publish(CHANNEL_NAME, message)

        print(f'PubSub Publisher sent \"{message}\" to channel {CHANNEL_NAME}')
        time.sleep(3)

if __name__ == "__main__":
    main()    
