# syntax = docker/dockerfile:1.3
FROM ubuntu:22.10
#  -e 's/security.ubuntu.com/mirrors.aliyun.com/g' \
#  -e 's/archive.ubuntu.com/mirrors.aliyun.com/g' \
#  -e 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' \
#  -e 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' \


RUN \
 --mount=type=cache,target=/var/cache/apt \
 --mount=type=cache,target=/var/lib/apt \
 rm -f /etc/apt/apt.conf.d/docker-clean && \
 echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
  > /etc/apt/apt.conf.d/keep-cache && \
 sed -i \
  -e 's/security.ubuntu.com/mirrors.aliyun.com/g' \
  -e 's/archive.ubuntu.com/mirrors.aliyun.com/g' \
  /etc/apt/sources.list && \
 apt-get update -y && apt-get upgrade -y && \
 apt-get install -y git curl python3 ffmpeg python3-pip vim \
  s3fs rsync rclone && \
 #apt-get clean all && \
 #rm -rf /var/lib/apt/lists/*
 echo "package ok."

RUN --mount=type=bind,source=setup/ffmpeg,target=/setup \
 curl -s -o /usr/bin/ossutil https://gosspublic.alicdn.com/ossutil/1.7.7/ossutil64 && \
 chmod a+x /usr/bin/ossutil && \
 /setup/pip
 
