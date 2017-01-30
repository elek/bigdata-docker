docker cp keytab.generate krb5:/data/
docker exec -it krb5 bash -c 'rm /data/*.keytab'
docker exec -it krb5 bash -c 'cd /data && ./keytab.generate'
./keys.sh
docker cp sc.dn.keystore krb5:/data/ 
