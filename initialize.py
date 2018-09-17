#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 14:32:32
# @Author  : giantbranch (giantbranch@gmail.com)
# @Link    : http://www.giantbranch.cn/
# @tags : 

from config import *
import os
import uuid

def getFileList():
    filelist = []
    for filename in os.listdir(PWN_BIN_PATH):
        filelist.append(filename)
    filelist.reverse()
    return filelist

def generateFlags(filelist):
    tmp = ""
    flags = []
    if os.path.exists(FLAG_BAK_FILENAME):
        os.remove(FLAG_BAK_FILENAME)
    with open(FLAG_BAK_FILENAME, 'a') as f:
        for filename in filelist:
            tmp = "flag{" + str(uuid.uuid4()) + "}"
            f.write(filename + ": " + tmp + "\n")
            flags.append(tmp)
    return flags

def generateXinetd(filelist):
    port = PORT_LISTEN_START_FROM
    conf = ""
    for filename in filelist:
        conf += XINETD % (filename, port, "/home/" + filename + "/" + filename)
        port = port + 1
    with open(XINETD_CONF_FILENAME, 'w') as f:
            f.write(conf)

def generateDockerfile(filelist, flags):
    conf = ""
    # useradd and put flag
    runcmd = "RUN "
    
    for filename in filelist:
        runcmd += "useradd -m " + filename + " && "
   
    for x in xrange(0, len(filelist)):
        if x == len(filelist) - 1:
            runcmd += "echo '" + flags[x] + "' > /home/" + filelist[x] + "/flag.txt" 
        else:
            runcmd += "echo '" + flags[x] + "' > /home/" + filelist[x] + "/flag.txt" + " && "
    # print runcmd 

    # copy bin
    copybin = ""
    for filename in filelist:
        copybin += "COPY " + PWN_BIN_PATH + "/" + filename  + " /home/" + filename + "/" + filename + "\n"    
    # print copybin

    # chown & chmod
    chown_chmod = "RUN "
    for x in xrange(0, len(filelist)):
        chown_chmod += "chown -R root:" + filelist[x] + " /home/" + filelist[x] + " && "
        chown_chmod += "chmod -R 750 /home/" + filelist[x] + " && "
        if x == len(filelist) - 1:
            chown_chmod += "chmod 740 /home/" + filelist[x] + "/flag.txt"
        else:
            chown_chmod += "chmod 740 /home/" + filelist[x] + "/flag.txt" + " && "
    # print chown_chmod
    conf = DOCKERFILE % (runcmd, copybin, chown_chmod)

    with open("Dockerfile", 'w') as f:
        f.write(conf)

def generateDockerCompose(length):
    conf = ""
    ports = ""
    port = PORT_LISTEN_START_FROM
    for x in xrange(0,length):
        ports += "- " + str(port) + ":" + str(port) + "\n    "
        port = port + 1

    conf = DOCKERCOMPOSE % ports
    # print conf
    with open("docker-compose.yml", 'w') as f:
        f.write(conf)

def generateBinPort(filelist):
    port = PORT_LISTEN_START_FROM
    tmp = "\n"
    for filename in filelist:
        tmp += filename  + "'s port: " + str(port) + "\n"
        port = port + 1
    print tmp
    with open(FLAG_BAK_FILENAME, 'a') as f:
        f.write(tmp)

    
filelist = getFileList()
flags = generateFlags(filelist)
generateBinPort(filelist)
generateXinetd(filelist)
generateDockerfile(filelist, flags)
generateDockerCompose(len(filelist))



