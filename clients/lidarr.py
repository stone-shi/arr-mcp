import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

# Models
class Artist(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    artistName: Optional[str] = None
    status: Optional[str] = None
    monitored: Optional[bool] = None
    path: Optional[str] = None
    mbid: Optional[str] = None

class Album(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    title: Optional[str] = None
    artistId: Optional[int] = None
    monitored: Optional[bool] = None
    status: Optional[str] = None

class SystemStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")
    version: Optional[str] = None
    osName: Optional[str] = None
    isMono: Optional[bool] = None
    isLinux: Optional[bool] = None

class QueueStatusMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    title: str
    messages: List[str]

class QueueItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    title: str
    status: str
    size: float
    sizeleft: float
    timeleft: Optional[str] = None
    trackedDownloadStatus: Optional[str] = None
    trackedDownloadState: Optional[str] = None
    statusMessages: List[QueueStatusMessage] = []

class HistoryItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    sourceTitle: str
    eventType: str
    date: str


class LidarrClient:
    def __init__(self, url: str, api_key: str, verify_ssl: bool = False):
        self.base_url = f"{url.rstrip('/')}/api/v1"
        self.headers = {"X-Api-Key": api_key}
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, verify=verify_ssl)

    def get_system_status(self) -> Dict[str, Any]:
        response = self.client.get("/system/status")
        response.raise_for_status()
        return response.json()

    def get_artists(self) -> List[Dict[str, Any]]:
        response = self.client.get("/artist")
        response.raise_for_status()
        return response.json()

    def search_artists(self, term: str) -> List[Dict[str, Any]]:
        response = self.client.get("/artist/lookup", params={"term": term})
        response.raise_for_status()
        return response.json()

    def get_albums(self, artist_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {}
        if artist_id:
            params["artistId"] = artist_id
        response = self.client.get("/album", params=params)
        response.raise_for_status()
        return response.json()

    def post_command(self, name: str, **kwargs) -> Dict[str, Any]:
        payload = {"name": name, **kwargs}
        response = self.client.post("/command", json=payload)
        response.raise_for_status()
        return response.json()

    def get_queue(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        params = {"page": page, "pageSize": page_size, "sortKey": "timeleft", "sortDirection": "ascending"}
        response = self.client.get("/queue", params=params)
        response.raise_for_status()
        return response.json()

    def get_history(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        params = {"page": page, "pageSize": page_size, "sortKey": "date", "sortDirection": "descending"}
        response = self.client.get("/history", params=params)
        response.raise_for_status()
        return response.json()
