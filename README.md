This is the umbrella project for all of my docker images related to Apache Hadoop and other bigdata related Apache and non-apache projects.

The docker images are in separated repository:

 * https://github.com/elek/docker-bigdata-base
 * https://github.com/elek/docker-hadoop
 * https://github.com/elek/docker-spark
 * https://github.com/elek/docker-zeppelin
 * https://github.com/elek/docker-spark

The configuration loading mechanism is defined by a script in the docker-bigdata-base repository. Usually you can set any configration value with using the config file name as prefix for the environment variable: eg. ```CORE_SITE_fs_default_name```.

This repository contains example cluster configuration, different ways how you can use the docker images.

## Locally with host network and docker-compose

This is the most simple option. All of the application will use the network of the localhost and the default ports will be available on the localhost. See the simple subdirectory for the docker-compose file of this option.

## Locally with dedicated network

This is more tricky as every component will use an own network interface on the private docker network. 

The advantage of this solution that with the right configuration you can start multiple slave components (eg. datanode, nodemanager) with docker-compose scale command.

Check the compose directory for this solution.

## Real cluster, host network, with ansible

This solution could work with a real cluster of machines. We can start the containers on different machines with ansible. The ansible example use host_network to make it easier to configure the ports/hostnames/communication.

See the scripts in the ansible directory.

### Additional tricks for ansible run
 * For ubuntu I can recommend this docker installation role: https://github.com/angstwad/docker.ubuntu
 * docker_container ansible module requires at least 2.1 version from ansible     
 * Please note that the volume path most probably should be adjust the volume path mapping
 * And you need a gateway group in the inventory and a variable gatway which should point to the gateway node (as you can see in the ansible example)
 * I recommend to use https://github.com/weaveworks/scope to visualize the cluster state
