from typing import List
from ai_assistant.bottleneck_detector import AnalysisResult

class RecommendationEngine:
    def get_recommendations(self, bottlenecks: List[AnalysisResult]) -> List[str]:
        recommendations = []
        
        for b in bottlenecks:
            if b.component == "1C":
                if "blocked sessions" in b.reason:
                    recommendations.append("Check 1C transaction locks. Look for long transactions in the code.")
            
            if b.component == "1C/DB":
                if "long running queries" in b.reason:
                    recommendations.append("Analyze slow query log. Check for missing indexes on frequently accessed tables.")

            if b.component == "Bitrix":
                if "HTTP 5xx" in b.reason:
                    recommendations.append("Check PHP-FPM logs and Nginx error logs. Verify PHP memory_limit.")

        if not recommendations and bottlenecks:
            recommendations.append("General performance tuning recommended.")
            
        return recommendations
