#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 14:01:13
# @Author  : giantbranch (giantbranch@gmail.com)
# @Link    : http://www.giantbranch.cn/
# @tags : 

FLAG_BAK_FILENAME = "flags.txt"
PWN_BIN_PATH = "./bin"
XINETD_CONF_FILENAME = "pwn.xinetd"
PORT_LISTEN_START_FROM = 10000

XINETD = '''service ctf
{
    disable = no
    socket_type = stream
    protocol    = tcp
    wait        = no
    user        = %s
    type        = UNLISTED
    port        = %d
    bind        = 0.0.0.0
    server      = %s   
    # safety options
    per_source  = 10 # the maximum instances of this service per source IP address
    rlimit_cpu  = 20 # the maximum number of CPU seconds that the service may use
    rlimit_as  = 100M # the Address Space resource limit for the service
    #access_times = 2:00-9:00 12:00-24:00
}

'''

DOCKERFILE = '''FROM ubuntu:16.04

RUN sed -i 's/archive.ubuntu.com/asia-east1.gce.archive.ubuntu.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd
#apt update && apt-get install -y lib32z1 xinetd

COPY ./'''+ XINETD_CONF_FILENAME +''' /etc/xinetd.d/pwn

COPY ./service.sh /service.sh

RUN chmod +x /service.sh

# useradd and put flag
%s

# copy bin
%s

# chown & chmod
%s

CMD ["/service.sh"]
'''

DOCKERCOMPOSE = '''version: '2'
services:
 pwn_deploy:
   image: pwn_deploy:latest
   build: .
   container_name: pwn_deploy
   ports:
    %s
'''

