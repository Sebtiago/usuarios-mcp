#!/usr/bin/env bash
# Install usuarios-mcp MCP server
# Usage: bash install.sh

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BOLD}🔧 usuarios-mcp installer${NC}"
echo ""

# Detect OS
OS=$(uname -s)
case "$OS" in
  Darwin)  OS_NAME="macOS" ;;
  Linux)   OS_NAME="Linux" ;;
  *)       echo "❌ Unsupported OS: $OS"; exit 1 ;;
esac

echo -e "${BLUE}System:${NC} $OS_NAME"

# Check/install uv
if ! command -v uv &>/dev/null; then
  echo -e "${BLUE}Installing uv...${NC}"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo -e "${BLUE}uv:${NC} $(uv --version)"

# Get server path
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_PATH="$SCRIPT_DIR"

echo -e "${BLUE}Server path:${NC} $SERVER_PATH"

# Create launcher script
LAUNCHER="$HOME/.local/bin/usuarios-mcp"
mkdir -p "$(dirname "$LAUNCHER")"

cat > "$LAUNCHER" << 'LAUNCHER_EOF'
#!/usr/bin/env bash
# Launcher for usuarios-mcp MCP server
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REAL_SERVER="SCRIPT_DIR_PLACEHOLDER"
cd "$REAL_SERVER"
exec uv run python "$REAL_SERVER/main.py" "$@"
LAUNCHER_EOF

# Replace placeholder with actual path
sed -i.bak "s|SCRIPT_DIR_PLACEHOLDER|$SERVER_PATH|g" "$LAUNCHER"
rm -f "${LAUNCHER}.bak"

chmod +x "$LAUNCHER"
echo -e "${GREEN}✅ Launcher created:${NC} $LAUNCHER"

# Detect available desktop apps
echo ""
echo -e "${BOLD}📋 Desktop App Configuration${NC}"
echo ""

CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
CODEX_CONFIG="$HOME/.codex/config.toml"

# Claude Desktop
if [ -f "$CLAUDE_CONFIG" ] || [ -d "$(dirname "$CLAUDE_CONFIG")" ]; then
  echo -e "${BLUE}Claude Desktop detected.${NC}"
  echo -e "Add this to ${BOLD}$CLAUDE_CONFIG${NC}:"
  echo ""
  echo '  {'
  echo '    "mcpServers": {'
  echo '      "usuarios": {'
  echo "        \"command\": \"$LAUNCHER\","
  echo '        "args": []'
  echo '      }'
  echo '    }'
  echo '  }'
  echo ""
fi

# Codex Desktop  
CODEX_DIR="$(dirname "$CODEX_CONFIG")"
if [ -f "$CODEX_CONFIG" ] || [ -d "$CODEX_DIR" ]; then
  echo -e "${BLUE}Codex Desktop detected.${NC}"
  echo -e "Add this to ${BOLD}$CODEX_CONFIG${NC}:"
  echo ""
  echo '  [mcp_servers.usuarios]'
  echo "  command = \"$LAUNCHER\""
  echo '  args = []'
  echo ""
fi

echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Add the server config to your desktop app (see above)"
echo "  2. Restart Claude Desktop / Codex Desktop"
echo "  3. Open a project and say: \"Initialize usuarios for this project\""
