#!/bin/sh
#git pull
#mvn -DskipTests=true package
JAVA_OPT="-Djava.security.auth.login.config=./m0.conf -Djava.security.krb5.conf=/etc/krb5.conf"
#export MAVEN_OPTS="-Djava.security.krb5.conf=/etc/krb5.conf"
#mvn exec:java -Dexec.mainClass="us.yuxin.demo.jsch.Krb5Init"
java -cp $(cat .cp):target/classes $JAVA_OPT us.yuxin.demo.jsch.Krb5Init
