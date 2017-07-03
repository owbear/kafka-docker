import json
import re
from subprocess import check_call, check_output, Popen, PIPE
import time
from docker import Client


ZK_BIN_PATH = "/tmp/kafka_2.12-0.10.2.1/bin/kafka-run-class.sh"
TEST_TOPIC = "test-topic"


def zk_query(path, fail_on_error=False):
    zk_cmd = [ZK_BIN_PATH, "kafka.tools.ZooKeeperMainWrapper", "get", path]
    output, errors = Popen(zk_cmd, universal_newlines=True, stdout=PIPE, stderr=PIPE).communicate()
    for line in output.split():
        match = re.match("^({.+})$", line)
        if match:
            return json.loads(match.group(0))
    if fail_on_error:
        raise RuntimeError("Command '{}' failed with: {}".format(zk_cmd, errors))


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
        check_call("docker rm -f".split() + containers)


def log_in_utc(str):
    import datetime
    date = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y")
    print("{}: {}".format(date, str))


def docker_compose(cmd):
    check_call(["docker-compose", "--project-name", "kafkanetworkfailuretests"] + cmd.split())


def do_test_producing_to_lost_leader(producer, consumer, take_down):
    """ Start a cluster, let the producer produce for a while, bring down the cluster and read the complete backlog
    to see if anything was missed """

    log_in_utc("# Remove all docker containers for a clean start")
    remove_all_docker_containers()

    log_in_utc("# Start zookeeper and 3 kafka instances")
    docker_compose("up -d --scale kafka=3 kafka")
    log_in_utc("# Wait for the cluster to start")
    for _ in range(7):
        time.sleep(2)
        state = zk_query("/brokers/topics/%s/partitions/0/state" % TEST_TOPIC, fail_on_error=False)
        if state and len(state.get('isr', [])) > 1:
            log_in_utc(state)
            break

    kafka_id_controller, docker_id_controller = broker_node('controller')
    log_in_utc("# Kafka cluster has controller {} ({})".format(kafka_id_controller, docker_id_controller))

    kafka_id_leader, docker_id_leader = broker_node('leader')
    kafka_id_isr, docker_id_isr = broker_node('isr')
    log_in_utc("# Topic {} has {} ({}) as leader and {} ({}) as in sync replica".format(
               TEST_TOPIC, kafka_id_leader, docker_id_leader, kafka_id_isr, docker_id_isr))
    assert kafka_id_leader != kafka_id_isr

    log_in_utc("# Start a producer and let it run for a while")
    docker_compose("up -d --scale kafka=3 kafka %s" % producer)
    time.sleep(10)

    take_down(docker_id_leader)

    log_in_utc("# Sleep for a while with the leader disconnected before checking what the producer has produced")
    for _ in range(20):
        log_in_utc(zk_query("/brokers/topics/%s/partitions/0/state" % TEST_TOPIC))
        time.sleep(2)

    log_in_utc("# Stop the producer")
    docker_compose("stop --timeout 1 %s" % producer)

    log_in_utc("# Start the consumer")
    docker_compose("up -d --scale kafka=3 kafka %s" % consumer)

    log_in_utc("# Wait for 3 minutes for the consumer to consume (it can take even longer)")
    time.sleep(180)

    log_in_utc("# Stop the consumer")
    docker_compose("stop %s" % consumer)

    log_in_utc("# Logs of what the producer produced and consumer consumed")
    docker_compose("logs --timestamps %s" % consumer)
    docker_compose("logs --timestamps %s" % producer)
    check_call(["docker", "logs", docker_id_isr])


def take_down_ifdown(docker_id):
    log_in_utc("# Bring down eth0 on {}".format(docker_id))
    check_call("docker exec --privileged -t {} ifconfig eth0 down".format(docker_id).split())


def take_down_disconnect(docker_id):
    log_in_utc("# Disconnect {} from network".format(docker_id))
    Client.from_env().disconnect_container_from_network(docker_id, "kafkanetworkfailuretests_default", force=True)


def take_down_kill(docker_id):
    log_in_utc("# Kill -9 {}".format(docker_id))
    Client.from_env().remove_container(docker_id, force=True)


#######
# Tests


def test_producing_to_lost_leader_using_librdkafka_producer_and_ifdown():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_ifdown)


def test_producing_to_lost_leader_using_librdkafka_producer_and_disconnect():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_disconnect)


def test_producing_to_lost_leader_using_librdkafka_producer_and_kill():
    do_test_producing_to_lost_leader("producer_librdkafka", "consumer_java", take_down_kill)


def test_producing_to_lost_leader_using_java_producer_and_ifdown():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_ifdown)


def test_producing_to_lost_leader_using_java_producer_and_disconnect():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_disconnect)


def test_producing_to_lost_leader_using_java_producer_and_kill():
    do_test_producing_to_lost_leader("producer_java", "consumer_java", take_down_kill)
