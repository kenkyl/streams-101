import redis

# consts
STREAMS = {
    'my-stream': 0
}
REDIS_HOST = 'localhost'
REDIS_PORT = 6379 

class StreamConsumer:
    def __init__(self, redis_host, redis_port, consumer_group):
        self.consumer_group = consumer_group
        self.redis = redis.Redis(host=redis_host, port=redis_port)

    # listen and consume indefinitely
    def consume(self):
        while True:
            update = self.redis.xread(STREAMS, block=5000)
            print(f'consumer #{self.consumer_group} received: {update}')

# initialize and start consumers
def main():
    consumer = StreamConsumer(REDIS_HOST, REDIS_PORT, 1)
    consumer.consume()

if __name__ == "__main__":
    main()    