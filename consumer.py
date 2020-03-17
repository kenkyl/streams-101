import redis
import sys

# consts
STREAM_NAME = 'my-stream'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379 

class StreamConsumer:
    def __init__(self, redis_host, redis_port, consumer_group, consumer_num):
        self.consumer_group = consumer_group
        self.consumer_num = consumer_num
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.streams = {
            STREAM_NAME: '>'
        }
        # check consumer groups
        # consumer group 1 --> posts values to dashboard
        # consumer group 2 --> generates live stats from values
        # consumer group 3 --> persists values to historical db
        self.group_name = 'group1-dashboard' # default to group1 if value is not 2 nor 3
        if (self.consumer_group == 2):
            self.group_name = 'group2-stats'
        elif (self.consumer_group == 3):
            self.group_name = 'group3-persistence'

    # listen and consume indefinitely
    def consume(self):
        try:
            # initiate consumer group if not already
            self.redis.xgroup_create(STREAM_NAME, self.group_name, id='$')
        except:
            print(f'group {self.group_name} already exists')

        while True:
            # XREAD STREAMS my-stream <num>
            consumer_name = f'consumer-{self.consumer_group}-{self.consumer_num}'
            update = self.redis.xreadgroup(self.group_name, consumer_name, self.streams, block=0)
            #update = self.redis.xread(self.streams, block=5000)
            #print(f'update: {update}')
            # parse result
            listened = update[len(update)-1]
            samples = listened[len(listened)-1]
            id_latest, val_latest = samples[len(samples)-1]
            print(f'consumer # {self.consumer_num} in {self.consumer_group} RECEIVED: {id_latest} => {val_latest}')
            self.process_message(id_latest, val_latest)

    def process_message(self, message_id, message_val):
        # psedo-processing
        action = 'REFRESHED DASHBOARD'
        if (self.consumer_group == 2):
            action = 'UPDATED STATISTICS'
        elif (self.consumer_group == 3):
            action = 'SAVED HISTORICAL DATA'
        # send consumer group ack

        self.redis.xack(STREAM_NAME, self.group_name, message_id.decode("utf-8"))
        print(f'consumer # {self.consumer_num} in {self.group_name} {action}: {message_id} => {message_val}')


# initialize and start consumers
def main():
    group = sys.argv[1]
    c_num = sys.argv[2]
    consumer = StreamConsumer(REDIS_HOST, REDIS_PORT, int(group), int(c_num))
    consumer.consume()

if __name__ == "__main__":
    main()    