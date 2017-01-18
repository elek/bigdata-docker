keytool -genkey -keystore sc.dn.keystore -keyalg RSA -alias dn -dname "CN=sc,O=Hadoop"  -keypass Welcome1 -storepass Welcome1
keytool -exportcert -keystore sc.dn.keystore -alias dn -file dn.cert -storepass Welcome1
keytool -import -keystore hadoop.truststore -alias dn -file dn.cert -noprompt -storepass Welcome1

