"""
MCP server core — creates and configures the FastMCP server instance.

Based on the MCP specification (modelcontextprotocol.io), protocol version 2025-06-18.
Uses stdio transport for direct process communication.
"""

from mcp.server.fastmcp import FastMCP

# Server identity — matches the MCP spec's Implementation type
SERVER_NAME = "usuarios"
SERVER_VERSION = "0.1.0"

# Server instructions — read by Claude Desktop / Codex Desktop as server-wide guidance.
# The MCP spec says: "use `instructions` for cross-tool workflows, constraints,
# and rate limits that apply across the server. Keep the first 512 characters
# self-contained so the most important guidance is available when Codex is
# deciding how to use the server."
INSTRUCTIONS = """# usuarios — Synthetic User Profile Generator

This server creates synthetic user profiles (archetypes/personas) from
service design research data. Methodology: "This Is Service Design Doing",
the Analysis-Synthesis Bridge Model, and Touchpoint Journal.

## 🚀 Autonomous workflows — follow these WITHOUT asking the user

### When user says "create users / crear usuarios / analizar investigación"

Follow this flow END-TO-END without stopping to ask:

1. Call `quick_status` to see project state.
2. If not initialized → call `init_project` first.
3. Call `get_research_prompt` → get the analysis prompt.
4. Process it with your LLM → extract patterns following the methodology.
5. Call `save_patterns` with the structured result.
6. Call `get_generate_prompt` → get the profile generation prompt.
7. Process it → generate 12-dimension profiles.
8. Call `save_profile` for EACH generated profile.
9. Call `quick_status` again → show the user a friendly summary with:
   - Number of profiles created
   - Names, archetypes, and one-line descriptions
   - Traceability percentages
   - The next suggested step: validation

### When user says "validate / validar / test design against X"

1. Call `list_profiles` to let the user pick (or auto-pick if specified).
2. For each relevant profile:
   - Call `get_validate_prompt` with the profile ID and design file.
   - Process it → evaluate against the user's criteria.
   - Call `save_validation` to persist the report.
3. Show a concise verdict with critical findings (🟢🟡🔴 format).
4. Suggest concrete next steps.

### When user says "show / ver / list profiles / estado"

1. Call `quick_status` for the dashboard view.
2. If they want a specific profile, call `get_profile` with format="markdown".
3. Present profiles in natural language, never raw JSON.

### When user says "refine / improve / actualizar profile X"

1. Call `get_profile` with format="json" to get the current version.
2. Process the refinement request against the existing data.
3. Call `save_profile` with the updated version (increment version number).
4. Show what changed.

## 🎯 UX principles

- NEVER expose tool names to the user. They don't need to know about init_project,
  they just want "crear usuarios sintéticos".
- NEVER show raw JSON to the user. Always translate to natural language with emojis.
- ALWAYS show a summary after completing any multi-step workflow.
- When in doubt, call `quick_status` first — it gives you the project dashboard.
- SPEAK THE USER'S LANGUAGE. Match their language in all responses.
- Be warm and encouraging — these are designers, not developers.

## 📐 Methodology

- Triangulation: cross-reference findings across multiple sources
- Traceability: every profile field must be tagged directo/inferido/especulativo
- 12-dimension profiles: identity, empathy map, JTBD, pain points, behaviors,
  mindset, ecosystem, scenarios, emotional journey, validation criteria,
  traceability, metadata
- Profiles expire after 12 months (mark fecha_expiracion)
- Focus on goals and behaviors, not demographics alone
- Human-in-the-loop: mark `validado_por_humano: false` until reviewed

## 🔧 Server facts

- Does NOT call any LLM API. You (the AI host) process all prompts.
- Works locally via stdio — no cloud, no API keys needed.
- Both Claude Desktop and Codex Desktop supported.
- Project data stored in .usuarios/ directory."""


def create_server() -> FastMCP:
    """Create and configure the MCP server instance.

    FastMCP uses the name and instructions parameters for server identity.
    The instructions field is read by MCP hosts as server-wide guidance.
    """
    server = FastMCP(
        name=SERVER_NAME,
        instructions=INSTRUCTIONS,
    )

    # Register all tools
    _register_tools(server)

    return server


def _register_tools(server: FastMCP) -> None:
    """Register all tool handlers on the server."""
    from usuarios_mcp.internal.mcp.tools import register_tools

    register_tools(server)


def run_server(server: FastMCP) -> None:
    """Run the MCP server with stdio transport.

    As per the MCP spec:
    - Server reads JSON-RPC messages from stdin
    - Server writes JSON-RPC responses to stdout
    - Messages are newline-delimited, no embedded newlines
    - Server may write UTF-8 strings to stderr for logging
    - Server MUST NOT write anything to stdout that is not a valid MCP message
    """
    import sys
    import logging

    # Configure logging to stderr only (stdout is reserved for JSON-RPC)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    server.run(transport="stdio")
