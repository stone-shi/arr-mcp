import pytest
import respx
from httpx import Response
from clients.lidarr import LidarrClient


class TestLidarrClientInit:
    def test_base_url_strips_trailing_slash(self):
        client = LidarrClient("http://localhost:8686/", "test-key")
        assert client.base_url == "http://localhost:8686/api/v1"

    def test_base_url_without_trailing_slash(self):
        client = LidarrClient("http://localhost:8686", "test-key")
        assert client.base_url == "http://localhost:8686/api/v1"

    def test_headers_contain_api_key(self):
        client = LidarrClient("http://localhost:8686", "test-key")
        assert client.headers["X-Api-Key"] == "test-key"


class TestLidarrClientMethods:
    @respx.mock
    def test_get_system_status(self, lidarr_client):
        mock_response = {"version": "1.0.0", "osName": "linux", "isMono": True, "isLinux": True}
        respx.get("http://localhost:8686/api/v1/system/status").mock(return_value=Response(200, json=mock_response))

        result = lidarr_client.get_system_status()
        assert result == mock_response

    @respx.mock
    def test_get_artists(self, lidarr_client):
        mock_artists = [{"id": 1, "artistName": "Artist 1"}, {"id": 2, "artistName": "Artist 2"}]
        respx.get("http://localhost:8686/api/v1/artist").mock(return_value=Response(200, json=mock_artists))

        result = lidarr_client.get_artists()
        assert result == mock_artists
        assert len(result) == 2

    @respx.mock
    def test_search_artists(self, lidarr_client):
        mock_results = [{"id": 1, "artistName": "Adele"}]
        respx.get("http://localhost:8686/api/v1/artist/lookup", params={"term": "Adele"}).mock(
            return_value=Response(200, json=mock_results)
        )

        result = lidarr_client.search_artists("Adele")
        assert result == mock_results

    @respx.mock
    def test_get_albums_without_artist_id(self, lidarr_client):
        mock_albums = [{"id": 1, "title": "Album 1"}]
        respx.get("http://localhost:8686/api/v1/album").mock(return_value=Response(200, json=mock_albums))

        result = lidarr_client.get_albums()
        assert result == mock_albums

    @respx.mock
    def test_get_albums_with_artist_id(self, lidarr_client):
        mock_albums = [{"id": 1, "title": "Album 1", "artistId": 123}]
        respx.get("http://localhost:8686/api/v1/album", params={"artistId": 123}).mock(
            return_value=Response(200, json=mock_albums)
        )

        result = lidarr_client.get_albums(artist_id=123)
        assert result == mock_albums

    @respx.mock
    def test_post_command(self, lidarr_client):
        mock_response = {"id": 1, "name": "RefreshArtist"}
        respx.post("http://localhost:8686/api/v1/command").mock(return_value=Response(200, json=mock_response))

        result = lidarr_client.post_command("RefreshArtist")
        assert result == mock_response

    @respx.mock
    def test_post_command_with_params(self, lidarr_client):
        mock_response = {"id": 1, "name": "RefreshArtist"}
        respx.post("http://localhost:8686/api/v1/command").mock(return_value=Response(200, json=mock_response))

        result = lidarr_client.post_command("RefreshArtist", artistId=123)
        assert result == mock_response

    @respx.mock
    def test_get_queue(self, lidarr_client):
        mock_queue = {"records": [], "page": 1, "pageSize": 10, "totalRecords": 0}
        respx.get("http://localhost:8686/api/v1/queue", params={
            "page": 1,
            "pageSize": 10,
            "sortKey": "timeleft",
            "sortDirection": "ascending"
        }).mock(return_value=Response(200, json=mock_queue))

        result = lidarr_client.get_queue()
        assert result == mock_queue

    @respx.mock
    def test_get_history(self, lidarr_client):
        mock_history = {"records": [], "page": 1, "pageSize": 10, "totalRecords": 0}
        respx.get("http://localhost:8686/api/v1/history", params={
            "page": 1,
            "pageSize": 10,
            "sortKey": "date",
            "sortDirection": "descending"
        }).mock(return_value=Response(200, json=mock_history))

        result = lidarr_client.get_history()
        assert result == mock_history

    @respx.mock
    def test_get_blocklist(self, lidarr_client):
        mock_blocklist = {"records": [], "page": 1, "pageSize": 10, "totalRecords": 0}
        respx.get("http://localhost:8686/api/v1/blocklist", params={"page": 1, "pageSize": 10}).mock(
            return_value=Response(200, json=mock_blocklist)
        )

        result = lidarr_client.get_blocklist()
        assert result == mock_blocklist

    @respx.mock
    def test_delete_blocklist_item(self, lidarr_client):
        respx.delete("http://localhost:8686/api/v1/blocklist/123").mock(return_value=Response(200))

        result = lidarr_client.delete_blocklist_item(123)
        assert result == {"status": "deleted", "id": 123}

    @respx.mock
    def test_list_import_list_exclusions(self, lidarr_client):
        mock_exclusions = [{"id": 1, "foreignId": "mbid-123", "artistName": "Adele"}]
        respx.get("http://localhost:8686/api/v1/importlistexclusion").mock(
            return_value=Response(200, json=mock_exclusions)
        )

        result = lidarr_client.list_import_list_exclusions()
        assert result == mock_exclusions

    @respx.mock
    def test_add_import_list_exclusion(self, lidarr_client):
        mock_added = {"id": 1, "foreignId": "mbid-123", "artistName": "Adele"}
        respx.post("http://localhost:8686/api/v1/importlistexclusion").mock(
            return_value=Response(200, json=mock_added)
        )

        result = lidarr_client.add_import_list_exclusion("mbid-123", "Adele")
        assert result == mock_added

    @respx.mock
    def test_delete_import_list_exclusion(self, lidarr_client):
        respx.delete("http://localhost:8686/api/v1/importlistexclusion/1").mock(return_value=Response(200))

        result = lidarr_client.delete_import_list_exclusion(1)
        assert result == {"status": "deleted", "id": 1}

    @respx.mock
    def test_get_system_status_http_error(self, lidarr_client):
        respx.get("http://localhost:8686/api/v1/system/status").mock(return_value=Response(500))

        with pytest.raises(Exception):
            lidarr_client.get_system_status()
