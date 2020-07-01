import redis
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
STREAM_NAME = 'process-stream:3'
 
def main(): 
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)
    # the special '$' character is to grab the newest message  
    id_latest = '$'
    while True:
        ### Streams Consumer uses XREAD with stream name and $ argument to grab the most recent message
        ### Block = 0 to wait indefinitely for next message 
        message = r.xread({STREAM_NAME: id_latest}, block=0)

        # parse the result and update id_latest to the id of the message we are processing
        listened = message[len(message)-1]
        stream = listened[len(listened)-2]
        samples = listened[len(listened)-1]
        id_latest, val_latest = samples[len(samples)-1]

        print(f'Streams Consumer got message {id_latest} with value \"{val_latest}\" on {stream}')
        # sleep to simulate message processing
        time.sleep(1)

if __name__ == "__main__":
    main()    
