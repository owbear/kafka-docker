#!/bin/bash
DOCKER_CMD="docker run --rm -v /var/run/docker.sock:/var/run/docker.sock --net=kafkanetworkfailuretests_default -e BROKERS=kafkanetworkfailuretests_kafka_1:9092,kafkanetworkfailuretests_kafka_2:9092,kafkanetworkfailuretests_kafka_3:9092 -e ZK=kafkanetworkfailuretests_zookeeper_1:2181 -i -t wurstmeister/kafka:0.11.0.0"
if [[ $# == 0 ]]; then
  $DOCKER_CMD /bin/bash
else
  $DOCKER_CMD /bin/bash -c "$*"
fi
