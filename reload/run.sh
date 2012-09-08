#!/bin/sh

export CLASSPATH=lib/guava-11.0.2.jar

rm -fr o
mkdir -p o/{m,0,1,s}

javac -Xlint:deprecation -s main -d o/m main/*.java
javac -Xlint:deprecation -cp o/m -s 0 -d o/0 0/*.java
javac -Xlint:deprecation -cp o/m -s 1 -d o/1 1/*.java

java -cp lib/guava-11.0.2.jar:o/m Main
