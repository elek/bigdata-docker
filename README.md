# Repository has been moved to https://flokkr.github.io



<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

Docker images for Open Source bigdata/hadoop projects

This is the umbrella project for all of my docker images related to Apache Hadoop and other bigdata related Apache and non-apache projects.

The docker images are in separated repository:

| name                                                                     | function                                                                 |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [bigdata-base](https://github.com/elek/docker-bigdata-base)              | Special image contains base packages and the config loading scripts      |    
| [docker-hadoop](https://github.com/elek/docker-hadoop)                   | Apache Hadoop components (hdfs/yarn)                                     |
| [docker-spark](https://github.com/elek/docker-spark)                     | Apache Spark                                                             |
| [docker-zeppelin](https://github.com/elek/docker-zeppelin)               | Apache Zeppelin                                                          |
| [docker-zookeeper](https://github.com/elek/docker-zookeeper)             | Apache Zookeeper                                                         |
| [docker-kafka](https://github.com/elek/docker-kafka)                     | Apache Kafka                                                             |
| [docker-hbase](https://github.com/elek/docker-hbase)                     | Apache HBase                                                             |
| [docker-phoenix](https://github.com/elek/docker-phoenix)                 | Apache Phoenix                                                           |
| [docker-livy](https://github.com/elek/docker-livy)                       | Cloudera Livy                                                            |
| [docker-hive](https://github.com/elek/docker-hive) (experimental)        | Apache Hive                                                              |
| [docker-storm](https://github.com/elek/docker-storm)                     | Apache Storm                                                             |
| [krb5](https://github.com/elek/docker-krb5) (for development only)       | MIT kerberos server                                                      |
| [docker-consul-composer](https://github.com/elek/docker-consul-composer) | Special image to dynamically start compose containers based on docker-compose in a Consul server |


All of the docker images contains the component extracted from the open source distribution and some advanced configuration loading mechanism.

Currently there are two main configuration use cases:

 * For using local docker-compose files we use the [envtoconf](https://github.com/elek/envtoconf) utility which converts environment variables to configuration files according to the naming convention. (eg. `CORE-SITE.XML_fs.default.name="hdfs://localhost:9000"` will be converted to a well formed hadoop xml configuration)
 *  For using a multi host environment we use the [consul-launcher](https://github.com/elek/consul-launcher) which downloads the configuration from consul and launch the specific starter. (It also listens to the changes and restart the process similar to the consul-template)

There is also a [simple python tool][consync] to upload configuration (the consul directory of this repository) to the consul (only required if consul is used for configuration management).

This repository contains example cluster configuration, using different ways to configure (environment variables, consul, spring config server) and provision (docker-compose, ansible, consul-composer) the products

## Examples

| directory              | configuration type    | docker container starter        | provisioning                                  | cluster type  | network (*)                    |
|------------------------|-----------------------|---------------------------------|-----------------------------------------------|---------------|--------------------------------|
| [simple][simple]       | environment variables | docker-compose                  |                                               | local         | Using host network             |
| [compose][compose]     | environment variables | docker-compose                  |                                               | local         | Using dedicated docker network |
| [consul][consulconfig] | consul                | consul-composer (docker-compose)|  [consul-compose][consulcompose](+ansible)    | local/cluster | Using host network             |
| [ansible][ansible]     | environment variables | docker (ansible module)         | ansible                                       | cluster       | Using host network             |

* Host network is not a limitation just the example uses this simplified approach.

## Locally with host network and docker-compose

This is the most simple option. All of the application will use the network of the localhost and the default ports will be available on the localhost. See the simple subdirectory for the docker-compose file of this option.

[simple]: https://github.com/elek/bigdata-docker/blob/master/simple/README.md
[compose]: https://github.com/elek/bigdata-docker/blob/master/compose/README.md
[ansible]: https://github.com/elek/bigdata-docker/blob/master/ansible/README.md
[consulconfig]: https://github.com/elek/bigdata-docker-consul/blob/master/README.md
[consulcompose]: https://github.com/elek/docker-consul-compose
[consync]: https://github.com/elek/consync
