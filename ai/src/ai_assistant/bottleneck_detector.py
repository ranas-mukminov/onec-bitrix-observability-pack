from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class AnalysisResult:
    is_bottleneck: bool
    component: str
    confidence: float
    reason: str

class BottleneckDetector:
    def analyze(self, metrics: Dict[str, float]) -> List[AnalysisResult]:
        results = []
        
        # 1C Checks
        if metrics.get("onec_sessions_blocked", 0) > 5:
            results.append(AnalysisResult(
                is_bottleneck=True,
                component="1C",
                confidence=0.9,
                reason="High number of blocked sessions detected (>5)"
            ))
            
        if metrics.get("onec_long_queries_total", 0) > 100:
            results.append(AnalysisResult(
                is_bottleneck=True,
                component="1C/DB",
                confidence=0.8,
                reason="Frequent long running queries detected"
            ))

        # Bitrix Checks
        if metrics.get("bitrix_http_5xx_total", 0) > 10:
            results.append(AnalysisResult(
                is_bottleneck=True,
                component="Bitrix",
                confidence=0.95,
                reason="High rate of HTTP 5xx errors"
            ))

        return results
