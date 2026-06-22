# 🧑‍🎨 usuarios · Synthetic User Profiles for Service Design

> Create research-backed user profiles that validate your designs across every sprint.

**usuarios** is an MCP server that turns your service design research (interviews, observations, field notes) into **synthetic user profiles** — rich, 12-dimension archetypes you can use to validate designs, align teams, and test ideas. All through natural conversation in Claude Desktop or Codex Desktop.

---

## 🚀 What your team says vs. what happens

| They say | The AI does |
|---|---|
| *"Creá usuarios sintéticos de las entrevistas"* | Analyzes your research, extracts patterns, generates full profiles |
| *"Validá el onboarding contra María"* | Tests your design against María's criteria, returns a report |
| *"¿Cómo va el proyecto?"* | Shows a dashboard with research → patterns → profiles → validations |
| *"Refiná el perfil de Juan"* | Updates the profile with new insights, versions it |

**Zero technical knowledge needed.** Your team just chats.

---

## 📦 Installation (2 minutes)

### 1. Install `uv`

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Configure your AI desktop app

**Claude Desktop**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "usuarios": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Sebtiago/usuarios-mcp",
        "usuarios-mcp"
      ]
    }
  }
}
```

**Codex Desktop**: Edit `~/.codex/config.toml`:

```toml
[mcp_servers.usuarios]
command = "uvx"
args = [
  "--from",
  "git+https://github.com/Sebtiago/usuarios-mcp",
  "usuarios-mcp"
]
```

### 3. Restart your app and start chatting

> *"Inicializá usuarios para este proyecto"*

That's it. The server handles everything else.

---

## 🧬 What's inside a profile? (12 dimensions)

Based on *This Is Service Design Doing*, *Mapping Experiences*, and the Touchpoint Journal:

| Dimension | What it captures |
|---|---|
| 1. **Identity** | Name, archetype, real quotes from research |
| 2. **Empathy Map** | Sees, hears, thinks/feels, says/does |
| 3. **Jobs-to-be-Done** | When/I want/So I can (functional, emotional, social) |
| 4. **Pain Points** | Intensity, frequency, context, traceability |
| 5. **Behaviors** | Patterns, triggers, workarounds |
| 6. **Mindset** | Beliefs, tech literacy, change attitude |
| 7. **Ecosystem** | Current tools, key people in their network |
| 8. **Scenarios** | Real usage flows with emotional arcs |
| 9. **Emotional Journey** | Stage-by-stage emotion map |
| 10. **Validation Criteria** | Intent principles + testable questions |
| 11. **Traceability** | Direct/Inferred/Speculative %, all sources cited |
| 12. **Metadata** | Version, expiration (12 months), human validation |

Every profile is saved in both **JSON** (machine-readable) and **Markdown** (team-readable).

---

## 🔄 The flow

```
INVESTIGACIÓN → ANÁLISIS → PERFILES → VALIDACIÓN → EVOLUCIÓN
 (research/)   (patterns/) (profiles/) (validations/)  (versioned)
```

The AI host orchestrates everything automatically. You never touch the tools directly.

---

## 📂 Project structure

After initialization, your project looks like this:

```
your-project/
└── .usuarios/
    ├── config.yaml          # Project settings
    ├── research/            # Drop your interview files here (.md, .txt)
    │   ├── entrevista-1.md
    │   └── focus-group.md
    ├── patterns/            # Extracted patterns (auto-generated)
    │   ├── patterns.json
    │   └── patterns.md
    ├── profiles/            # Your synthetic users (auto-generated)
    │   ├── maria-cuidadora.json
    │   └── maria-cuidadora.md
    └── validations/         # Design validation reports
        └── 2026-06-22-onboarding.md
```

---

## 🛠️ Development

```bash
# Clone
git clone https://github.com/Sebtiago/usuarios-mcp.git
cd usuarios-mcp

# Install dependencies
uv sync

# Run locally
uv run python main.py

# Customize templates (optional)
# Create .usuarios/templates/analyze.md in your project
# to override the default analysis methodology
```

---

## 🔒 Privacy

- **Runs locally.** No cloud, no API keys, no data leaves your machine.
- **Does not call LLM APIs.** The AI host (Claude/GPT) processes everything with its existing model.
- **Your research data stays in `.usuarios/`** in your project folder.

---

## 📚 Methodology

This tool implements the service design methodology from:

- *This Is Service Design Doing* — Stickdorn, Hormess, et al.
- *Good Services* — Louise Downe
- *Mapping Experiences* — Jim Kalbach
- Touchpoint: The Journal of Service Design
- Analysis-Synthesis Bridge Model for AI in design

---

## 📄 License

MIT © [Santiago Sirias](https://github.com/Sebtiago)

---

**Built for designers, by a designer.** If this helps your team, ⭐ the repo.
