# Genshin Impact Project

# To do

1.) See if I need to add ssh key to GCP in VM instances (under Metadata) --NOT NECESSARY IF I'M GOING TO RUN STUFF ON MY PERSONAL PC

# Docker

This is how I set it up for WSL. First, I followed the instructions here: https://docs.docker.com/engine/install/ubuntu/.

Then I got the error: 
```shell
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
```

To fix this, I ran
```shell
sudo apt-get install -y iptables arptables ebtables
sudo dockerd --iptables=false
```
Otherwise, I would need to fix things related to using WSL