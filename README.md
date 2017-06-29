kafka-network-failure-tests
===========================

A suite of tests of kafka in failing network. Based on [https://github.com/wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker)

## Pre-Requisites

- install docker-compose [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- install docker-py [https://github.com/docker/docker-py/](https://pypi.python.org/pypi/docker/)
- modify ```ZK_BIN_PATH``` in ```kafka-network-tests.py``` to point to your kafka installation
- if you want to customize any Kafka parameters, simply add them as environment variables in ```docker-compose.yml```, e.g. in order to increase the ```message.max.bytes``` parameter set the environment to

## Running the tests

- run all tests: ```py.test-3 -s kafka-network-tests.py```
- run individual tests: ```py.test-3 -s kafka-network-tests.py -k test_producing_to_lost_leader_using_librdkafka_producer```

## Sample results

The first test shows that while the producer produced values between ```12:33:30``` and ```12:33:52```, no values was stored in the log after the network was taken down at ```12:33:40```.

```kafka-network-tests.py:107: test_producing_to_lost_leader_using_librdkafka_producer
Thu Jun 29 12:33:02 UTC 2017: # Remove all docker containers for a clean start
Thu Jun 29 12:33:03 UTC 2017: # Start zookeeper and 3 kafka instances
Creating kafkanetworkfailuretests_zookeeper_1 ... 
Creating kafkanetworkfailuretests_zookeeper_1 ... done
Creating kafkanetworkfailuretests_kafka_1 ... 
Creating kafkanetworkfailuretests_kafka_2 ... 
Creating kafkanetworkfailuretests_kafka_3 ... 
Creating kafkanetworkfailuretests_kafka_1 ... done
Creating kafkanetworkfailuretests_kafka_2 ... done
Creating kafkanetworkfailuretests_kafka_3 ... done
Thu Jun 29 12:33:05 UTC 2017: # Wait for the cluster to start
Thu Jun 29 12:33:29 UTC 2017: # Kafka cluster started, topic test-topic has 1003 (3f33a18422cd4a06acabe3e819787072801c41103e280c2b0ab960f15195ab07) as leader and 1003 (ac59d8b97dbe8f0d92a8e962b1d9e00d49f5ee5cb1727c7ef95c8ec5a1ad590f) as in sync replica
Thu Jun 29 12:33:29 UTC 2017: # Start a producer and let it run for a while
kafkanetworkfailuretests_zookeeper_1 is up-to-date
kafkanetworkfailuretests_kafka_1 is up-to-date
kafkanetworkfailuretests_kafka_2 is up-to-date
kafkanetworkfailuretests_kafka_3 is up-to-date
Creating kafkanetworkfailuretests_producer_librdkafka_1 ... 
Creating kafkanetworkfailuretests_producer_librdkafka_1 ... done
Thu Jun 29 12:33:40 UTC 2017: $ Bring down eth0 on leader 1002 (docker id: 3f33a18422cd4a06acabe3e819787072801c41103e280c2b0ab960f15195ab07)
Thu Jun 29 12:33:40 UTC 2017: # Sleep for a while with the leader disconnected before checking what the producer has produced
Thu Jun 29 12:33:50 UTC 2017: # Stop the producer
Stopping kafkanetworkfailuretests_producer_librdkafka_1 ... done
Thu Jun 29 12:33:52 UTC 2017: # Start the consumer
kafkanetworkfailuretests_zookeeper_1 is up-to-date
kafkanetworkfailuretests_kafka_1 is up-to-date
kafkanetworkfailuretests_kafka_2 is up-to-date
kafkanetworkfailuretests_kafka_3 is up-to-date
Creating kafkanetworkfailuretests_consumer_java_1 ... 
Creating kafkanetworkfailuretests_consumer_java_1 ... done
Thu Jun 29 12:33:53 UTC 2017: # Wait for 3 minutes for the consumer to consume (it can take even longer)
Thu Jun 29 12:36:53 UTC 2017: # Stop the consumer
Stopping kafkanetworkfailuretests_consumer_java_1 ... done
Thu Jun 29 12:37:04 UTC 2017: # Logs of what the producer produced and consumer consumed
Attaching to kafkanetworkfailuretests_consumer_java_1
consumer_java_1        | Thu Jun 29 12:33:53 UTC 2017 Starting java consumer
consumer_java_1        | Thu Jun 29 12:33:30 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:31 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:31 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:32 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:32 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:33 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:33 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:34 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:34 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:35 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:35 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:36 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:36 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:37 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:37 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:38 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:38 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:39 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:39 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
consumer_java_1        | Thu Jun 29 12:33:40 UTC 2017 [received Thu Jun 29 12:34:11 UTC 2017]
Attaching to kafkanetworkfailuretests_producer_librdkafka_1
producer_librdkafka_1  | Thu Jun 29 12:33:30 UTC 2017 Starting librdkafka producer
producer_librdkafka_1  | Thu Jun 29 12:33:30 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:31 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:31 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:32 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:32 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:33 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:33 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:34 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:34 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:35 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:35 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:36 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:36 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:37 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:37 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:38 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:38 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:39 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:39 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:40 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:40 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:41 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:41 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:42 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:42 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:43 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:43 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:44 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:44 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:45 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:45 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:46 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:46 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:47 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:47 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:48 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:48 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:49 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:49 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:50 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:51 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:51 UTC 2017
producer_librdkafka_1  | Thu Jun 29 12:33:52 UTC 2017
PASSED
```

The second test shows that while the producer produced values between ```12:37:33``` and ```12:37:54```, theres a gap between ```12:37:41`` and ```12:37:50``` where no values was stored in the log after the network was taken down at ```12:37:42```:

```
kafka-network-tests.py:111: test_producing_to_lost_leader_using_java_producer
Thu Jun 29 12:37:05 UTC 2017: # Remove all docker containers for a clean start
ce5faf4ece8a
cff580e26796
ac59d8b97dbe
3f33a18422cd
5291aa2c1598
d3f6624c6fe1
Thu Jun 29 12:37:06 UTC 2017: # Start zookeeper and 3 kafka instances
Creating kafkanetworkfailuretests_zookeeper_1 ... 
Creating kafkanetworkfailuretests_zookeeper_1 ... done
Creating kafkanetworkfailuretests_kafka_1 ... 
Creating kafkanetworkfailuretests_kafka_2 ... 
Creating kafkanetworkfailuretests_kafka_3 ... 
Creating kafkanetworkfailuretests_kafka_1 ... done
Creating kafkanetworkfailuretests_kafka_2 ... done
Creating kafkanetworkfailuretests_kafka_3 ... done
Thu Jun 29 12:37:08 UTC 2017: # Wait for the cluster to start
Thu Jun 29 12:37:31 UTC 2017: # Kafka cluster started, topic test-topic has 1001 (91d563f4650a7b396fb4b4fc6d4f0444b43451c035e7f57c800a1b7218cb8c36) as leader and 1001 (f2a471f104e7a2637cb7181aac961133c43de8320b48421248c9ba36e0a45677) as in sync replica
Thu Jun 29 12:37:31 UTC 2017: # Start a producer and let it run for a while
kafkanetworkfailuretests_zookeeper_1 is up-to-date
kafkanetworkfailuretests_kafka_1 is up-to-date
kafkanetworkfailuretests_kafka_2 is up-to-date
kafkanetworkfailuretests_kafka_3 is up-to-date
Creating kafkanetworkfailuretests_producer_java_1 ... 
Creating kafkanetworkfailuretests_producer_java_1 ... done
Thu Jun 29 12:37:42 UTC 2017: $ Bring down eth0 on leader 1003 (docker id: 91d563f4650a7b396fb4b4fc6d4f0444b43451c035e7f57c800a1b7218cb8c36)
Thu Jun 29 12:37:42 UTC 2017: # Sleep for a while with the leader disconnected before checking what the producer has produced
Thu Jun 29 12:37:52 UTC 2017: # Stop the producer
Stopping kafkanetworkfailuretests_producer_java_1 ... done
Thu Jun 29 12:37:54 UTC 2017: # Start the consumer
kafkanetworkfailuretests_zookeeper_1 is up-to-date
kafkanetworkfailuretests_kafka_1 is up-to-date
kafkanetworkfailuretests_kafka_2 is up-to-date
kafkanetworkfailuretests_kafka_3 is up-to-date
Creating kafkanetworkfailuretests_consumer_java_1 ... 
Creating kafkanetworkfailuretests_consumer_java_1 ... done
Thu Jun 29 12:37:55 UTC 2017: # Wait for 3 minutes for the consumer to consume (it can take even longer)
Thu Jun 29 12:40:55 UTC 2017: # Stop the consumer
Stopping kafkanetworkfailuretests_consumer_java_1 ... done
Thu Jun 29 12:41:06 UTC 2017: # Logs of what the producer produced and consumer consumed
Attaching to kafkanetworkfailuretests_consumer_java_1
consumer_java_1        | Thu Jun 29 12:37:55 UTC 2017 Starting java consumer
consumer_java_1        | Thu Jun 29 12:37:33 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:33 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:34 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:34 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:35 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:35 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:36 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:36 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:37 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:37 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:38 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:38 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:39 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:39 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:40 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:40 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:41 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:41 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:50 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:50 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:51 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:51 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:52 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:52 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:53 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
consumer_java_1        | Thu Jun 29 12:37:53 UTC 2017 [received Thu Jun 29 12:38:13 UTC 2017]
Attaching to kafkanetworkfailuretests_producer_java_1
producer_java_1        | Thu Jun 29 12:37:32 UTC 2017 Starting java producer
producer_java_1        | Thu Jun 29 12:37:33 UTC 2017
producer_java_1        | Thu Jun 29 12:37:33 UTC 2017
producer_java_1        | Thu Jun 29 12:37:34 UTC 2017
producer_java_1        | Thu Jun 29 12:37:34 UTC 2017
producer_java_1        | Thu Jun 29 12:37:35 UTC 2017
producer_java_1        | Thu Jun 29 12:37:35 UTC 2017
producer_java_1        | Thu Jun 29 12:37:36 UTC 2017
producer_java_1        | Thu Jun 29 12:37:36 UTC 2017
producer_java_1        | Thu Jun 29 12:37:37 UTC 2017
producer_java_1        | Thu Jun 29 12:37:37 UTC 2017
producer_java_1        | Thu Jun 29 12:37:38 UTC 2017
producer_java_1        | Thu Jun 29 12:37:38 UTC 2017
producer_java_1        | Thu Jun 29 12:37:39 UTC 2017
producer_java_1        | Thu Jun 29 12:37:39 UTC 2017
producer_java_1        | Thu Jun 29 12:37:40 UTC 2017
producer_java_1        | Thu Jun 29 12:37:40 UTC 2017
producer_java_1        | Thu Jun 29 12:37:41 UTC 2017
producer_java_1        | Thu Jun 29 12:37:41 UTC 2017
producer_java_1        | Thu Jun 29 12:37:42 UTC 2017
producer_java_1        | Thu Jun 29 12:37:42 UTC 2017
producer_java_1        | Thu Jun 29 12:37:43 UTC 2017
producer_java_1        | Thu Jun 29 12:37:43 UTC 2017
producer_java_1        | Thu Jun 29 12:37:44 UTC 2017
producer_java_1        | Thu Jun 29 12:37:44 UTC 2017
producer_java_1        | [2017-06-29 12:37:45,266] WARN Got error produce response with correlation id 14 on topic-partition test-topic-0, retrying (2 attempts left). Error: NETWORK_EXCEPTION (org.apache.kafka.clients.producer.internals.Sender)
producer_java_1        | [2017-06-29 12:37:45,266] WARN Got error produce response with correlation id 13 on topic-partition test-topic-0, retrying (2 attempts left). Error: NETWORK_EXCEPTION (org.apache.kafka.clients.producer.internals.Sender)
producer_java_1        | Thu Jun 29 12:37:45 UTC 2017
producer_java_1        | Thu Jun 29 12:37:45 UTC 2017
producer_java_1        | Thu Jun 29 12:37:46 UTC 2017
producer_java_1        | Thu Jun 29 12:37:46 UTC 2017
producer_java_1        | Thu Jun 29 12:37:47 UTC 2017
producer_java_1        | [2017-06-29 12:37:47,284] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 2 record(s) for test-topic-0: 1917 ms has passed since last attempt plus backoff time
producer_java_1        | [2017-06-29 12:37:47,285] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 2 record(s) for test-topic-0: 1917 ms has passed since last attempt plus backoff time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 2 record(s) for test-topic-0: 1919 ms has passed since last attempt plus backoff time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 2 record(s) for test-topic-0: 1919 ms has passed since last attempt plus backoff time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:47,286] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 7 record(s) for test-topic-0: 2022 ms has passed since batch creation plus linger time
producer_java_1        | Thu Jun 29 12:37:47 UTC 2017
producer_java_1        | Thu Jun 29 12:37:48 UTC 2017
producer_java_1        | Thu Jun 29 12:37:48 UTC 2017
producer_java_1        | Thu Jun 29 12:37:49 UTC 2017
producer_java_1        | Thu Jun 29 12:37:49 UTC 2017
producer_java_1        | [2017-06-29 12:37:50,297] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 5 record(s) for test-topic-0: 1506 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:50,297] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 5 record(s) for test-topic-0: 1506 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:50,298] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 5 record(s) for test-topic-0: 1506 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:50,298] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 5 record(s) for test-topic-0: 1506 ms has passed since batch creation plus linger time
producer_java_1        | [2017-06-29 12:37:50,298] ERROR Error when sending message to topic test-topic with key: null, value: 28 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)
producer_java_1        | org.apache.kafka.common.errors.TimeoutException: Expiring 5 record(s) for test-topic-0: 1506 ms has passed since batch creation plus linger time
producer_java_1        | Thu Jun 29 12:37:50 UTC 2017
producer_java_1        | Thu Jun 29 12:37:50 UTC 2017
producer_java_1        | Thu Jun 29 12:37:51 UTC 2017
producer_java_1        | Thu Jun 29 12:37:51 UTC 2017
producer_java_1        | Thu Jun 29 12:37:52 UTC 2017
producer_java_1        | Thu Jun 29 12:37:52 UTC 2017
producer_java_1        | Thu Jun 29 12:37:53 UTC 2017
producer_java_1        | Thu Jun 29 12:37:53 UTC 2017
producer_java_1        | Thu Jun 29 12:37:54 UTC 2017
PASSED
```

