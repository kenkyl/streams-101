from .consumer import StreamConsumer
from .producer import StreamProducer
import os

# constants
REDIS_HOST = 'localhost'
REDIS_PORT = 6379 

def main():
    producer = StreamProducer(REDIS_HOST, REDIS_PORT, 1)
    consumer = StreamConsumer(REDIS_HOST, REDIS_PORT, 1)
    


if __name__ == "__main__":
    main()    