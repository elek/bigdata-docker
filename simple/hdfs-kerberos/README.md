
Example for kerberized HDFS cluster.


```
docker-compose up -d krb5
docker-compose exec krb5 /root/keytab.generate

#Check the hostname with using hostnetwork
docker-compose exec krb5 hostname

#Modify the .env to use the hostname from the previous output

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

