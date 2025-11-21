from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ClusterInfo:
    name: str
    host: str
    port: int

@dataclass
class SessionStats:
    infobase_name: str
    active_sessions: int
    blocked_sessions: int

@dataclass
class LockStats:
    infobase_name: str
    locks_count: int

class OneCClient(ABC):
    """Abstract base class for 1C Cluster Client."""

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the cluster."""
        pass

    @abstractmethod
    def get_cluster_info(self) -> ClusterInfo:
        """Get basic cluster information."""
        pass

    @abstractmethod
    def get_session_stats(self) -> List[SessionStats]:
        """Get session statistics per infobase."""
        pass

    @abstractmethod
    def get_lock_stats(self) -> List[LockStats]:
        """Get lock statistics per infobase."""
        pass

class MockOneCClient(OneCClient):
    """Mock implementation for testing and development."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._connected = False

    def connect(self) -> bool:
        self._connected = True
        return True

    def get_cluster_info(self) -> ClusterInfo:
        return ClusterInfo(name="test-cluster", host=self.host, port=self.port)

    def get_session_stats(self) -> List[SessionStats]:
        return [
            SessionStats(infobase_name="accounting", active_sessions=10, blocked_sessions=0),
            SessionStats(infobase_name="hrm", active_sessions=5, blocked_sessions=1)
        ]

    def get_lock_stats(self) -> List[LockStats]:
        return [
            LockStats(infobase_name="accounting", locks_count=2),
            LockStats(infobase_name="hrm", locks_count=0)
        ]
