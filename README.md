## DOCKER and Kurbuentues
- Containers is a light way to "bundel" an application and it's all requirements and deploy it in various places.
# Container Vs VMs
- it stated with a physical server (composed of hardwares) , installed on it an OS , and some applications
- there was a problem consists of "what if i want to deploy more than one application or service ?" does it rational to get another physical servers and pay more to get this services ? (in 60s there wasn't anyway rather this)
- for this problem the concept of virtualization comes into the play.
- so on the same server i can deploy more than a vm of different oss' running on it with different services
- to acheive such a task i needed another layer above the hardware layer called "hypervisor layer" which is the interface that tells the hardware that we have now vms and each vm need a some resources ie (it's away to virtualize the hardware components to make the vms able to share thier resources)

- The container takes the kernel of the os not all the user mood
- A container bundels the applications and it's requirements
- linux depends on the concept of containers internally in the kernel
    - cgroups / namesspaces
    - cgroups -> a way that linux/unix systems to monitor the resources that a process used and assigne resources       to a process

    - namesspaces -> a way that monitors the hierachey of a process (sub-process) (same as cgroups) ensures that        all childs process can see each other and use eachothers

- with that if you think in it you would see that linux uses this concept(starting with 1 process and that process made the os-specification [first layer] and so on....)


- i just need the kernel not the all system (how i did that , i just dived into the kernel and i found such a similar concept that do the job)

## Docker

- Docker.inc has a software called docker (such as the HYPER-V in windows or the Vm-Ware)
- There's no macosx container , there's only windows and linux containers , when installing a container it takes the host machine's kernel

- > [!IMPORTANT]
> The Docker software is available on macosx , windows , linux : but a container it self should be a linux or a windows
> when installing docker on windows , it will search for hyper-v and asks you if you want to get a linux images , if yes it will create a linux Vm and puts all the containers inside of it (not in linux :( )
> same for macosx (linux , windows)

# docker cmds
- docker container run -it alpine:latest sh -> interactive with alpine linux image (i = interactive , t = terminal)
- [LOL] new linux command cat /etc/*release* get the os release info
- docker container ls -a => shows all containers and it's status
- docker image ls => shows all container images
- `docker container run -d -p 80:80 nginx:latest` running a web service in the background and forwarding the port 80 (default port for web service) to port 80 on the host machine (exposing the port of the container to the host machine)

- `docker container stop (container name / id)` stops the running container
- By default docker socket listens on port 2375/tcp (http not-secure)

- `docker container run -it --name 'name' -h name2` change the name of the container(--name) , change the name of the host (-h)
- `docker container run -it ubunut:latest -c 'cmd'` excutes command inside the container
- `docker image / container instpect [id]` returns a json file with inspection of the image / container details.
- `docker image rm $(docker image ls -q)` removes all images from the system $(docker image ls -q) lists all images ids

# Image Naming
- hub.docker.com => default registery (cloud storage)
- the registery consits some repos => (repositories)
- a repo of an image contains it's all versions
- ubuntu:latest => the repo (ubuntu) , the tag (latest) togather is the image name.
- the official image (docker image pull (python)) well get the official image from the set.
- to get non-official images (docker image pull [account name] [image name])
- the latest version of some image `docker image pull python:latest` latest is not a tag name but it's a keyword.

# mainfest list
- a manifest list contains images with multiple architecture

# docker vs-code extention.
- for linux user (recommended)

# Notes
- if you delete the container any changes you made on the container will be deleted , and we will start again from the scratch.
- stopping a container `docker container stop` sends a [SIGTERM (signal 15 in unix)](gracefull termination) signal to PID(1) which is the process of you application running on the container, if the process doesn't exit in 10 seconds it will sends [SIGKILL (signal 9 in unix)] signal.
- kill -9 = SIGKILL , kill -15 = SIGTERM.
- when creating a container from an image (that image has many layers (read-only layers)) , the container itself is just another layer above it.

# Examples
 - `docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=P@ssw0rd" -e "MSSQL_PID=Express" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest` runs ms-sqlserver , -e is a environment variable (it debends on how the application inside the container is configured.)

# self-healing container with restart policies.
- check the arabigdata directory.


## Container networking.
- how to make 2 container see each other?
- imagine we have 2 running containers , one for nginx and other for centos
- if we tried to ping the web service (nginx) from the centos it will be okay and each of the containers will be able to see each other (As long as they're on the same host machine)
- say that nginx container has a host name which is web , if we tried to ping or curl using this name it will not recognize it.
- one (temp , non-optimal) solution is we can attach this parameter to the client (centos) container `docker container run -it --name client --add-host [web:ip] centos:latest`
the --add-host will add the ip to the `/etc/hosts` file so you will be able to access it.

# docker networking.
- docker mainly has 3 network connections type.
    1. bridge (default) (the docker0 virtual interface `ip link show | grep docker0`), the default ip address for the interface is `172.17.0.1` so each time you will create a new container it will follow this ip range `172.17.0.1 : 172.17.225.225`
    2. host
    3. none

- each time your create a new container a new adapter is created on the host machine (veth[some random values])
- each container contains 2 adapters (lo (loopback) and eth0) the eth0 adapter is forwared to the outer world on the host machine using the veth adapter which is automatically created every time you create a new container and connect it to the `bridge network`

- `docker container run -dit/-it --name alp3 --network [network type] alpine`
- this will create a container and attach it to a newtork type ... if we used the none network type this will make our container completley isolated from the outer world (it will have only the lo adapter)

- the `host` network is a special case network type ... if we created a container with a network type host `docker container run -it /-dit --name alp4 --network host alpine:latest` it will make our container exposed on the host.. actually that container will act that he's the host itself as it will grant all adapters of the host , with the same hostname...etc

- why? ... in case you have an application with many open ports , you can create a container with the host network to access all thies ports from the host without need to forward each port to the host machine.

# drivers
- there's 3 drivers on the host machine that deals with containers networking.
    1. bridge (single host containers) (NAT on windows)
    2. macvlan (multi-host containers) (acts like a physical device and the outer people will see the MAC address , to do so you need to follow the `promiscuous mode`)
    3. overlay (containers on different machines)
- `docker network create mynet` = creates a custom network (the driver will be bridge)
- `docker network connect mynet alp1` = connects a container to a network
- `docker network create --subnet 10.0.0.0/16 mynet2` = creates a newtork with a specific subnet mask
- `docker network disconnect mynet alp1` = disconnects the container from the network.
- `docker network create --internal mynet3` = creates an internal network (the containers will be able to see eachother but they will be isolated from the outer world) (usually for testing evnornment)


# Storage
- storage in containers is tow types , the non-presisting data and the presisting data.
    1. The non presisting data.
    `ls /var/lib/docker/overlay2` = the overlay2 driver is the driver responsible for storage if we ls that path you will not find anything (if you don't have any images)
    if you installed alpine (for instance) you will see after ls'ing that path that there's another directory inside of it, that directory is the base for the filesystem , every time your need to make a container the content of this file (alpine root directory) will be copied , now try to create a container , ls that basterd , now you will see 2 new directories ignore the -init one head to the otherone , go inside the diff folder , now this is the folder where stores each change (file creationg , deleation..etc) you did in the container , for instance you wrote an new file in the /tmp/file , in the diff dir you will find that path , so if you deleted that container everything will be removed .

    - how to solve this problem (how to make a presisting data)
2. presitance storage
    # 1- Bind mount.
    - you just mount a directory from the docker host (actual machine) to the docker/container path

    - `docker container run -it -v $(pwd)/code:/app/code python` this command will create a python container with -it (interactive mode) , the `-v` option stands for volume which is the mount point on my host machine ($(pwd)/code) to the mount end at the container (/app/code) , please note that even if the path /app/code isn't exist it will be created automatically. this way if you edited the file on the host machine the modifications will still occure on the docker and this solve the copy approach.

    # 2- docker volume
    - docker volume is a shared mount point to all containers
    - just like the bind mount approach but this approach is better than the bind mount as in case we want to move file from container to another , we don't have to keep track of the file path on the host machine

    - `docker volume create myvol` create a volume named myvol
    - this volume exists in the path `/var/lib/docker/volumes`
    - `docker container run -it -v myvol:/app/code python` this will attach our volume to the mount end (/app/code) on the container.
    - `docker volume ls` shows all volumes we have



## Containeralize your application
- imagine we have a python container and we want to excute a script on it .... how?
- to do so one way is to write the script on your local machine and then copy it to the container.
- so we made file.py and save it on our local machine , then we have a python:latest container running so the command used to copy files is `docker container cp file.py [containerhash]:[outputdir]`
- we are in the repl mode in python , how to excute the script...
- `exec(open('path to the file.py on container').read())`
- this approach is not effecient as each time we modefie the file we will have to copy it again to the container.

- after learning the bind mount it would be easy to do the devlopment process with containers.

- one way to containeralize your application is the following , first pull any base image for instance python , then write your code , make your configs , then convert that container to an image ... how `docker container commit [container-name] [your new image name](try to start it with your account name on docker hub , it would be easy to upload it)`

- now this image is ready to be a container and used in other environment (testing , production,..etc)
    # example
    - we will try to containerlize a flask application
    - first pick a base image (ie.python)
    - make a container , install flask frame work , install vim (for real geaks :) )
    - then write some code , convert it to an image.
    - `docker container run -dit -p 5000:5000 --name pyf martell0x1/pyflask:v1.0 python /app/hello.py` 
- this way is not optimal for editing you application as with each edit you will have to make a new container image , so this will be painfull .
