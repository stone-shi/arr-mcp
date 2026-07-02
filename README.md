# Arr-MCP Server

A unified Model Context Protocol (MCP) server providing access to **Lidarr**, **Radarr**, and **Sonarr** APIs. This allows AI assistants (like Claude, Cursor, etc.) to query system statuses, list resources, search for media, add/update library entries, monitor download queues, trigger system commands, and inspect event history.

## Features & Tools

### Lidarr (Music)
- `lidarr_get_status`: Get system status and version.
- `lidarr_list_artists`: List all artists in the library.
- `lidarr_search_artists`: Search for new artists on MusicBrainz lookup.
- `lidarr_list_albums`: List albums, optionally filtered by artist ID.
- `lidarr_get_queue`: Get current download queue.
- `lidarr_get_history`: Get system event history.
- `lidarr_trigger_command`: Trigger Lidarr system commands.

### Radarr (Movies)
- `radarr_get_status`: Get system status and version.
- `radarr_list_movies`: List movies in the library.
- `radarr_get_movie`: Get detailed details for a movie.
- `radarr_search_movie`: Search for movies to add.
- `radarr_add_movie`: Add a movie by TMDB ID, setting root folders and quality profiles automatically if omitted.
- `radarr_update_movie`: Update monitored status or quality profile for a movie.
- `radarr_delete_movie`: Delete a movie (optionally deleting files).
- `radarr_list_root_folders`: List configured directories.
- `radarr_list_quality_profiles`: List quality profiles.
- `radarr_get_queue`: Get active downloads.
- `radarr_get_history`: Get historical events.
- `radarr_trigger_command`: Run a Radarr command.
- `radarr_list_indexers`: List configured indexers.
- `radarr_test_indexer`: Run a verification test for an indexer.

### Sonarr (TV Shows)
- `sonarr_get_health`: Check health and system status.
- `sonarr_list_series`: List all series in the library.
- `sonarr_search_series`: Search for new TV shows.
- `sonarr_get_configs`: Retrieve root folders, quality profiles, and language profiles.
- `sonarr_add_series`: Add a series with standard configurations.
- `sonarr_delete_series`: Delete a TV show (optionally deleting files).
- `sonarr_get_queue`: Show current downloads.
- `sonarr_get_history`: Show event history.
- `sonarr_trigger_command`: Trigger Sonarr system commands.
- `sonarr_list_episodes`: List episodes for a TV series.

---

## Installation & Setup

1. **Clone/Move into directory**:
   ```bash
   cd /data/homes/stoneshi/src/arr-mcp
   ```

2. **Create Environment Configuration**:
   Copy `.env.example` to `.env` and fill in the details:
   ```bash
   cp .env.example .env
   ```

   Ensure the variables are set correctly:
   ```env
   LIDARR_URL=https://lidarr.example.com
   LIDARR_API_KEY=your_lidarr_api_key

   RADARR_URL=https://radarr.example.com
   RADARR_API_KEY=your_radarr_api_key

   SONARR_URL=https://sonarr.example.com
   SONARR_API_KEY=your_sonarr_api_key

   # Disable SSL verification since we use internal domain names with self-signed certificates
   ARR_SSL_VERIFY=False

   # MCP Transport settings (stdio or sse)
   MCP_TRANSPORT=stdio
   MCP_HOST=0.0.0.0
   MCP_PORT=8000
   ```

3. **Install Dependencies**:
   Create a virtual environment and install the required modules:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Running the Server

### Option A: Local Process (stdio)
By default, the server runs using standard input/output (`stdio`) when executed:
```bash
./venv/bin/python main.py
```

### Option B: Network Accessible (SSE & Streamable HTTP)
To run the server over the network (supporting both Server-Sent Events and Streamable HTTP on the same port), set `MCP_TRANSPORT` (e.g., `sse`, `streamable-http`, or `http`):
```bash
MCP_TRANSPORT=sse MCP_HOST=0.0.0.0 MCP_PORT=8000 ./venv/bin/python main.py
```

Or configure inside your `.env` file:
```env
MCP_TRANSPORT=sse
MCP_HOST=0.0.0.0
MCP_PORT=8000
```
When running over network mode, the server exposes:
- **SSE Endpoint**: `http://<server-ip>:8000/sse`
- **Streamable HTTP Endpoint**: `http://<server-ip>:8000/mcp`


### Option C: Docker & Docker Compose (SSE)
You can run the server in a containerized environment using the provided `Dockerfile` and `docker-compose.yml`:

1. **Start the Container**:
   Make sure you have populated the `.env` file with your URL and API credentials, then run:
   ```bash
   docker compose up -d
   ```

2. **Check Logs**:
   Verify that the server starts up properly:
   ```bash
   docker compose logs -f
   ```

3. **Validate Connection**:
   Ensure it is listening on port `8000`:
   ```bash
   curl http://localhost:8000/sse
   ```

---

## Client Configuration

### 1. Local stdio Client (e.g., Claude Desktop / Cursor)

To integrate this local server into an MCP client, add the following entry to your configuration file (e.g., `~/config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "/data/homes/stoneshi/src/arr-mcp/venv/bin/python",
      "args": [
        "/data/homes/stoneshi/src/arr-mcp/main.py"
      ],
      "env": {
        "LIDARR_URL": "https://lidarr.example.com",
        "LIDARR_API_KEY": "your_lidarr_api_key",
        "RADARR_URL": "https://radarr.example.com",
        "RADARR_API_KEY": "your_radarr_api_key",
        "SONARR_URL": "https://sonarr.example.com",
        "SONARR_API_KEY": "your_sonarr_api_key",
        "ARR_SSL_VERIFY": "False"
      }
    }
  }
}
```

### 2. Network Client (SSE)

To connect remote clients to the server running over the network, specify the SSE endpoint in the client's settings:
- **SSE URL**: `http://<server-ip>:8000/sse`

