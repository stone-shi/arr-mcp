import pytest
from clients.lidarr import LidarrClient
from clients.radarr import RadarrClient
from clients.sonarr import SonarrClient


@pytest.fixture
def lidarr_client():
    return LidarrClient("http://localhost:8686", "test-api-key", verify_ssl=False)


@pytest.fixture
def radarr_client():
    return RadarrClient("http://localhost:7878", "test-api-key", verify_ssl=False)


@pytest.fixture
def sonarr_client():
    return SonarrClient("http://localhost:8989", "test-api-key", verify_ssl=False)
