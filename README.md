# pwn_deploy

> A project for deploying ctf pwn challenge

中文请点击：

[README_CN.md](https://github.com/giantbranch/pwn_deploy/blob/master/README_CN.md)

This is not safe, please use [https://github.com/giantbranch/pwn_deploy_chroot](https://github.com/giantbranch/pwn_deploy_chroot)

## Before

```
# Install the latest version docker
curl -s https://get.docker.com/ | sh
# Install docker compose
apt install docker-compose
```

## Configuration

Put your pwn bin to ./bin （**Note that the filename should not contain special characters.**）

Listen port start from 10000, you can change in config.py

## Run

```
python initialize.py
# please run as root
docker-compose up --build -d
```

## Attention

The flag will be generated by the initialize.py and it store in flags.txt

The port information corresponding to the pwn program is also inside  flags.txt.


