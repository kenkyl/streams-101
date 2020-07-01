# Redis Message Patterns Code Samples

Simple code examples are provided for each of the following messaging patterns with Redis. Prerequisites to run the code examples are:
* [Python3](https://www.python.org/downloads/) installed
* Redis running at localhost:6379 
  * This can simply be a [Redis Docker container](https://hub.docker.com/_/redis) that is port-mapped to your localhost
* redis-py library installed, either globally or in a [virtual environment](https://docs.python.org/3/library/venv.html)
  * `pip install redis`

Note that the list, message channel, and stream names are all arbitrary, and they would likely follow a standardized naming convention in your implementation.

## 1. Queues
These examples show basic usage of the Redis List datatype as a message queue by calling `LPUSH` to push onto the queue and `RPOP` and `BRPOP` to pop items off for processing. 

* *list-producer.py*
  * adds random "process IDs" to a queue called *my-queue:1* every 3 seconds (**LPUSH**)
  * run once with `python list-producer.py` to continuosly append to the queue

* *list-consumer.py*
  * removes a single message from the queue (**RPOP**), prints, and exits 
  * run with `python list-consumer.py` to pop a single message from the queue
  * note: this client does NOT block, so it will return a null response if there are no items in the queue (you can test this by running it before starting the producer)

* *list-blocking-consumer.py*
  * removes a single message from the queue, sleeps for 1 second to simulate processing time, and then listens for new additions to the queue (**BRPOP**)
  * run once with `python list-blocking-producer.py` to continuously pop items off of the queue 
  * note: if you start two instances of this process (i.e. call `python list-blocking-producer.py` in a new terminal window), you should see them alternate processing messages from the queue 

## 2. Pub-Sub
To demonstrate pub-sub, the publisher and subscribers use a channel called *message-channel:2* to send and receive sample process completion methods with the `PUBLISH` and `SUBSCRIBE` commands. 

* *publisher.py*
  * sends a process completion method with a random process IDs to the channel *message-channel:2* every 3 seconds (**PUBLISH**)
  * run once with `python publisher.py` to continuosly send messages to the channel
  * note: if no one is listening to the channel, the message is "lost" (i.e. it's not saved anywhere)!

* *subscriber.py*
  * listens for incoming messages on the channel *message-channel:2*, sleeps for 1 second to simulate processing time, and then continues to listen for new messages (**(P)SUBSCRIBE**)
    * note: **PSUBSCRIBE** is used in the code to demonstrate pattern matching  to listen on multiple streams with a common prefix, but the base command **SUBSCRIBE** would typically be used to listen to a sinlge channel
  * run with `python subscriber.py` to continuously listen for new messages
    * start multiple instances of the process to see that every subscriber will receive every incoming message (fan-out)

## 3. Streams
The examples show the Redis streams capabilities of pushing of data into a stream with `XADD`, fetching incoming messages with `XREAD`, processing historical data with `XRANGE`/`XREVRANGE`, and using a consumer group. The data in each message of the sample stream are two field-value pairs indicating a random process ID and completion value, simulating a notification that certain process completed with a final value or score.

* *streams-producer.py*
  * adds a stream entry with a random process ID and "completion value" to a stream called *process-stream:3* every 3 seconds (**XADD**)
  * run once with `python streams-producer.py` to continuosly add messages to the stream

* *streams-consumer.py*
  * listens for a single message from the stream, sleeps for 1 second to simulate processing time, and then listens for new additions to the stream (**XREAD**)
    *  note: Block=0 is used to block infinitely, which is not recommended for production usage 
    * note: the '$' character is used as the ID argument to grab the newest entry on the stream, but after that the previous entry's ID is used
  * run with `python streams-consumer.py` to continuously process new messages on the stream
    * note: start multiple instances of the process to see that every streams consumer will receive every incoming message on the stream by default (fan-out)

* *streams-group-consumer.py*
  * attempts to create the consumer group (**XGROUP CREATE**), listens for a single message from the consumer group on the stream (**XREADGROUP**), sleeps for 1 second to simulate processing time, sends an acklowedgement that it has processed its message (**XACK**), and then listens for new additions to the consumer group 
    *  note: 2 command line arguments are used to determine the group name and consumer name within that group
      * they can be alphanumeric strings, but it is recommended to use a single number or digit for simplicity 
  * recommende usage:
    * run with `python streams-group-consumer.py A 1` to great consumer group 1 and consumer 1 in that group
    * run with `python streams-group-consumer.py A 2` to add consumer 2 to the group we just created 
    * note: each member of the consumer group with take turns processing messages that enter the stream 
    * note: a second consumer group with two consumers could be added by running `python streams-group-consumer.py B 1` and `python streams-group-consumer.py B 2` in two new terminal windows

* *streams-range-average.py* 
  * fetches the most recent 10 messages in the stream (**XREVRANGE**), calculates their average "completion value", prints and exits 
  * this demonstrates the capability to fetch and process historical data in a Redis Stream 
  * note: **XRANGE** can be used to grab a range starting with older messages in the stream 
  * run once `python streams-range-average.py` to calculate the average completion value of the 10 most recent messages in the stream