# 🚀 **Containers: The Modern Way to Build, Ship, and Scale Applications** 🌐

![img](https://sue.eu/wp-content/uploads/sites/6/2022/09/1.png)

Welcome to the world of containers! Whether you're deploying a small service or managing an enterprise-level application, containers give you the power to streamline your workflow. Say goodbye to dependency issues and platform conflicts, and embrace a future where applications run consistently in any environment. Dive into Docker and Kubernetes with this repository, where simplicity meets scalability. Let's get building!
---

Welcome to the world of containers! Whether you're deploying a small service or managing an enterprise-level application, containers give you the power to streamline your workflow. Say goodbye to dependency issues and platform conflicts, and embrace a future where applications run consistently in any environment. Dive into Docker and Kubernetes with this repository, where simplicity meets scalability. Let's get building!


## DOCKER and Kubernetes
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

    # Instruction File (docker file)
    - `FROM` = telling the docker engine which image i will start with ex. `FROM python:latest`
    - `WORKDIR [dir]` = create a directory and navigate to it (mkdir dirname && cd dirname) 
    - the directory that DockerFile exist in called `build context`
    - `COPY src dist` copy a file from the build context or any other location to the container
    - `RUN [cmd]` = runs a command on the container.
    - `EXPOSE [port number]` = exposes a port on the host machine.
    - `CMD command` runs a command during the runtime of the container (the first command will be excuted in the container) (probably the only thing will be excuted)
    - [NOTE] `Any instruction that modefies the status of the container (remove , add) makes a new layer inside the image` , the `CMD` command for instance doesn't make a new layer as it is the gateway to my application it's the process that runs my application.

    - to build a container from the image , we have to excute the following command
    - `docker build -t [tagename] [DockerFile location]` ex. `docker build -t martell0x1/pyflask:v1.0 .` , this will build the image from the DockerFile with -t option which is the tage of my image and the instruction will be in DockerFile exist in my current directory , i can even give him a github repo and tell him to get the DockerFile from it, even if the file was online and was archived it will reach it.

    - how does docker container do this work?
    - it uses intermedient containers to do the jobs ie. each instruction requires making layer it makes a container and add this layer and export this container to an image , then it makes a new container of that image and do the next steps... and so on.

    - after finishing the devlopment stage , you can now make you build context (the directory that contains the Dockerfile and your code) a git repo and push it on github.

# Dockerfile Deep Dive.
- `FROM` , i can pull official /non-official , i can get the digest of an image, from another registery , private registery or scratch `FROM scratch`

- `COPY` , `COPY ["Name With Spaces.py" , "/app"] this called exec way` , `COPY file /src called shell way`

    # .dockerignore
    - .dockerignore is like .gitignore (files i don't want to include in my image) same for git files i don't want to add to my repo.

    - ex. `Dockerfile* *.pyc !important.pyc` this says don't include anyfiles named Dockerfile or any file ends with .pyc , except file called important.pyc

- `ADD` , used to copy files , that doesn't exist in my build context ie. downloading files from internet , copy a file from tar archive .. etc , ex. `ADD <url> /app`

- `SHELL` , change the shell from shell typt to another , ie. the defaul shell (sh) some people don't like dealing with and prefere using bash ... same for python from /bin/python3 to /usr/local/bin/python3 , ex. `SHELL ["/bin/bash","-c"]` | `SHELL ["/usr/local/bin/python3","-c"]`

- `RUN <command> <arg1> <arg2>` , the `RUN` command work silently without inputs such as "are you sure" , "password: " ... etc , the RUN command has 2 modes , exec mode and shell mode, in docker docs , they tell you that you should always consider using the exective mode rather than the shell mode, as you don't know the behaviour of your shell 

- sometimes you need to commands to print out something (IN BUILD Time) such as "cat 'file'" as it is usefull in debugging , as in complex dockerfiles you sometimes need to put some print statments to troubleshoot the problem and locate where the issue happend

- `ENV` (META-DATA command , doesn't add layer) , sets some environment variables and edit the meta-data of the image (inspect) ex.`ENV SQL_SA_ACCOUNT "sa"`

- `LABEL` (META-DATA command) , sets some labels for your image , ex. `LABEL author="Marwan"` , `LABEL is_dev = true is_alive = true`.

- `USER` in default when creating a container the default user is the superuser of the base system (root in linux , ADMINSTRATOR in windows) , sometimes people need a new user to hold the things , but there's one small issue , most of linux base images comes with no user authentication packages , so you will not be able to create / remove / grant privellage to a user , the solution for this is to use the `USER` instruction rather than the `RUN` instruction , ex. `RUN groupadd hadoop && useradd -g hadoop hduser` , `USER hduser` ... first i created a user using the `RUN` , then i used the `USER` instruction to switch to that user. (su - hduser)

- `ENTRYPOINT` , this command excutes commands ... the difference between `ENTRYPOINT , CMD , RUN` that the RUN instruction excutes commands on the build time of the image (using the intermedient (temp) containers, adding new layers) , but the CMD , ENTRYPOINT this edits the metadata of the container. (The first command that container will up and work for) ... the `ENTRYPOINT` instruction is the original command that determines the entry command for the container ... the `CMD` instruction is the arguments of the `ENTRYPOINT` , so if you want to run a command (application command) you do first the entrypoint then the argument in the cmd

- `ARG` instruction google it.
- You should consider searching for an image to save the build time ... for instance if you need a hadoop container that requires JDK , instead of intalling and configuring it from scratch you should consider searching for the openjdk image on docker hub.

- `-P` option with building means all porst are forwarded to the host.

# image Registrey (pushing images to docker-hub (registrey))
- `docker login` = login to dockerhub(simple and easy) , don't forget to create an access token on docker hub.

- `docker tag` = tagging an image (it's like git .. in git we say git tag to tag a commit to be a version in this case we will tag the image to be an image on docker hub ) , we change it's tag as it should be changes to fit the format on docker hub which is [account]/[imagename]:[tag]

- `docker image push` = pushing an iamge to a docker hub repo , with each image it creates a new repo , when pushing an image on docker hub , if you have already pushed one and for some reason you edited it or made another tag , when pushing up the new tag it will compare the layers on dockerhub before uploading , and just uploads the new layer.

# Docker Compose
- when talking about application , we need to understand first that an application may consists of many parts , ex. a web application may have it's fornt-end , authentication , authorization , middle-ware , database .... etc, each one named a `service` , the authenticaion is a service , authorization is a service ...etc , each service consistis of many small parts each part called `microservice`... let me tell you a story ... in the past , when talking about applictaion , we have had one server has it's application on it , that one application was doing everything ... a single python file that contains the front-end , back-end , authentication , db-connections ...etc , this design called `monolithic application` , a single application that holds everything it's programmed for in one single unit, you may notice the problem here (it's very hard to extend , troubleshooting...etc), that's why the `microservices` design comes into play ,it separates an application into many services each service contains one / many `microservice (container)`

- service = container + network +storage.
- in the past there was a CORP called `orchad`(i guess) made a python software called `fig` ( which is a python module now) that applicationit made for `composing` an application's services , ex. this Dockerfile will handle this containers' network and attach that vollume to it....etc , later on docker.inc aquired that CORP , and now it have it under the name of `docker-compose`.

- docker-compose `is a python package that automate the process of building an application with it's services`.

- docker-compose script isn't part of docker run time it's a standalone script that cna be installed.

- docker-compose needs a file to tell him what to do , this file has fixed name and fixed extention which is `docker-compose.yml`

- a `yml` files is a subsequence of `json` files , it's `key-value` structured.

- in `docker-compose.yml` there's four main keys `versoin , services , network , volumes` (VSNV)

- `version` key is the only required key(in the past , now in docker-compose cli v2 it takes it's current version automatically) , that tells the file is compitable with which docker-compose version

- `networks` key is telling dokcer engine to create netrowk , ex
    `
        netowrk:
            counter-net:
    `
    this telling docker engine to create a network named counter-net = `docker network create counter-net`

- `volumes` key is telling docker engine to create volumes , ex
    `
        volumes:
            counter-vol:
    `
    which is equal to `docker volume create counter-vol`

- `services` this contains all services (that contains the microservices) that will run in my application.
- `services:\n  web-fe:\n   build: .` this tells docker engine to build from the current building directoory (searches for the Dockerfile)

- `see the docker-compose.yml file inside container-app/`
- `docker-compose up -f [file name].yml &` composing the docker-compose.yml file
- now let's see how things inside `docker-work/container-app` are happend inside docker engine
- if you cuirios it's just a flask(python) application with redis to store how many times a user visited the home page.
- if you navigate through `/var/lib/docker` which is where docker engine keeps it's configs and things on your host, `cd volumes` you will see that you have 2 volumes the one we created `container-app_counter-vol` and other one , `cd ../overlay2` you will be able to see that you have now a new network `container-app_counter-net`.

- please note that working with docker-compose will name the container/network/volumes starting with the application's name (the build context directory).

- please note that you can test your containers using the following command `docker exec [container's name / hash] ping -c1 google.com`.

- please note that the 2 containers (in our case) can see and talk to each other (ICMP ping) with the service names(redis , web-fe) , ex `docker exec d58a ping -c1 redis`

- we can do the same thing using docker-compose `docker-compose exec [service's name] ping -c1 [another service's name]`.

- we can see how many services running on our docker compose using `docker-compose ps`

- to remove everything from your host (instead of removing each image / each network) use this cmd `docker-compose down (within the build context)` , it will not remove volumes as it's the presitance storage i have , it will be meaningless to delete them when i shutdown the services , and it will keep the images as will , as in the next time you create your services it would be faster than pulling the images from scratch, however you can still remove everything using `docker-compose down --rmi local`

- I have edited something in the docker-compose.yml , which is this is a tiny full stack code , right? , does it seem right to allow the backend service (redis) exposed to the internet ?? , ofc not , that's why we have created tow networks (frontend-net and backend-net) , the web-fe service is connected on both frontend-net (exposed) and the backend-net (internal) , while the redis service is connected just on the backend-net

- that's all i know about docker-compose , it's not everything ... keep going on docks.

# Docker Swarm (services on different hosts)
- kubernates (will be discussed later)
- the swarm in docker makes you able to deal with many services that not stored on the same host , it turns your host to a `node` in a cluster of nodes , each node can be a `manager` or a `worker` ,manager nodes are the nodes that is taking control (excute commands , edit services...etc)

- the number of manager nodes is recommened to be in the range 1-7 , the number prefered to be odd not even

- a manager node can carry workload , so it works as a manager and a worker in the same time.
- each manager node has a database that stores all the configs , it's called `etcd database`
- `docker swarm init --advertise-addr [host ip]:2377 --listen-addr [host ip]:2377` this initializes the swarm on the host machine

- The --advertise-addr flag specifies the address that will be advertised to other members of the swarm for API access and overlay networking

- The --listen-addr flag specifies the address that will used to listen on the comming connections from the other nodes.

- `docker swarm join-token worker` shows the token that makes you able to add aworker to the cluster

- `docker swarm join-token manager` shows the token that makes you able to add manager to the cluster

- suppose we have 5 VMs , each of which we have installed docker on them , the swarm logic in docker works with different containers on different docker-hosts , so we will make 3 of them managers and the 2 remainig are workers , with doing this , we can use above commands to achieve this , now let's change the think of our mind from containers to services , so we will create a service to do so we will use the follwing command...

- `docker service create --name web -p 80:80 --replicas 5 nginx:latest`

- we have created 5 replicas of our service , so now our 5 nodes (vms) are having the same service (container(s)), when excuting the above command , a new netowrk is generated with a new driver which is (overlay) driver that have the capapility to make each nodes see each other and make our service alive on all nodes , another network is created as well.

- please not that if you tried to preform the following command on a worker machine `docker service ls` it will give you an error says that this node is a worker , this command must be excuted on a manager host

- `docker service rm [name of service]` removes a service

- the services are created it will start giving the replecas first on the worker nodes (so if we have 3 mangers and 2 workers and we created a service with 2 replicas the 2 workers nodes will have it)

- even if the service (container) doesn't exist on the current docker host the managers will be able to view it(if you running nginx a manager will be able to veiw it in it's browser) , and that is becaouse of the `ingress` network ( the network that makes the service alive on each node)

- you can change the number of replicas without deleting the service and creating it again with different number of replicas using the following command `docker service scale [name of service]=[number of new replicas]`
    # Visualize docker-swarm (for linux users)
    - `docker service create --name=viz -publish=8080:8080/tcp --constrain=node.role=manager --mount=type=bind,src=/var/run/docker.sock,dist=/var/run/docker.sock dockersamples/visualizer`

    - this command will download and excutes a service called viz it's available on docker hub under repo called `dockersamples/visualizer`

    - this will help you view and manage your nodes with docker-swarm
    - for windows / macosx you guys have alread docker-desktop that help you.

- if a service fall down on a worker node , the rest of worker nodes will carry up the service , the service's microserverices(containers) will be distributed over other worker nodes , `if the failed node recoverd and back to work (up and running) the tasks will not be redistrubted once again , to achieve so , a complix configus must be done :) , so the down machine / node will not carry any services again.`

- if you want to update the image that your service live on .. `docker service update --image nignx:latest --update-perallelism 2 --update-delay 5s [service name]`

- the default in update command that when updating to a new version , it will update each microservice individually (kills the first container , then make a new one...and so on) but with the flag `--update-perallelism [number]` you say please update n numbers of containers on each step.

- another flag which is `--update-delay [n]s` this will wait n seconds between each step

- the pervious containers (older version) will be exist and stoped , you can later on `merge` the services.

- you can roll back to the previous version using `docker service rollback`

    # Service Vs Container
    - the concept of service in general said to be `statefull`
    - statefull is meant to be the condition that this service is running depening on them
    - a container  is `stateless` , it doesn't matter what the condition that this container follows , it's just care about whiether if the container up or down

    - the message when you create a new service `service converged` means that the `desired state` met , a desired state is the original state that you created the service with , ex. if you created a serivce with 6 replicas , and a node fall down , si each node now carry 4 tasks(for instance) this is not the desired state.

    - if you tried to run this command it will fail `docker service create ubuntu --replicas 2 ubunut:latest`

    - why??
    - this is because that y're running a `container` not a service ... what's inside this container?? , nothing , it's just the bash script... so when the bash script `/bin/sh or /bin/bash` excutes and finishes this container will be `stateless` it's just doing nothing ,so with that the docker engine will keep trying over and over again to create this as a service and it will fail , to understand it deeply , we have agreed that the container runs everything on `PID 1` , so when you create an ubunut service (container) what will be excuted on that PID 1 ... the bash shell , so the PID 1 will excutes `/bin/bash` and terminates , so it will keep re-upping the container over and over again (for ever) as everytime the PID 1 process terminates , so it will stuck in a loop, so you will not evern rich the `desired state` of the service . ie. `the service will never converges`.

    - a service will keep that PID 1 up and running for ever (during the service life-time.)

    - it's not meaningless to create a service with an os' base image , but if you even want to do so , there's a way we can do this , ... by selecting a process to be excuted for ever (infinte-loop)

    - ex. `docker service create --name ubuntu --replicas 2 ubuntu:latest bash -c "while true; do echo hello ; sleep 2 ; done"`

    - docker swarm has some cons , one of them is it doesn't matter what's inside the container , it only cares about wheier that PID 1 is up and running or not.

    - so in general a service will be converged (running without problems) if the desired state achived (the desired state contains , networks , replicas , volumes, certicate ...etc)


    # Docker Stack
    - is a way that automates the deployment of the services , it works only on swarm
    - it's a yaml file just as the compose file , it has the same four main keys(version , services ,network , volumes) , it has another one called secretes

    - `docker-secret swarm object` a secret in docker is anything that you don't want it to be public (creticates , credintials , etc) , why?
        1- to prevent being just a clear text in the file (saba7 el security awarness :) )
        2- to make them shared amoung all nodes in docker-swarm
    - secrets objects exists in `/run/secrets` in linux

    - please look at the stack file in the directory `atsea-sample-shop-app/docker-stack.yml` , or visit the original repo [LINK](https://github.com/dockersamples/atsea-sample-shop-app)

    - one last thing about docker swarm ... it's very poor and have many drawbacks (google it)

    # Portainer
    - another Gui visualization to control and manage docker swarm services (kubernates and docker solution).
    - [LINK](https://www.portainer.io/) , google how to install and use it
    - you can download the docker-stack file and install it , it's deployed as containers
    - it's reliable to work with


# Kubernetes (K8s)
- Kubernetes is an open source container orchestration engine for automating deployment, scaling, and management of containerized applications. The open source project is hosted by the Cloud Native Computing Foundation.

- I will study it later , going to learn about databases.
- and i will glad to announce that we have finished this repo :)
