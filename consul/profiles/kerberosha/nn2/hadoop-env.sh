{% include "hadoop-env.sh" %}
export HADOOP_OPTS="$HADOOP_OPTS -Dsun.security.krb5.debug=true -Dsun.security.spnego.debug=true"
export HADOOP_JAAS_DEBUG=true
