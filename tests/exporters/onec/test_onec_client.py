import unittest
from onec_exporter.onec_client import MockOneCClient, ClusterInfo, SessionStats, LockStats

class TestOneCClient(unittest.TestCase):
    def setUp(self):
        self.client = MockOneCClient("localhost", 1540)

    def test_connection(self):
        self.assertTrue(self.client.connect())

    def test_cluster_info(self):
        info = self.client.get_cluster_info()
        self.assertIsInstance(info, ClusterInfo)
        self.assertEqual(info.host, "localhost")
        self.assertEqual(info.port, 1540)

    def test_session_stats(self):
        stats = self.client.get_session_stats()
        self.assertIsInstance(stats, list)
        self.assertTrue(len(stats) > 0)
        self.assertIsInstance(stats[0], SessionStats)

    def test_lock_stats(self):
        stats = self.client.get_lock_stats()
        self.assertIsInstance(stats, list)
        self.assertTrue(len(stats) > 0)
        self.assertIsInstance(stats[0], LockStats)

if __name__ == '__main__':
    unittest.main()
