"""Main tool"""
import prometheus_client

from . import Collector


def main():
    """Register collector and serve it via HTTP"""

    prometheus_client.REGISTRY.register(Collector())
    print("serving on :9116")
    prometheus_client.start_http_server(9116)
    while True:
        pass


if __name__ == "__main__":
    main()
