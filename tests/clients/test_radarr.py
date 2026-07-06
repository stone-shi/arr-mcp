import pytest
import respx
from httpx import Response
from clients.radarr import RadarrClient


class TestRadarrClientInit:
    def test_base_url_strips_trailing_slash(self):
        client = RadarrClient("http://localhost:7878/", "test-key")
        assert client.base_url == "http://localhost:7878/api/v3"

    def test_base_url_without_trailing_slash(self):
        client = RadarrClient("http://localhost:7878", "test-key")
        assert client.base_url == "http://localhost:7878/api/v3"

    def test_headers_contain_api_key(self):
        client = RadarrClient("http://localhost:7878", "test-key")
        assert client.headers["X-Api-Key"] == "test-key"


class TestRadarrClientMethods:
    @respx.mock
    def test_get_system_status(self, radarr_client):
        mock_response = {"version": "3.0.0", "osName": "linux"}
        respx.get("http://localhost:7878/api/v3/system/status").mock(return_value=Response(200, json=mock_response))

        result = radarr_client.get_system_status()
        assert result == mock_response

    @respx.mock
    def test_list_movies(self, radarr_client):
        mock_movies = [{"id": 1, "title": "Movie 1"}, {"id": 2, "title": "Movie 2"}]
        respx.get("http://localhost:7878/api/v3/movie").mock(return_value=Response(200, json=mock_movies))

        result = radarr_client.list_movies()
        assert result == mock_movies

    @respx.mock
    def test_get_movie(self, radarr_client):
        mock_movie = {"id": 123, "title": "Inception"}
        respx.get("http://localhost:7878/api/v3/movie/123").mock(return_value=Response(200, json=mock_movie))

        result = radarr_client.get_movie(123)
        assert result == mock_movie

    @respx.mock
    def test_search_movie(self, radarr_client):
        mock_results = [{"id": 1, "title": "Inception"}]
        respx.get("http://localhost:7878/api/v3/movie/lookup", params={"term": "Inception"}).mock(
            return_value=Response(200, json=mock_results)
        )

        result = radarr_client.search_movie("Inception")
        assert result == mock_results

    @respx.mock
    def test_list_root_folders(self, radarr_client):
        mock_folders = [{"path": "/movies", "freeSpace": 1000000}]
        respx.get("http://localhost:7878/api/v3/rootfolder").mock(return_value=Response(200, json=mock_folders))

        result = radarr_client.list_root_folders()
        assert result == mock_folders

    @respx.mock
    def test_list_quality_profiles(self, radarr_client):
        mock_profiles = [{"id": 1, "name": "HD-1080p"}]
        respx.get("http://localhost:7878/api/v3/qualityprofile").mock(return_value=Response(200, json=mock_profiles))

        result = radarr_client.list_quality_profiles()
        assert result == mock_profiles

    @respx.mock
    def test_add_movie_with_defaults(self, radarr_client):
        mock_lookup = {"tmdbId": 123, "title": "Inception"}
        mock_folders = [{"path": "/movies"}]
        mock_profiles = [{"id": 1, "name": "HD-1080p"}]
        mock_added = {"id": 1, "title": "Inception"}

        respx.get("http://localhost:7878/api/v3/movie/lookup/tmdb", params={"tmdbId": 123}).mock(
            return_value=Response(200, json=mock_lookup)
        )
        respx.get("http://localhost:7878/api/v3/rootfolder").mock(return_value=Response(200, json=mock_folders))
        respx.get("http://localhost:7878/api/v3/qualityprofile").mock(return_value=Response(200, json=mock_profiles))
        respx.post("http://localhost:7878/api/v3/movie").mock(return_value=Response(200, json=mock_added))

        result = radarr_client.add_movie(123)
        assert result == mock_added

    @respx.mock
    def test_add_movie_with_explicit_params(self, radarr_client):
        mock_lookup = {"tmdbId": 123, "title": "Inception"}
        mock_added = {"id": 1, "title": "Inception"}

        respx.get("http://localhost:7878/api/v3/movie/lookup/tmdb", params={"tmdbId": 123}).mock(
            return_value=Response(200, json=mock_lookup)
        )
        respx.post("http://localhost:7878/api/v3/movie").mock(return_value=Response(200, json=mock_added))

        result = radarr_client.add_movie(123, root_folder="/custom", quality_profile_id=5)
        assert result == mock_added

    @respx.mock
    def test_add_movie_no_root_folders(self, radarr_client):
        mock_lookup = {"tmdbId": 123, "title": "Inception"}
        respx.get("http://localhost:7878/api/v3/movie/lookup/tmdb", params={"tmdbId": 123}).mock(
            return_value=Response(200, json=mock_lookup)
        )
        respx.get("http://localhost:7878/api/v3/rootfolder").mock(return_value=Response(200, json=[]))

        with pytest.raises(ValueError, match="No root folders configured"):
            radarr_client.add_movie(123)

    @respx.mock
    def test_update_movie(self, radarr_client):
        mock_movie = {"id": 123, "title": "Inception", "monitored": False, "qualityProfileId": 1}
        mock_updated = {"id": 123, "title": "Inception", "monitored": True, "qualityProfileId": 2}

        respx.get("http://localhost:7878/api/v3/movie/123").mock(return_value=Response(200, json=mock_movie))
        respx.put("http://localhost:7878/api/v3/movie/123").mock(return_value=Response(200, json=mock_updated))

        result = radarr_client.update_movie(123, monitored=True, quality_profile_id=2)
        assert result == mock_updated

    @respx.mock
    def test_delete_movie(self, radarr_client):
        respx.delete("http://localhost:7878/api/v3/movie/123", params={"deleteFiles": True, "addImportExclusion": False}).mock(
            return_value=Response(200)
        )

        result = radarr_client.delete_movie(123, delete_files=True)
        assert result == {"status": "success", "id": 123}

    @respx.mock
    def test_get_queue(self, radarr_client):
        mock_queue = {"records": [], "page": 1, "pageSize": 20}
        respx.get("http://localhost:7878/api/v3/queue", params={
            "page": 1,
            "pageSize": 20,
            "includeUnknownMovieItems": True
        }).mock(return_value=Response(200, json=mock_queue))

        result = radarr_client.get_queue()
        assert result == mock_queue

    @respx.mock
    def test_get_history(self, radarr_client):
        mock_history = {"records": [], "page": 1, "pageSize": 20}
        respx.get("http://localhost:7878/api/v3/history", params={
            "page": 1,
            "pageSize": 20,
            "sortKey": "date",
            "sortDirection": "descending"
        }).mock(return_value=Response(200, json=mock_history))

        result = radarr_client.get_history()
        assert result == mock_history

    @respx.mock
    def test_post_command(self, radarr_client):
        mock_response = {"id": 1, "name": "RefreshMovie"}
        respx.post("http://localhost:7878/api/v3/command").mock(return_value=Response(200, json=mock_response))

        result = radarr_client.post_command("RefreshMovie")
        assert result == mock_response

    @respx.mock
    def test_list_indexers(self, radarr_client):
        mock_indexers = [{"id": 1, "name": "Indexer 1"}]
        respx.get("http://localhost:7878/api/v3/indexer").mock(return_value=Response(200, json=mock_indexers))

        result = radarr_client.list_indexers()
        assert result == mock_indexers

    @respx.mock
    def test_test_indexer(self, radarr_client):
        mock_indexer = {"id": 1, "name": "Test Indexer"}
        respx.get("http://localhost:7878/api/v3/indexer/1").mock(return_value=Response(200, json=mock_indexer))
        respx.post("http://localhost:7878/api/v3/indexer/test").mock(return_value=Response(200))

        result = radarr_client.test_indexer(1)
        assert result == {"status": "success", "indexer": "Test Indexer"}
