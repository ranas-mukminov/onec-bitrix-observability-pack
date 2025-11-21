import logging
import time
from typing import Optional

from prometheus_client import start_http_server

from onec_exporter.metrics import (
    SESSIONS_ACTIVE,
    SESSIONS_BLOCKED,
    LOCKS_COUNT,
    CLUSTER_UP
)
from onec_exporter.onec_client import OneCClient

logger = logging.getLogger(__name__)

class OneCCollector:
    def __init__(self, client: OneCClient, interval: int = 15):
        self.client = client
        self.interval = interval
        self._running = False

    def collect(self):
        """Fetch metrics from 1C and update Prometheus gauges."""
        try:
            # Check connection/cluster status
            if not self.client.connect():
                logger.error("Failed to connect to 1C cluster")
                CLUSTER_UP.labels(cluster="default").set(0)
                return

            info = self.client.get_cluster_info()
            CLUSTER_UP.labels(cluster=info.name).set(1)

            # Collect sessions
            sessions = self.client.get_session_stats()
            for s in sessions:
                SESSIONS_ACTIVE.labels(infobase=s.infobase_name, cluster=info.name).set(s.active_sessions)
                SESSIONS_BLOCKED.labels(infobase=s.infobase_name, cluster=info.name).set(s.blocked_sessions)

            # Collect locks
            locks = self.client.get_lock_stats()
            for l in locks:
                LOCKS_COUNT.labels(infobase=l.infobase_name, cluster=info.name).set(l.locks_count)

        except Exception as e:
            logger.exception("Error collecting metrics: %s", e)
            CLUSTER_UP.labels(cluster="unknown").set(0)

    def run(self):
        """Start the collection loop."""
        self._running = True
        logger.info("Starting 1C Collector with interval %ss", self.interval)
        while self._running:
            self.collect()
            time.sleep(self.interval)
