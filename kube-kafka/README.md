## Installing persistent single instance of Kafka via Strimzi Kafka Operator
Before deploying Strimzi Kafka operator, let’s first create our kafka namespace:
```
$ kubectl create namespace kafka
```
Next we apply the Strimzi install files, including ClusterRoles, ClusterRoleBindings and some Custom Resource Definitions (CRDs). The CRDs define the schemas used for declarative management of the Kafka cluster, Kafka topics and users.
```
$ kubectl apply -f kafka-operator.yml -n kafka
```
Check operator logs:
```
$ kubectl logs deployment/strimzi-cluster-operator -n kafka -f
```
### Provision the Apache Kafka cluster
Use `kafka-persistent-single.yml` manifest it will create for us small persistent Apache Kafka Cluster with one node for each - Apache Zookeeper and Apache Kafka:
```
$ kubectl apply -f kafka-persistent-single.yml
```
Important to notice that we have `class: nfs-client` at `kafka-persistent-single.yml` manifest, in a case of installation where some kind of a persistent storage already exists this value could be deleted of changed to appropriate `storageClass` kind. We now need to wait while Kubernetes starts the required pods, services and so on.
```
$ kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka 
```
The above command might timeout if you’re downloading images over a slow connection. If that happens you can always run it again.
### Send and receive messages, test installation
Once the cluster is running, you can run a simple producer to send messages to a Kafka topic (the topic will be automatically created):
```
$ kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.28.0-kafka-3.1.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list my-cluster-kafka-bootstrap:9092 --topic my-topic
If you don't see a command prompt, try pressing enter.

>[2022-03-31 11:25:58,319] WARN [Producer clientId=console-producer] Error while fetching metadata with correlation id 1 : {my-topic=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient)
>ping
>pong
>^Cpod "kafka-producer" deleted
pod kafka/kafka-producer terminated (Error)
```
And to receive them in a different terminal you can run:
```
$ kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.28.0-kafka-3.1.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
If you don't see a command prompt, try pressing enter.


ping
pong
^CProcessed a total of 3 messages
pod "kafka-consumer" deleted
pod kafka/kafka-consumer terminated (Error)
```
Enjoy your Apache Kafka cluster, running!
