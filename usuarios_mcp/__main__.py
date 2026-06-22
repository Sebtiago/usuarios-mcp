#!/usr/bin/env python3
"""
usuarios-mcp — MCP server for synthetic user profile generation.

The server communicates via stdio (JSON-RPC 2.0) and works with any
MCP-compatible host: Claude Desktop, Codex Desktop, VS Code, etc.
"""

from usuarios_mcp.internal.mcp.server import create_server, run_server


def main():
    """Entrypoint: create and run the MCP server."""
    server = create_server()
    run_server(server)


if __name__ == "__main__":
    main()
