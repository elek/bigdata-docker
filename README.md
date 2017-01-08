# Docker images for Open Source bigdata/hadoop projects

This is the umbrella project for all of my docker images related to Apache Hadoop and other bigdata related Apache and non-apache projects.

The docker images are in separated repository:

| name                                                                     | function                                                                 |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [bigdata-base](https://github.com/elek/docker-bigdata-base)              | Special image contains base packages and the config loading scripts      |    
| [docker-hadoop](https://github.com/elek/docker-hadoop)                   | Apache Hadoop components (hdfs/yarn)
| [docker-spark](https://github.com/elek/docker-spark)                     | Apache Spark
| [docker-zeppelin](https://github.com/elek/docker-zeppelin)               | Apache Zeppelin
| [docker-zookeeper](https://github.com/elek/docker-zookeeper)             | Apache Zookeeper
| [docker-kafka](https://github.com/elek/docker-kafka)                     | Apache Kafka
| [docker-hbase](https://github.com/elek/docker-hbase)                     | Apache HBase
| [docker-phoenix](https://github.com/elek/docker-phoenix)                 | Apache Phoenix
| [docker-livy](https://github.com/elek/docker-livy)                       | Clodera Livy
| [docker-consul-composer](https://github.com/elek/docker-consul-composer) | Special image to dynamically start compose containers based on docker-compose in a Consul server

The configuration loading mechanism is defined by scripts in the docker-bigdata-base repository. The base image supports configuration loading from environment variables, Consul server, Spring config server. See the [bigdata-base](https://github.com/elek/docker-bigdata-base) repository for more details.

This repository contains example cluster configuration, using different ways to configure (environment variables, consul, spring config server) and provision (docker-compose, ansible, consul-composer) the products

## Examples

| directory        | configuration type    | docker container starter        | provisioning | cluster type  | note (*)
|------------------|-----------------------|---------------------------------|--------------|---------------|------------------
| simple[simple]   | environment variables | docker-compose                  |              | local         | Using host network
| compose[compose] | environment variables | docker-compose                  |              | local         | Using dedicated docker network
| consul           | consul                | consul-composer (docker-compose)| (ansible)    | local/cluster | Using host network
| spring           | spring config server  | docker-compose                  |              | local/cluster | Using host network
| ansible[ansible] | environment variables | docker (ansible module)         | ansible      | cluster       | Using host network

* Host network is not a limitation just the example uses this simplified approach.

## Locally with host network and docker-compose

This is the most simple option. All of the application will use the network of the localhost and the default ports will be available on the localhost. See the simple subdirectory for the docker-compose file of this option.

[simple]: https://github.com/elek/bigdata-docker/blob/master/simple/README.md
[compose]: https://github.com/elek/bigdata-docker/blob/master/compose/README.md
[ansible]: https://github.com/elek/bigdata-docker/blob/master/ansible/README.md
