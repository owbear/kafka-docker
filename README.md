kafka-network-failure-tests
===========================

A suite of tests of kafka in failing network. Based on [https://github.com/wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker).
Please refer to the [original README.md](https://github.com/wurstmeister/kafka-docker/README.md) for information on how to build and configure the image.

## Pre-Requisites

- install docker-compose [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- install docker-py [https://github.com/docker/docker-py/](https://pypi.python.org/pypi/docker/)
- modify ```ZK_BIN_PATH``` in ```kafka-network-tests.py``` to point to your kafka installation
- if you want to customize any Kafka parameters, simply add them as environment variables in ```docker-compose.yml```, e.g. in order to increase the ```message.max.bytes``` parameter set the environment to

## Running the tests

- run all tests: ```py.test -s kafka-network-tests.py```
- run individual tests: ```py.test -s kafka-network-tests.py -k test_producing_to_lost_leader_using_java_producer_and_ifdown```
- run individual tests: ```py.test -s kafka-network-tests.py -k test_producing_to_lost_leader_using_librdkafka_producer_and_ifdown```

## Sample results

The test with [the java producer and ifdown](test_producing_to_lost_leader_using_java_producer_and_ifdown_producer.log) shows that there's a 9-23 seconds long gap where no values were stored in the log after the network was taken down.

The test with [the librdkafka producer and ifdown](test_producing_to_lost_leader_using_librdkafka_producer_and_ifdown_main.log) shows that no values was stored in the log after the network was taken down at.

