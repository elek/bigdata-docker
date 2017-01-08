# Docker compose based Hadoop/bigdata cluster

The example configuration from this directory use docker-compose but with dedicated bridge network. With this approach each component will get a dedicated ip from docker. 

## Run

At first time you should create a docker bridge network:

```
docker network create -d bridge hadoop
```

And you need to format the namenode volume:

```
cd hdfs
docker-compose run namenode /opt/hadoop/bin/hdfs namenode -format
```

After that you can start the components

```
cd hdfs
docker-compose up -d
cd ../yarn
docker-compose up -d
cd ../hbase
docker-compose up -d
```

The advantage of this solution that with the right configuration you can start multiple slave components (eg. datanode, nodemanager) with docker-compose scale command.

For example if you need multiple datanode:

```
docker-compose scale datanode=2
```