import redis
import time
import random

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
CHANNEL_NAME = 'message-channel:2'

def main():
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    while True:
        # Generatre pseduo random task id 
        message = f'process # {random.randint(1000,10000)} is complete'

        ### Publisher uses PUBLISH to send a message to Subscribers on the Channel ###
        res = r.publish(CHANNEL_NAME, message)

        print(f'PubSub Publisher sent \"{message}\" to channel {CHANNEL_NAME}')
        time.sleep(3)

if __name__ == "__main__":
    main()    