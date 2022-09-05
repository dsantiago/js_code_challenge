#!/bin/bash

rm -f /tmp/*.pid

echo "=== STARTING SSH ==="
service ssh start

echo "=== STARTING NAMENODE AND DATANODE DAEMON ==="
if [ ! -d /data/nn/current ]; then
    $HADOOP_HOME/bin/hdfs namenode -format
    $HADOOP_HOME/sbin/hadoop-daemon.sh start namenode
    $HADOOP_HOME/sbin/hadoop-daemon.sh start datanode
    $HADOOP_HOME/sbin/start-all.sh

    hdfs dfs -mkdir /inputs && hdfs dfs -chmod 777 /inputs
    hdfs dfs -mkdir /user && hdfs dfs -chmod 755 /user
    hdfs dfs -mkdir /tmp && hdfs dfs -chmod 777 /tmp
else
    $HADOOP_HOME/sbin/hadoop-daemon.sh start namenode
    $HADOOP_HOME/sbin/hadoop-daemon.sh start datanode
    $HADOOP_HOME/sbin/start-all.sh
fi

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi

if [[ $1 == "-bash" ]]; then
  /bin/bash
fi