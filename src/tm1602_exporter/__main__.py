"""Main tool"""
from time import sleep

import prometheus_client

from . import Collector


def main():
    """Register collector and serve it via HTTP"""

    prometheus_client.REGISTRY.register(Collector())
    print("serving on :9116", flush=True)
    prometheus_client.start_http_server(9116)
    while True:
        sleep(5)


if __name__ == "__main__":
    main()
