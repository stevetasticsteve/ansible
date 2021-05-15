#!/bin/bash
# This script starts the Nextcloud docker containers, creating volumes if required

docker-compose --env-file /etc/docker/nextcloud/nextcloud.env -f /etc/docker/nextcloud/nextcloud_docker-compose.yml up -d