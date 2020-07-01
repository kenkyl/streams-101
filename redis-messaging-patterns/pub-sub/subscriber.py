import redis
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
CHANNEL_NAME = 'message-channel:2'
 
def main(): 
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)

    ### Subscriber uses PSUBSCRIBE to subscribe to all channels starting with prefix 'message-channels:'
    p = r.pubsub()
    p.psubscribe('message-channel:*')
    ### Note: can also use SUBSCRIBE to subscibe to specified channel(s)
    #p.subscribe(CHANNEL_NAME)

    while True:
        ### Grab a message from the channel(s) subscribed to (note: Python implementation specfic)
        message = p.get_message(timeout=100.0)

        print(f'PubSub Subscriber got \"{message}\" on channel {CHANNEL_NAME}')
        
        # sleep to simulate processing of the item
        time.sleep(1)

if __name__ == "__main__":
    main()    

