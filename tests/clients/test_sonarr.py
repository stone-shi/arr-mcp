import pytest
import respx
from httpx import Response
from clients.sonarr import SonarrClient


class TestSonarrClientInit:
    def test_base_url_strips_trailing_slash(self):
        client = SonarrClient("http://localhost:8989/", "test-key")
        assert client.base_url == "http://localhost:8989/api/v3"

    def test_base_url_without_trailing_slash(self):
        client = SonarrClient("http://localhost:8989", "test-key")
        assert client.base_url == "http://localhost:8989/api/v3"

    def test_headers_contain_api_key(self):
        client = SonarrClient("http://localhost:8989", "test-key")
        assert client.headers["X-Api-Key"] == "test-key"


class TestSonarrClientMethods:
    @respx.mock
    def test_get_health(self, sonarr_client):
        mock_status = {"version": "3.0.0", "osName": "linux"}
        mock_health = [{"source": "System", "type": "info", "message": "All good"}]

        respx.get("http://localhost:8989/api/v3/system/status").mock(return_value=Response(200, json=mock_status))
        respx.get("http://localhost:8989/api/v3/health").mock(return_value=Response(200, json=mock_health))

        result = sonarr_client.get_health()
        assert result == {"status": mock_status, "health": mock_health}

    @respx.mock
    def test_list_series(self, sonarr_client):
        mock_series = [{"id": 1, "title": "Series 1"}, {"id": 2, "title": "Series 2"}]
        respx.get("http://localhost:8989/api/v3/series").mock(return_value=Response(200, json=mock_series))

        result = sonarr_client.list_series()
        assert result == mock_series

    @respx.mock
    def test_search_series(self, sonarr_client):
        mock_results = [{"id": 1, "title": "The Boys"}]
        respx.get("http://localhost:8989/api/v3/series/lookup", params={"term": "The Boys"}).mock(
            return_value=Response(200, json=mock_results)
        )

        result = sonarr_client.search_series("The Boys")
        assert result == mock_results

    @respx.mock
    def test_get_configs(self, sonarr_client):
        mock_folders = [{"path": "/tv"}]
        mock_profiles = [{"id": 1, "name": "HD-1080p"}]
        mock_lang_profiles = [{"id": 1, "name": "English"}]

        respx.get("http://localhost:8989/api/v3/rootfolder").mock(return_value=Response(200, json=mock_folders))
        respx.get("http://localhost:8989/api/v3/qualityprofile").mock(return_value=Response(200, json=mock_profiles))
        respx.get("http://localhost:8989/api/v3/languageprofile").mock(return_value=Response(200, json=mock_lang_profiles))

        result = sonarr_client.get_configs()
        assert result == {
            "rootFolders": mock_folders,
            "qualityProfiles": mock_profiles,
            "languageProfiles": mock_lang_profiles
        }

    @respx.mock
    def test_add_series(self, sonarr_client):
        series_data = {"title": "The Boys", "tvdbId": 123, "qualityProfileId": 1, "rootFolderPath": "/tv"}
        mock_added = {"id": 1, "title": "The Boys"}

        respx.post("http://localhost:8989/api/v3/series").mock(return_value=Response(200, json=mock_added))

        result = sonarr_client.add_series(series_data)
        assert result == mock_added

    @respx.mock
    def test_delete_series(self, sonarr_client):
        respx.delete("http://localhost:8989/api/v3/series/123", params={"deleteFiles": True}).mock(
            return_value=Response(200)
        )

        result = sonarr_client.delete_series(123, delete_files=True)
        assert result == {"status": "deleted", "id": 123}

    @respx.mock
    def test_get_queue(self, sonarr_client):
        mock_queue = {"records": [], "page": 1, "pageSize": 10}
        respx.get("http://localhost:8989/api/v3/queue").mock(return_value=Response(200, json=mock_queue))

        result = sonarr_client.get_queue()
        assert result == mock_queue

    @respx.mock
    def test_get_history(self, sonarr_client):
        mock_history = {"records": [], "page": 1, "pageSize": 20}
        respx.get("http://localhost:8989/api/v3/history", params={"pageSize": 20}).mock(
            return_value=Response(200, json=mock_history)
        )

        result = sonarr_client.get_history(limit=20)
        assert result == mock_history

    @respx.mock
    def test_post_command(self, sonarr_client):
        mock_response = {"id": 1, "name": "SeriesSearch"}
        respx.post("http://localhost:8989/api/v3/command").mock(return_value=Response(200, json=mock_response))

        result = sonarr_client.post_command("SeriesSearch")
        assert result == mock_response

    @respx.mock
    def test_get_episodes(self, sonarr_client):
        mock_episodes = [{"id": 1, "episodeNumber": 1}, {"id": 2, "episodeNumber": 2}]
        respx.get("http://localhost:8989/api/v3/episode", params={"seriesId": 123}).mock(
            return_value=Response(200, json=mock_episodes)
        )

        result = sonarr_client.get_episodes(123)
        assert result == mock_episodes

    @respx.mock
    def test_get_blocklist(self, sonarr_client):
        mock_blocklist = {"records": [], "page": 1, "pageSize": 20}
        respx.get("http://localhost:8989/api/v3/blocklist", params={"page": 1, "pageSize": 20}).mock(
            return_value=Response(200, json=mock_blocklist)
        )

        result = sonarr_client.get_blocklist()
        assert result == mock_blocklist

    @respx.mock
    def test_delete_blocklist_item(self, sonarr_client):
        respx.delete("http://localhost:8989/api/v3/blocklist/123").mock(return_value=Response(200))

        result = sonarr_client.delete_blocklist_item(123)
        assert result == {"status": "deleted", "id": 123}
