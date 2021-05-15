#!/bin/bash
# This script stops the nextcloud docker images, retaining the volumes

docker-compose --env-file /etc/docker/nextcloud/nextcloud.env -f /etc/docker/nextcloud/nextcloud_docker-compose.yml down