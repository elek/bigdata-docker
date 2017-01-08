

 * For ubuntu I can recommend this docker installation role: https://github.com/angstwad/docker.ubuntu
 * docker_container ansible module requires at least 2.1 version from ansible     
 * Please note that the volume path most probably should be adjust the volume path mapping
 * And you need a gateway group in the inventory and a variable gatway which should point to the gateway node (as you can see in the ansible example)
 * I recommend to use https://github.com/weaveworks/scope to visualize the cluster state
