#!/bin/bash
NODE_NAME=${NODE_NAME:-node1}
CONFIG_SERVER_URL=${CONFIG_SERVER_URL:-http://localhost:8888}
curl -s $CONFIG_SERVER_URL/compose-$NODE_NAME.yaml -o docker-compose.yaml
curl -s $CONFIG_SERVER_URL/env-$NODE_NAME.yaml | awk -F: '{ st = index($0,":");print $1 "=" substr($0,st+2)}' > .env
