import redis
import random
import time

# consts
STREAM_NAME = 'my-stream'


# class to produce data 
class StreamProducer:
    def __init__(self, redis_host, redis_port, num_consumers):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.num_consumers = num_consumers

    # listen and produce indefinitely
    def produce(self):
        random.seed()
        while True:
            group = random.randint(1, self.num_consumers)
            data = {
                'temp-sensor': random.uniform(65.0, 75.0)
            }
            print(f'producer sending data: {data}')
            # XADD my-stream * temp-sensor <num>
            self.redis.xadd(STREAM_NAME, data, id='*')
            # send every three seconds
            time.sleep(3)

# initialize and start consumers
def main():
    producer = StreamProducer(REDIS_HOST, REDIS_PORT, 1)
    producer.produce()

if __name__ == "__main__":
    main()    
