import httpx
from typing import List, Dict, Any, Optional

class RadarrClient:
    def __init__(self, url: str, api_key: str, verify_ssl: bool = False):
        self.base_url = f"{url.rstrip('/')}/api/v3"
        self.headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, verify=verify_ssl)

    def get_system_status(self) -> Dict[str, Any]:
        response = self.client.get("/system/status")
        response.raise_for_status()
        return response.json()

    def list_movies(self) -> List[Dict[str, Any]]:
        response = self.client.get("/movie")
        response.raise_for_status()
        return response.json()

    def get_movie(self, movie_id: int) -> Dict[str, Any]:
        response = self.client.get(f"/movie/{movie_id}")
        response.raise_for_status()
        return response.json()

    def search_movie(self, term: str) -> List[Dict[str, Any]]:
        response = self.client.get("/movie/lookup", params={"term": term})
        response.raise_for_status()
        return response.json()

    def list_root_folders(self) -> List[Dict[str, Any]]:
        response = self.client.get("/rootfolder")
        response.raise_for_status()
        return response.json()

    def list_quality_profiles(self) -> List[Dict[str, Any]]:
        response = self.client.get("/qualityprofile")
        response.raise_for_status()
        return response.json()

    def add_movie(self, tmdb_id: int, root_folder: Optional[str] = None, quality_profile_id: Optional[int] = None, monitored: bool = True, search_for_movie: bool = False) -> Dict[str, Any]:
        # Lookup movie by TMDB ID
        lookup_response = self.client.get("/movie/lookup/tmdb", params={"tmdbId": tmdb_id})
        lookup_response.raise_for_status()
        movie_data = lookup_response.json()

        # Determine root folder path if not provided
        if not root_folder:
            folders = self.list_root_folders()
            if not folders:
                raise ValueError("No root folders configured in Radarr.")
            root_folder = folders[0]['path']
        movie_data['rootFolderPath'] = root_folder

        # Determine quality profile ID if not provided
        if not quality_profile_id:
            profiles = self.list_quality_profiles()
            if not profiles:
                raise ValueError("No quality profiles configured in Radarr.")
            quality_profile_id = profiles[0]['id']
        movie_data['qualityProfileId'] = quality_profile_id

        movie_data['monitored'] = monitored
        movie_data['addOptions'] = {"searchForMovie": search_for_movie}

        response = self.client.post("/movie", json=movie_data)
        response.raise_for_status()
        return response.json()

    def update_movie(self, movie_id: int, monitored: Optional[bool] = None, quality_profile_id: Optional[int] = None) -> Dict[str, Any]:
        # Fetch existing details
        movie_data = self.get_movie(movie_id)
        
        if monitored is not None:
            movie_data['monitored'] = monitored
        if quality_profile_id is not None:
            movie_data['qualityProfileId'] = quality_profile_id

        response = self.client.put(f"/movie/{movie_id}", json=movie_data)
        response.raise_for_status()
        return response.json()

    def delete_movie(self, movie_id: int, delete_files: bool = False, add_import_exclusion: bool = False) -> Dict[str, Any]:
        params = {
            "deleteFiles": delete_files,
            "addImportExclusion": add_import_exclusion
        }
        response = self.client.delete(f"/movie/{movie_id}", params=params)
        response.raise_for_status()
        # Radarr delete returns 200 OK without body, or sometimes 200 with structure.
        return {"status": "success", "id": movie_id}

    def get_queue(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        params = {
            "page": page,
            "pageSize": page_size,
            "includeUnknownMovieItems": True
        }
        response = self.client.get("/queue", params=params)
        response.raise_for_status()
        return response.json()

    def get_history(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": "date",
            "sortDirection": "descending"
        }
        response = self.client.get("/history", params=params)
        response.raise_for_status()
        return response.json()

    def post_command(self, name: str, **kwargs) -> Dict[str, Any]:
        payload = {"name": name, **kwargs}
        response = self.client.post("/command", json=payload)
        response.raise_for_status()
        return response.json()

    def list_indexers(self) -> List[Dict[str, Any]]:
        response = self.client.get("/indexer")
        response.raise_for_status()
        return response.json()

    def test_indexer(self, indexer_id: int) -> Dict[str, Any]:
        # Fetch indexer first
        response = self.client.get(f"/indexer/{indexer_id}")
        response.raise_for_status()
        indexer_data = response.json()

        # Test indexer
        test_response = self.client.post("/indexer/test", json=indexer_data)
        test_response.raise_for_status()
        return {"status": "success", "indexer": indexer_data.get('name')}
