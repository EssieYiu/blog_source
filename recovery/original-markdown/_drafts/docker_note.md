# docker 笔记

安装指南：https://yeasy.gitbooks.io/docker_practice/install/ubuntu.html

## 构建并运行

```bash
$docker build -t image_name path
```

image_name镜像名称，自行命名

path为路径，若dockerfile在当前目录下，可以使用相对路径 .

```bash
$docker run -p port1:port2 image_name
```

port1为主机端口，port2为容器开放的端口

-d选项：让容器在后台运行

-P选项，将容器内部的网络端口映射到主机任意端口

## 查看

docker images查看本地的镜像

docker ps查看正在运行的容器

## 停止和移除

docker stop

docker rm

## 进入运行中的docker

attach坏处是退出之后dockers也跟着退出

```bash
docker attach container_id
```

```bash
docker exec -it container_id /bin/bash
```

exec不会

退出docker直接

```bash
exit
```

就ok

或者ctrl+D

## docker-compose

```bash
docker-compose build
docker-compose up [-d]
```

## 删除

删除镜像docker image rm image_id

删除容器docker rm container_id

删除所有exit的容器

sudo docker rm $(sudo docker ps -qf status=exited)



## docker save

```bash
docker save [options] image_name [image...]
```

-o 输出的文件

如

```bash
docker save -o my_ubuntu.tar ubuntu_image
```

