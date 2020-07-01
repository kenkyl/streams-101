import redis
import sys
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
STREAM_NAME = 'process-stream:3'

class StreamGroupConsumer:
    def __init__(self, r, consumer_group, consumer_name):
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.redis = r
        
    # listen and consume indefinitely
    def consume(self):
        try:
            ### initiate consumer group if not already
            self.redis.xgroup_create(STREAM_NAME, self.consumer_group, id='$')
        except:
            print(f'group {self.consumer_group} already exists')
        while True:
            ### Streams Group Consumer calls XREADGROUP with Block=0 to listen indefinitely an
            ### Note: use '>' as id field to grab the most recent additions to the consumer group   
            update = self.redis.xreadgroup(self.consumer_group, self.consumer_name, {STREAM_NAME: '>'}, block=0)
            # parse the result 
            listened = update[len(update)-1]
            samples = listened[len(listened)-1]
            id_latest, val_latest = samples[len(samples)-1]
            # process the message then continue listening for new messages 
            print(f'Group Consumer {self.consumer_name} in {self.consumer_group} RECEIVED: {id_latest} => {val_latest}')
            self.process_message(id_latest, val_latest)

    def process_message(self, message_id, message_val):
        # sleep to simulate message processing
        time.sleep(1)
        ### Group Consumer uses XACK to acknowledge the completion of a message
        self.redis.xack(STREAM_NAME, self.consumer_group, message_id)
        print(f'Group Consumer {self.consumer_name} in {self.consumer_group} PROCESSED: {message_id} => {message_val}')


def main():
    # Use command line arguments to add new groups and consumers (defaults are 1 and 1)
    group = 1
    consumer = 1
    if (len(sys.argv) > 1):
        consumer = sys.argv[2]
    if (len(sys.argv) > 1):
        group = sys.argv[1]
    
    # Create a new group consumer and start consuming new items on the stream 
    r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)
    group_consumer = StreamGroupConsumer(r, f'group{group}', f'consumer{consumer}')
    group_consumer.consume()
    print('done consuming!')

if __name__ == "__main__":
    main()    