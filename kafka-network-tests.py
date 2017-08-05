import json
import logging
import logging.handlers
import pprint
import re
import sys
import time
from subprocess import check_call, check_output, STDOUT

from docker import Client

PROJECT_NAME = "kafkanetworkfailuretests"
ZK_COMMAND = "docker exec -t {}_zookeeper_1 env ZOO_LOG4J_PROP=WARN,CONSOLE bin/zkCli.sh".format(PROJECT_NAME).split()
TEST_TOPIC = "test-topic"


def zk_query(path, fail_on_error=True):
    zk_cmd = ZK_COMMAND + ["get", path]
    output = check_output(zk_cmd, stderr=STDOUT)
    for line in output.decode().split():
        match = re.match("^({.+})$", line)
        if match:
            return json.loads(match.group(0))
    if fail_on_error:
        raise RuntimeError("Command '{}' returned unexpected output: {}".format(zk_cmd, output))


def broker_node(broker_type):
    if broker_type == 'controller':
        broker = zk_query("/controller")['brokerid']
    else:
        state = zk_query("/brokers/topics/%s/partitions/0/state" % TEST_TOPIC)

        if broker_type == 'leader':
            broker = state['leader']
        else:
            assert len(state['isr']) > 1  # We need at least one follower isr
            broker = [isr for isr in state['isr'] if isr != state['leader']][0]  # Pick one

    containers = Client.from_env().containers(filters={'label': 'com.docker.compose.project'})
    broker_port = zk_query("/brokers/ids/%d" % broker)['port']
    for c in containers:
        if not c['Ports'] or 'PublicPort' not in c['Ports'][0]:
            pass  # Skip zookeeper, multiple ports, not all of them public
    docker_id = [c['Id'] for c in containers if c['Ports'] and c['Ports'][0].get('PublicPort') == broker_port][0]
    return broker, docker_id[:12]


def remove_all_docker_containers():
    containers = check_output("docker ps -a -q --filter label=com.docker.compose.project".split()).decode().split()
    if containers:
        check_output("docker rm -f".split() + containers)


def docker_compose(logger, cmd):
    cmd = ["docker-compose", "--project-name", PROJECT_NAME] + cmd.split()
    output = check_output(cmd, stderr=STDOUT)
    for line in output.decode().split('\n'):
        # Remove some of that pesky docker-compose output formatting
        line = re.sub(r'\x1b[[0-9]+[ABKm]', '', line)
        line = re.sub(r'^([^\r]*\r)+', '', line)
        if line:
            logger.info(line)


def setup_logging(name):
    logging.Formatter.converter = time.gmtime
    handler = logging.FileHandler(name + '.log', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def sort_dict(state):
    return pprint.pformat(state).replace('\n', '')


def do_test_producing_to_lost_leader(producer, consumer, take_down):
    """ Start a cluster, let the producer produce for a while, bring down the cluster and read the complete backlog
    to see if anything was missed """
    test_name = sys._getframe(1).f_code.co_name
    logger = setup_logging(test_name + '_main')
    logger.info("### Running " + test_name)

    logger.info("# Remove all docker containers for a clean start")
    remove_all_docker_containers()

    logger.info("# Start zookeeper and 3 kafka instances")
    docker_compose(logger, "up -d --scale kafka=3 kafka")
    logger.info("# Wait for the cluster to start")
    for _ in range(7):
        time.sleep(2)
        state = zk_query("/brokers/topics/%s/partitions/0/state" % TEST_TOPIC, fail_on_error=False)
        if state and len(state.get('isr', [])) > 1:
            logger.info(sort_dict(state))
            break

    kafka_id_controller, docker_id_controller = broker_node('controller')
    logger.info("# Kafka cluster has controller {} ({})".format(kafka_id_controller, docker_id_controller))

    kafka_id_leader, docker_id_leader = broker_node('leader')
    kafka_id_isr, docker_id_isr = broker_node('isr')
    logger.info("# Topic {} has {} ({}) as leader and {} ({}) as in sync replica".format(
                TEST_TOPIC, kafka_id_leader, docker_id_leader, kafka_id_isr, docker_id_isr))
    if docker_id_leader == docker_id_controller:
        logger.info("# Note that the leader is also controller in this cluster (affects fail-over)")
    assert kafka_id_leader != kafka_id_isr

    logger.info("# Start a producer and let it run for a while")
    docker_compose(logger, "up -d --scale kafka=3 kafka %s" % producer)
    time.sleep(10)

    logger.info("# Disable the leader on {}".format(kafka_id_leader))
    take_down(logger, docker_id_leader)

    logger.info("# Sleep for a while with the leader disconnected before checking what the producer has produced")
    for _ in range(20):
        logger.info(sort_dict(zk_query("/brokers/topics/%s/partitions/0/state" % TEST_TOPIC)))
        time.sleep(2)

    logger.info("# Stop the producer")
    docker_compose(logger, "stop --timeout 1 %s" % producer)

    logger.info("# Start the consumer")
    docker_compose(logger, "up -d --scale kafka=3 kafka %s" % consumer)

    logger.info("# Wait for 10 seconds for the consumer to consume")
    time.sleep(10)

    logger.info("# Stop the consumer")
    docker_compose(logger, "stop %s" % consumer)

    logger.info("# Logs of what the consumer consumed:\n" +
                check_output(["docker", "logs", '%s_%s_1' % (PROJECT_NAME, consumer)], stderr=STDOUT).decode())

    logger_producer = setup_logging(test_name + '_producer')
    logger_producer.info("# Logs of what the producer produced:\n" +
                         check_output(["docker", "logs", '%s_%s_1' % (PROJECT_NAME, producer)], stderr=STDOUT).decode())

    logger_isr = setup_logging(test_name + '_isr')
    logger_isr.info("# docker logs from the the new leader (%s)" % kafka_id_isr +
                    check_output(["docker", "logs", docker_id_isr], stderr=STDOUT).decode())

    print("# Test %s completed. Inspect logs to see if kafka was unavailable after leader was changed" % test_name)


def take_down_ifdown(logger, docker_id):
    logger.info("## Bring down eth0 on {}".format(docker_id))
    check_call("docker exec --privileged -t {} ifconfig eth0 down".format(docker_id).split())


def take_down_disconnect(logger, docker_id):
    logger.info("## Disconnect {} from network".format(docker_id))
    Client.from_env().disconnect_container_from_network(docker_id, "%s_default" % PROJECT_NAME, force=True)


def take_down_kill(logger, docker_id):
    logger.info("## Kill -9 {}".format(docker_id))
    Client.from_env().remove_container(docker_id, force=True)


#######
# Tests

def test_producing_to_lost_leader_using_java_producer_and_ifdown():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_ifdown)


def test_producing_to_lost_leader_using_java_producer_and_disconnect():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_disconnect)


def test_producing_to_lost_leader_using_java_producer_and_kill():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_kill)


def test_producing_to_lost_leader_using_librdkafka_producer_and_ifdown():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_ifdown)


def test_producing_to_lost_leader_using_librdkafka_producer_and_disconnect():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_disconnect)


def test_producing_to_lost_leader_using_librdkafka_producer_and_kill():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_kill)

if __name__ == '__main__':
    test_producing_to_lost_leader_using_java_producer_and_ifdown()
    test_producing_to_lost_leader_using_java_producer_and_kill()
