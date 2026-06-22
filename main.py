#!/usr/bin/env python3
"""
usuarios-mcp — MCP server for synthetic user profile generation.

Provides tools for service design research analysis, synthetic user profile
generation, and design validation — all through the Model Context Protocol.

Usage:
    uv run main.py
    # Or compile to binary: nuitka --standalone main.py

The server communicates via stdio (JSON-RPC 2.0) and works with any
MCP-compatible host: Claude Desktop, Codex Desktop, VS Code, etc.

It does NOT call any LLM APIs. It orchestrates the process by reading data,
rendering prompts, and persisting results. The AI host processes the prompts
using its own model.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from internal.mcp.server import create_server, run_server


def main():
    """Entrypoint: create and run the MCP server."""
    server = create_server()
    run_server(server)


if __name__ == "__main__":
    main()
