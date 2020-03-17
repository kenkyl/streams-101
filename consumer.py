import redis

# consts
STREAM_NAME = 'my-stream'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379 

class StreamConsumer:
    def __init__(self, redis_host, redis_port, consumer_group):
        self.consumer_group = consumer_group
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.streams = {
            STREAM_NAME: 0
        }

    # listen and consume indefinitely
    def consume(self):
        while True:
            # XREAD STREAMS my-stream <num>
            update = self.redis.xread(self.streams, block=5000)
            print(f'consumer #{self.consumer_group} received: {update}')
            listened = update[len(update)-1]
            samples = listened[len(listened)-1]
            id_latest, val_latest = samples[len(samples)-1]
            # update streams
            self.streams = {
                STREAM_NAME: id_latest
            }

# initialize and start consumers
def main():
    consumer = StreamConsumer(REDIS_HOST, REDIS_PORT, 1)
    consumer.consume()

if __name__ == "__main__":
    main()    