#!/bin/sh

JAVA_OPTS="-Djava.security.auth.login.config=./m1.conf -Djava.security.krb5.conf=/etc/krb5.conf"
JAVA_OPTS="$JAVA_OPTS -Dsun.security.krb5.debug=true"
java -cp $(cat .cp):target/classes $JAVA_OPTS us.yuxin.demo.jsch.JschKrb5 host0 22
