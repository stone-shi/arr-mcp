# Agent Handover & Guidelines

Welcome, Agent! This repository implements **Arr-MCP**, a Model Context Protocol (MCP) server providing access to Lidarr, Radarr, and Sonarr APIs.

This guide provides instructions on the codebase structure, execution, guidelines, and context.

---

## 📂 Project Structure

```
.
├── clients/                  # API Clients for each service
│   ├── lidarr.py             # Lidarr client and tools
│   ├── radarr.py             # Radarr client and tools
│   └── sonarr.py             # Sonarr client and tools
├── main.py                   # Main entry point & MCP server initialization
├── config.py                 # Configuration settings via Pydantic Settings
├── Dockerfile                # Docker setup
├── docker-compose.yml        # Docker compose file for SSE mode
├── requirements.txt          # Python dependencies
├── .env.example              # Dummy environment file template
└── README.md                 # User-facing README
```

---

## ⚙️ Configuration & Secrets

> [!IMPORTANT]
> **Privacy First**: Do NOT commit or push the `.env` file or any credentials (API keys, internal domain names) to git. They are ignored by `.gitignore`. Keep `README.md` clean of active secrets.

Local configuration is loaded via environment variables or the local `.env` file:
* `LIDARR_URL`, `LIDARR_API_KEY`
* `RADARR_URL`, `RADARR_API_KEY`
* `SONARR_URL`, `SONARR_API_KEY`
* `ARR_SSL_VERIFY` (Toggle SSL certificate validation; defaults to `False` for self-signed certificates)
* `MCP_TRANSPORT` (Options: `stdio` or `sse`)
* `MCP_HOST` / `MCP_PORT` (Relevant for `sse` transport)

---

## 🛠️ Operational Tasks

### Running the Server
* **stdio Mode (default)**:
  ```bash
  python main.py
  ```
* **SSE Mode**:
  ```bash
  MCP_TRANSPORT=sse MCP_HOST=0.0.0.0 MCP_PORT=8000 python main.py
  ```
* **Docker Compose (SSE Mode)**:
  ```bash
  docker compose up --build -d
  ```

---

## 💡 Developer Guidelines for Future Agents

1. **Adding New Tools**:
   * If you need to extend APIs, modify the respective client class in `clients/{service}.py`.
   * Register the new tool in `main.py` using `mcp.tool()`. Make sure to add proper docstrings and parameter schemas.
2. **SSL / HTTPS Handling**:
   * Ensure that all http/https client calls respect the `verify_ssl` settings. Many environments use self-signed certificates.
3. **Pydantic**:
   * Settings loading uses `pydantic-settings`. Any new config variables should be added to `config.py`.
4. **Media Retrieval Guidelines**:
   * **Do not use list calls** (e.g., listing all movies, series, artists, or albums) to find a specific media item. Always use the search/lookup tools instead. Listing calls fetch the entire library (even with local pagination, the server must fetch all items from the upstream service), whereas search calls are optimized for finding specific items.
