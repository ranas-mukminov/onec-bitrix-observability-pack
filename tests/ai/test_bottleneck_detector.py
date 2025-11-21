import unittest
from ai_assistant.bottleneck_detector import BottleneckDetector

class TestBottleneckDetector(unittest.TestCase):
    def setUp(self):
        self.detector = BottleneckDetector()

    def test_no_bottlenecks(self):
        metrics = {"onec_sessions_blocked": 0, "bitrix_http_5xx_total": 0}
        results = self.detector.analyze(metrics)
        self.assertEqual(len(results), 0)

    def test_onec_blocking(self):
        metrics = {"onec_sessions_blocked": 10}
        results = self.detector.analyze(metrics)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].component, "1C")

    def test_bitrix_errors(self):
        metrics = {"bitrix_http_5xx_total": 50}
        results = self.detector.analyze(metrics)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].component, "Bitrix")

if __name__ == '__main__':
    unittest.main()
