import os
import logging
import sys
from prometheus_client import start_http_server

from onec_exporter.onec_client import MockOneCClient
from onec_exporter.collector import OneCCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Configuration from environment variables
    listen_port = int(os.getenv("PROMETHEUS_LISTEN_PORT", "8000"))
    cluster_host = os.getenv("ONEC_CLUSTER_HOST", "localhost")
    cluster_port = int(os.getenv("ONEC_CLUSTER_PORT", "1540"))
    interval = int(os.getenv("COLLECTION_INTERVAL", "15"))

    logger.info(f"Starting onec_exporter on port {listen_port}")
    
    # Initialize Client
    # In a real scenario, we would choose between Real and Mock client based on config or availability
    # For this pack, we default to Mock if no real credentials/libs are found, 
    # but the structure allows swapping in a real COM/RAS client.
    client = MockOneCClient(host=cluster_host, port=cluster_port)

    # Initialize Collector
    collector = OneCCollector(client=client, interval=interval)

    # Start Prometheus HTTP Server
    start_http_server(listen_port)

    # Start Collection Loop
    try:
        collector.run()
    except KeyboardInterrupt:
        logger.info("Stopping exporter...")
        sys.exit(0)

if __name__ == "__main__":
    main()
