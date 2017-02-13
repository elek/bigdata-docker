# Consul configuration for HADOOP clusters

Quick start:

  1. Install docker to all hosts. For Ubuntu I use  https://github.com/angstwad/docker.ubuntu
  2. Install consul to the hosts (see the consul.yaml from https://github.com/elek/bigdata-docker/tree/master/infra-playbooks )
  3. Install ```consync``` from https://github.com/elek/consync (most probably with clone and ```pip install .```)
  4. Upload the configuration to the consul: ```consync /yourworkingdir/bigdata-docker/consul conf --url http://consulhost:8500/v1/kv``` (You need to set GATEWAY_HOST and DATA_DIR environment variables. The first is to No1 node with the master components, the second is a data directory which will be a docker volume for the persistent data)
  5. Start the agents with agent.yaml from https://github.com/elek/bigdata-docker/tree/master/infra-playbooks (The docker-compose files will be downloaded from consul and the containers will be started)
  6. It's possible that some components needs additional initialization (eg. namenode format). Do It Yourself.
