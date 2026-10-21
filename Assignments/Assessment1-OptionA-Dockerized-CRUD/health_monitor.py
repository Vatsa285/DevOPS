import logging
import os
import time

import docker
from docker.errors import NotFound

CONTAINER_NAME = os.getenv("CONTAINER_NAME", "assessment-a-web")
INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def check_and_restart(client):
    try:
        container = client.containers.get(CONTAINER_NAME)
    except NotFound:
        logging.error("Container %s does not exist", CONTAINER_NAME)
        return
    container.reload()
    health = container.attrs.get("State", {}).get("Health", {}).get("Status", "unknown")
    if container.status != "running" or health == "unhealthy":
        logging.warning("Restarting %s: status=%s health=%s", CONTAINER_NAME, container.status, health)
        container.restart()
    else:
        logging.info("%s healthy: status=%s health=%s", CONTAINER_NAME, container.status, health)


if __name__ == "__main__":
    client = docker.from_env()
    while True:
        check_and_restart(client)
        time.sleep(INTERVAL)
