#!/bin/bash -e
file_path="/www/ScMonitor/main.py"
#进程号
PROCESS=$(ps -ef | grep $file_path | grep python | grep -v grep | grep -v PPID | awk '{ print $2}')

for i in $PROCESS; do
    echo "结束进程 [ $i ]"
    kill -9 "$i"
done

nohup python -u $file_path prod >out.log 2>&1 &
echo 启动监控程序
tail -f out.log
