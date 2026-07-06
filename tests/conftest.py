import os

# Set dummy env vars before any test imports config/main modules,
# which instantiate Settings() at module load time.
os.environ.setdefault("LIDARR_URL", "http://localhost:8686")
os.environ.setdefault("LIDARR_API_KEY", "test-key")
os.environ.setdefault("RADARR_URL", "http://localhost:7878")
os.environ.setdefault("RADARR_API_KEY", "test-key")
os.environ.setdefault("SONARR_URL", "http://localhost:8989")
os.environ.setdefault("SONARR_API_KEY", "test-key")

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
