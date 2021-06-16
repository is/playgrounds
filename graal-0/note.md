```
export JAVA_HOME=/home/admin/graal/jdk-11.0.3
export PATH=$JAVA_HOME/bin:$PATH
export JAVA_TOOL_OPTIONS='-XX:+UseParallelGC -Xmx512m -Xms512m'

http://openjdk.java.net/jeps/243


export JAVA_TOOL_OPTIONS='-XX:+UseParallelGC -Xmx512m -Xms512m -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler'

java --list-modules
java --list-modules | grep jdk.interval

java -XX:+PrintFlagsFinal -version
java -XX:+PrintFlagsFinal -version | grep JVMCI

java -XX:+JVMCIPrintProperties

java -Djvmci.InitTimer=true -XX:+PrintCompilation -version

java -Djvmci.InitTimer=true -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -l

java -Djvmci.InitTimer=true \
  -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -s small avrora


JAVA_TOOL_OPTIONS='-XX:+UseParallelGC -Xmx512m -Xms512m' \
java -Djvmci.InitTimer=true \
  -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -s small -n 5 avrora

java -XX:+BootstrapJVMCI \
  -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -s small -n 5 avrora

JAVA_TOOL_OPTIONS='-XX:+UseParallelGC -Xmx512m -Xms512m' \
java -Xlog:gc \
  -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -s small -n 3 avrora

java -Xlog:class+load \
  -jar scala-benchmark-suite-0.1.0-20120216.103539-3.jar -s small -n 3 avrora

--add-modules=java.se.ee
-Xlog:class+load


export JAVA_TOOL_OPTIONS='-XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler'
```


