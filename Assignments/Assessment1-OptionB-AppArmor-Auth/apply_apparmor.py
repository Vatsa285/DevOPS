import os
import subprocess

import docker

PROFILE_NAME = "assessment-b-python"
PROFILE_PATH = os.path.join(os.path.dirname(__file__), PROFILE_NAME)
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "assessment-b-web")


def load_profile():
    subprocess.run(["sudo", "apparmor_parser", "-r", PROFILE_PATH], check=True)
    print(f"Loaded AppArmor profile: {PROFILE_NAME}")


def verify_profile():
    container = docker.from_env().containers.get(CONTAINER_NAME)
    container.reload()
    options = container.attrs.get("HostConfig", {}).get("SecurityOpt", [])
    expected = f"apparmor={PROFILE_NAME}"
    if expected not in options:
        raise RuntimeError(f"Expected {expected!r} in SecurityOpt, got {options!r}")
    print(f"Verified AppArmor profile on {CONTAINER_NAME}: {expected}")


if __name__ == "__main__":
    load_profile()
    verify_profile()
