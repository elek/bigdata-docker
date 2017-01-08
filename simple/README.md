# Simple configuration
This is the most simple option to run docker based hadoop cluster locally.
 
All of the application will use the network of the localhost (host networking) and the default ports will be available on the localhost (so you can't start multiple datanode without additional configuration. 

## Run

You need to format the namenode at the first time:
```
docker-compose run namenode /opt/hadoop/bin/hdfs namenode -format
```

After that you can start all the docker containers.

```
docker-compose up
```

For test, check the defaults ports of the components. Eg.:

 * [Namenode web ui](http://localhost:50070)
 * [Yarn web ui](http://localhost:8080)

