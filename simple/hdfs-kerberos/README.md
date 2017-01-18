
Example for kerberized HDFS cluster.


```
docker-compose up -d krb5
docker-compose exec krb5 /root/keytab.generate

#Check the hostname with using hostnetwork
docker-compose exec krb5 hostname

#Modify the .env to use the hostname from the previous output

docker-compose run namenode /opt/hadoop/bin/hdfs namenode -format

docker-compose up namenode
docker-compose up datanode
```

From the client machine (you need the krb5.conf):

```
kinit admin/admin
klist
curl -v --negotiate -u : "http://sc:50070/webhdfs/v1/?op=LISTSTATUS&user.name=root"
klist
```

Note: for OSX you may need to fix the hostname resolution for the moby hostname:

```
screen  ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
```

And add moby to the 127.0.0.1 in /etc/hosts
