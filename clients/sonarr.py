import httpx
from typing import List, Dict, Any, Optional

class SonarrClient:
    def __init__(self, url: str, api_key: str, verify_ssl: bool = False):
        self.base_url = f"{url.rstrip('/')}/api/v3"
        self.headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, verify=verify_ssl)

    def get_health(self) -> Dict[str, Any]:
        status_r = self.client.get("/system/status")
        status_r.raise_for_status()
        
        health_r = self.client.get("/health")
        health_r.raise_for_status()
        
        return {
            "status": status_r.json(),
            "health": health_r.json()
        }

    def list_series(self) -> List[Dict[str, Any]]:
        response = self.client.get("/series")
        response.raise_for_status()
        return response.json()

    def search_series(self, term: str) -> List[Dict[str, Any]]:
        response = self.client.get("/series/lookup", params={"term": term})
        response.raise_for_status()
        return response.json()

    def get_configs(self) -> Dict[str, Any]:
        configs = {}
        
        # Root folders
        r = self.client.get("/rootfolder")
        r.raise_for_status()
        configs["rootFolders"] = r.json()
        
        # Quality profiles
        r = self.client.get("/qualityprofile")
        r.raise_for_status()
        configs["qualityProfiles"] = r.json()
        
        # Language profiles
        r = self.client.get("/languageprofile")
        r.raise_for_status()
        configs["languageProfiles"] = r.json()

        return configs

    def add_series(self, series_data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.post("/series", json=series_data)
        response.raise_for_status()
        return response.json()

    def delete_series(self, series_id: int, delete_files: bool = False) -> Dict[str, Any]:
        params = {"deleteFiles": delete_files}
        response = self.client.delete(f"/series/{series_id}", params=params)
        response.raise_for_status()
        return {"status": "deleted", "id": series_id}

    def get_queue(self) -> Dict[str, Any]:
        response = self.client.get("/queue")
        response.raise_for_status()
        return response.json()

    def get_history(self, limit: int = 20) -> Dict[str, Any]:
        params = {"pageSize": limit}
        response = self.client.get("/history", params=params)
        response.raise_for_status()
        return response.json()

    def post_command(self, name: str, **kwargs) -> Dict[str, Any]:
        payload = {"name": name, **kwargs}
        response = self.client.post("/command", json=payload)
        response.raise_for_status()
        return response.json()

    def get_episodes(self, series_id: int) -> List[Dict[str, Any]]:
        params = {"seriesId": series_id}
        response = self.client.get("/episode", params=params)
        response.raise_for_status()
        return response.json()

    def get_blocklist(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        params = {"page": page, "pageSize": page_size}
        response = self.client.get("/blocklist", params=params)
        response.raise_for_status()
        return response.json()

    def delete_blocklist_item(self, blocklist_id: int) -> Dict[str, Any]:
        response = self.client.delete(f"/blocklist/{blocklist_id}")
        response.raise_for_status()
        return {"status": "deleted", "id": blocklist_id}

    def list_import_list_exclusions(self) -> List[Dict[str, Any]]:
        response = self.client.get("/importlistexclusion")
        response.raise_for_status()
        return response.json()

    def add_import_list_exclusion(self, tvdb_id: int, title: str) -> Dict[str, Any]:
        payload = {"tvdbId": tvdb_id, "title": title}
        response = self.client.post("/importlistexclusion", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_import_list_exclusion(self, exclusion_id: int) -> Dict[str, Any]:
        response = self.client.delete(f"/importlistexclusion/{exclusion_id}")
        response.raise_for_status()
        return {"status": "deleted", "id": exclusion_id}
