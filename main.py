from mcp.server.fastmcp import FastMCP
from config import settings
from clients import LidarrClient, RadarrClient, SonarrClient
import logging
from typing import List, Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("arr-mcp")

# Instantiate MCP with network configurations
mcp = FastMCP(
    "Arr-MCP",
    host=settings.mcp_host,
    port=settings.mcp_port
)

# Initialize Clients
lidarr = LidarrClient(settings.lidarr_url, settings.lidarr_api_key, settings.arr_ssl_verify)
radarr = RadarrClient(settings.radarr_url, settings.radarr_api_key, settings.arr_ssl_verify)
sonarr = SonarrClient(settings.sonarr_url, settings.sonarr_api_key, settings.arr_ssl_verify)

# ----------------- Lidarr Tools -----------------

@mcp.tool()
def lidarr_get_status() -> dict:
    """Get the system status and version information from the Lidarr server."""
    logger.info("lidarr_get_status called")
    return lidarr.get_system_status()

@mcp.tool()
def lidarr_list_artists() -> list:
    """List all artists in the Lidarr library."""
    logger.info("lidarr_list_artists called")
    return lidarr.get_artists()

@mcp.tool()
def lidarr_search_artists(term: str) -> list:
    """Search for new artists to add (artist lookup on musicbrainz/Lidarr metadata service).
    
    Args:
        term: Search term/artist name (e.g. 'Adele').
    """
    logger.info(f"lidarr_search_artists called with term: {term}")
    return lidarr.search_artists(term)

@mcp.tool()
def lidarr_list_albums(artist_id: Optional[int] = None) -> list:
    """List albums in the Lidarr library, optionally filtered by artist ID.
    
    Args:
        artist_id: Optional artist ID to filter albums.
    """
    logger.info(f"lidarr_list_albums called with artist_id: {artist_id}")
    return lidarr.get_albums(artist_id)

@mcp.tool()
def lidarr_trigger_command(name: str, params: Optional[dict] = None) -> dict:
    """Execute a system command in Lidarr.
    
    Args:
        name: Name of the command (e.g., 'RefreshArtist', 'ApplicationUpdate').
        params: Optional dictionary of additional command parameters.
    """
    logger.info(f"lidarr_trigger_command called: {name}")
    p = params or {}
    return lidarr.post_command(name, **p)

@mcp.tool()
def lidarr_get_queue(page: int = 1, page_size: int = 10) -> dict:
    """Show the download queue with pagination.
    
    Args:
        page: Page number to fetch (default: 1).
        page_size: Number of items per page (default: 10).
    """
    logger.info(f"lidarr_get_queue called (page={page}, page_size={page_size})")
    return lidarr.get_queue(page, page_size)

@mcp.tool()
def lidarr_get_history(page: int = 1, page_size: int = 10) -> dict:
    """Show activity history with pagination.
    
    Args:
        page: Page number to fetch (default: 1).
        page_size: Number of items per page (default: 10).
    """
    logger.info(f"lidarr_get_history called (page={page}, page_size={page_size})")
    return lidarr.get_history(page, page_size)


# ----------------- Radarr Tools -----------------

@mcp.tool()
def radarr_get_status() -> dict:
    """Get the system status and version information from the Radarr server."""
    logger.info("radarr_get_status called")
    return radarr.get_system_status()

@mcp.tool()
def radarr_list_movies() -> list:
    """List all movies in the Radarr library."""
    logger.info("radarr_list_movies called")
    return radarr.list_movies()

@mcp.tool()
def radarr_get_movie(movie_id: int) -> dict:
    """Get details for a specific movie in the Radarr library by its Radarr ID.
    
    Args:
        movie_id: The ID of the movie in Radarr.
    """
    logger.info(f"radarr_get_movie called with id: {movie_id}")
    return radarr.get_movie(movie_id)

@mcp.tool()
def radarr_search_movie(term: str) -> list:
    """Search for movies to add (term lookup).
    
    Args:
        term: Search term/movie title (e.g. 'Inception').
    """
    logger.info(f"radarr_search_movie called with term: {term}")
    return radarr.search_movie(term)

@mcp.tool()
def radarr_add_movie(
    tmdb_id: int,
    root_folder: Optional[str] = None,
    quality_profile_id: Optional[int] = None,
    monitored: bool = True,
    search_for_movie: bool = False
) -> dict:
    """Add a movie to the Radarr library.
    
    Args:
        tmdb_id: TMDB ID of the movie to add.
        root_folder: Root folder path. If not provided, the first available root folder is used.
        quality_profile_id: Quality profile ID. If not provided, the first available profile is used.
        monitored: Whether to monitor the movie.
        search_for_movie: Search for the movie immediately on addition.
    """
    logger.info(f"radarr_add_movie called for tmdb_id={tmdb_id}")
    return radarr.add_movie(tmdb_id, root_folder, quality_profile_id, monitored, search_for_movie)

@mcp.tool()
def radarr_update_movie(
    movie_id: int,
    monitored: Optional[bool] = None,
    quality_profile_id: Optional[int] = None
) -> dict:
    """Update settings for a movie in the Radarr library.
    
    Args:
        movie_id: The Radarr ID of the movie to update.
        monitored: Set monitored status.
        quality_profile_id: Set quality profile ID.
    """
    logger.info(f"radarr_update_movie called for movie_id={movie_id}")
    return radarr.update_movie(movie_id, monitored, quality_profile_id)

@mcp.tool()
def radarr_delete_movie(
    movie_id: int,
    delete_files: bool = False,
    add_import_exclusion: bool = False
) -> dict:
    """Delete a movie from the Radarr library.
    
    Args:
        movie_id: The Radarr ID of the movie to delete.
        delete_files: Also delete movie files from disk.
        add_import_exclusion: Add the movie to import exclusions to prevent re-adding.
    """
    logger.info(f"radarr_delete_movie called for movie_id={movie_id}")
    return radarr.delete_movie(movie_id, delete_files, add_import_exclusion)

@mcp.tool()
def radarr_list_root_folders() -> list:
    """List root folders configured in Radarr, along with free/total space."""
    logger.info("radarr_list_root_folders called")
    return radarr.list_root_folders()

@mcp.tool()
def radarr_list_quality_profiles() -> list:
    """List quality profiles configured in Radarr."""
    logger.info("radarr_list_quality_profiles called")
    return radarr.list_quality_profiles()

@mcp.tool()
def radarr_get_queue(page: int = 1, page_size: int = 20) -> dict:
    """Show the download queue in Radarr with pagination.
    
    Args:
        page: Page number to fetch (default: 1).
        page_size: Number of items per page (default: 20).
    """
    logger.info(f"radarr_get_queue called (page={page}, page_size={page_size})")
    return radarr.get_queue(page, page_size)

@mcp.tool()
def radarr_get_history(page: int = 1, page_size: int = 20) -> dict:
    """Show activity history in Radarr with pagination.
    
    Args:
        page: Page number to fetch (default: 1).
        page_size: Number of items per page (default: 20).
    """
    logger.info(f"radarr_get_history called (page={page}, page_size={page_size})")
    return radarr.get_history(page, page_size)

@mcp.tool()
def radarr_trigger_command(name: str, params: Optional[dict] = None) -> dict:
    """Execute a system command in Radarr.
    
    Args:
        name: Name of the command (e.g., 'RefreshMovie', 'RenameMovie', 'RssSync').
        params: Optional dictionary of additional command parameters.
    """
    logger.info(f"radarr_trigger_command called: {name}")
    p = params or {}
    return radarr.post_command(name, **p)

@mcp.tool()
def radarr_list_indexers() -> list:
    """List configured indexers in Radarr."""
    logger.info("radarr_list_indexers called")
    return radarr.list_indexers()

@mcp.tool()
def radarr_test_indexer(indexer_id: int) -> dict:
    """Test a specific indexer configuration.
    
    Args:
        indexer_id: The ID of the indexer to test.
    """
    logger.info(f"radarr_test_indexer called for indexer_id={indexer_id}")
    return radarr.test_indexer(indexer_id)


# ----------------- Sonarr Tools -----------------

@mcp.tool()
def sonarr_get_health() -> dict:
    """Check Sonarr health and system status."""
    logger.info("sonarr_get_health called")
    return sonarr.get_health()

@mcp.tool()
def sonarr_list_series() -> list:
    """List all TV series in the Sonarr library."""
    logger.info("sonarr_list_series called")
    return sonarr.list_series()

@mcp.tool()
def sonarr_search_series(term: str) -> list:
    """Search for new series (lookup).
    
    Args:
        term: Search term/series title (e.g. 'The Boys').
    """
    logger.info(f"sonarr_search_series called with term: {term}")
    return sonarr.search_series(term)

@mcp.tool()
def sonarr_get_configs() -> dict:
    """Get root folders, quality profiles, and language profiles from Sonarr."""
    logger.info("sonarr_get_configs called")
    return sonarr.get_configs()

@mcp.tool()
def sonarr_add_series(series_data: dict) -> dict:
    """Add a series to the Sonarr library.
    
    Args:
        series_data: Dictionary of series data (obtained from sonarr_search_series and sonarr_get_configs).
            Example fields: title, tvdbId, qualityProfileId, rootFolderPath, monitored, seriesType.
    """
    logger.info("sonarr_add_series called")
    return sonarr.add_series(series_data)

@mcp.tool()
def sonarr_delete_series(series_id: int, delete_files: bool = False) -> dict:
    """Delete a TV series from the Sonarr library.
    
    Args:
        series_id: The ID of the series in Sonarr.
        delete_files: Also delete series files from disk.
    """
    logger.info(f"sonarr_delete_series called for series_id={series_id}")
    return sonarr.delete_series(series_id, delete_files)

@mcp.tool()
def sonarr_get_queue() -> dict:
    """Show the download queue in Sonarr."""
    logger.info("sonarr_get_queue called")
    return sonarr.get_queue()

@mcp.tool()
def sonarr_get_history(limit: int = 20) -> dict:
    """Show activity history in Sonarr.
    
    Args:
        limit: Max number of history items to return (default: 20).
    """
    logger.info(f"sonarr_get_history called (limit={limit})")
    return sonarr.get_history(limit)

@mcp.tool()
def sonarr_trigger_command(name: str, params: Optional[dict] = None) -> dict:
    """Execute a system command in Sonarr.
    
    Args:
        name: Name of the command (e.g., 'SeriesSearch', 'RescanSeries').
        params: Optional dictionary of additional command parameters.
    """
    logger.info(f"sonarr_trigger_command called: {name}")
    p = params or {}
    return sonarr.post_command(name, **p)

@mcp.tool()
def sonarr_list_episodes(series_id: int) -> list:
    """List episodes for a specific TV series in Sonarr.
    
    Args:
        series_id: The ID of the series in Sonarr.
    """
    logger.info(f"sonarr_list_episodes called for series_id={series_id}")
    return sonarr.get_episodes(series_id)


if __name__ == "__main__":
    transport = settings.mcp_transport.lower()
    if transport == "sse":
        logger.info(f"Starting Arr-MCP server over SSE on {settings.mcp_host}:{settings.mcp_port}...")
        mcp.run(transport="sse")
    else:
        logger.info("Starting Arr-MCP server over stdio...")
        mcp.run(transport="stdio")
