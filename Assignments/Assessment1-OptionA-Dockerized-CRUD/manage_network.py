import os

import docker
from docker.errors import APIError, NotFound

NETWORK_NAME = os.getenv("NETWORK_NAME", "assessment-a-net")
MONGO_CONTAINER = os.getenv("MONGO_CONTAINER", "assessment-a-mongo")
WEB_CONTAINER = os.getenv("WEB_CONTAINER", "assessment-a-web")


def ensure_network(client):
    networks = client.networks.list(names=[NETWORK_NAME])
    if networks:
        return networks[0]
    return client.networks.create(NETWORK_NAME, driver="bridge")


def connect_if_needed(network, container):
    if not any(item.get("Name") == container.name for item in network.attrs.get("Containers", {}).values()):
        network.connect(container)


def main():
    client = docker.from_env()
    network = ensure_network(client)
    print(f"Network: {network.name} ({network.id[:12]})")
    for name in (MONGO_CONTAINER, WEB_CONTAINER):
        try:
            container = client.containers.get(name)
        except NotFound:
            print(f"Container not found: {name}")
            continue
        connect_if_needed(network, container)
        print(f"{name}: status={container.status}")
    print("Connected containers:", [item.get("Name") for item in network.reload().attrs.get("Containers", {}).values()])


if __name__ == "__main__":
    try:
        main()
    except APIError as error:
        raise SystemExit(f"Docker API error: {error}")
