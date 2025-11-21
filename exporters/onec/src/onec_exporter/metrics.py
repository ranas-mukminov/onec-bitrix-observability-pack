from prometheus_client import Gauge, Histogram, Counter

# Namespace for all metrics
NAMESPACE = "onec"

# Session metrics
SESSIONS_ACTIVE = Gauge(
    f"{NAMESPACE}_sessions_active",
    "Number of active sessions",
    ["infobase", "cluster"]
)

SESSIONS_BLOCKED = Gauge(
    f"{NAMESPACE}_sessions_blocked",
    "Number of blocked sessions",
    ["infobase", "cluster"]
)

# Lock metrics
LOCKS_COUNT = Gauge(
    f"{NAMESPACE}_locks_count",
    "Current number of locks",
    ["infobase", "cluster"]
)

# Performance metrics
LONG_QUERIES_TOTAL = Counter(
    f"{NAMESPACE}_long_queries_total",
    "Total number of long queries detected",
    ["infobase"]
)

QUERY_DURATION_SECONDS = Histogram(
    f"{NAMESPACE}_query_duration_seconds",
    "Duration of queries in seconds",
    ["infobase", "operation_type"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
)

# Cluster status
CLUSTER_UP = Gauge(
    f"{NAMESPACE}_cluster_up",
    "1C Cluster availability status (1=up, 0=down)",
    ["cluster"]
)
