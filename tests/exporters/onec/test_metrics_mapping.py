import unittest
from unittest.mock import MagicMock
from prometheus_client import REGISTRY
from onec_exporter.metrics import SESSIONS_ACTIVE, SESSIONS_BLOCKED, LOCKS_COUNT
from onec_exporter.onec_client import SessionStats, LockStats

class TestMetricsMapping(unittest.TestCase):
    def setUp(self):
        # Reset metrics before each test to avoid registry errors or stale data
        # Note: In real prometheus_client, unregistering is tricky, so we might just set values
        pass

    def test_metrics_exist(self):
        self.assertIsNotNone(SESSIONS_ACTIVE)
        self.assertIsNotNone(SESSIONS_BLOCKED)
        self.assertIsNotNone(LOCKS_COUNT)

    def test_update_metrics(self):
        # Simulate data
        session_data = SessionStats(infobase_name="test_db", active_sessions=42, blocked_sessions=2)
        
        # Update metrics
        SESSIONS_ACTIVE.labels(infobase=session_data.infobase_name, cluster="default").set(session_data.active_sessions)
        SESSIONS_BLOCKED.labels(infobase=session_data.infobase_name, cluster="default").set(session_data.blocked_sessions)

        # Verify (using internal prometheus_client API for testing)
        self.assertEqual(
            SESSIONS_ACTIVE.labels(infobase="test_db", cluster="default")._value.get(),
            42
        )
        self.assertEqual(
            SESSIONS_BLOCKED.labels(infobase="test_db", cluster="default")._value.get(),
            2
        )

if __name__ == '__main__':
    unittest.main()
