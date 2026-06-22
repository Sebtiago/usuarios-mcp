"""
MCP tool definitions for usuarios-mcp.

All tools follow the pattern: read data from project → format prompt or
persist result → return structured response. The server NEVER calls LLMs.
"""

from pathlib import Path
from typing import Optional
import json
import os

from mcp.server.fastmcp import FastMCP

from internal.project.config import (
    init_project as cfg_init,
    get_config,
    set_config,
)
from internal.project.research import (
    list_research_files,
    read_research_files,
)
from internal.project.profiles import (
    save_profile as prof_save,
    list_profiles as prof_list,
    get_profile as prof_get,
    save_validation as val_save,
    list_validations,
    get_validation,
)
from internal.templates.engine import (
    render_template,
    load_project_template,
)
from internal.schema.patterns import PATTERNS_SCHEMA
from internal.schema.profile import PROFILE_SCHEMA, PROFILE_MD_TEMPLATE
from internal.schema.validation import VALIDATION_SCHEMA
from internal.mcp.server import INSTRUCTIONS

# ---------------------------------------------------------------------------
# Tool registration
# ---------------------------------------------------------------------------

def register_tools(server: FastMCP) -> None:
    """Register all tool handlers on the FastMCP server."""
    _register_init(server)
    _register_research(server)
    _register_patterns(server)
    _register_profiles(server)
    _register_validation(server)
    _register_config(server)
    _register_status(server)


# ---------------------------------------------------------------------------
# 1. Project Initialization
# ---------------------------------------------------------------------------

def _register_init(server: FastMCP) -> None:

    @server.tool()
    def init_project(project_path: str) -> str:
        """Initialize a new usuarios project.

        Creates the .usuarios/ directory structure:
          .usuarios/
            config.yaml
            research/     <- Put interview files here
            patterns/     <- Analysis results go here
            profiles/     <- Generated profiles (JSON + MD)
            validations/  <- Validation reports

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            result = cfg_init(project_path)
            return json.dumps({
                "status": "ok",
                "message": f"Project initialized at {result['path']}",
                "structure": result["structure"],
                "next_steps": [
                    "1. Add research files to .usuarios/research/ (interviews, notes, etc.)",
                    "2. Call get_research_prompt to analyze the research",
                    "3. After AI analysis, call save_patterns to persist results",
                    "4. Call get_generate_prompt to generate profiles",
                    "5. Call save_profile for each generated profile",
                ],
            }, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 2. Research Operations
# ---------------------------------------------------------------------------

def _register_research(server: FastMCP) -> None:

    @server.tool()
    def list_research(project_path: str) -> str:
        """List all research files in the project.

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            files = list_research_files(project_path)
            return json.dumps({
                "status": "ok",
                "project_path": project_path,
                "files": files,
                "count": len(files),
            }, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def get_research_prompt(
        project_path: str,
        source_files: Optional[list[str]] = None,
    ) -> str:
        """Generate an analysis prompt from research data.

        Reads all research files (or specified subset) and returns a prompt
        that you (the AI host) should process with your LLM to extract:
        - Behavioral patterns
        - Pain points
        - Goals and motivations
        - Environment/context factors
        - Key differentiators between user segments

        After processing, call save_patterns with the structured result.

        Args:
            project_path: Absolute path to the project directory.
            source_files: Optional list of specific file names to analyze.
        """
        try:
            files = read_research_files(project_path, source_files)
            if not files:
                return json.dumps({
                    "status": "error",
                    "message": "No research files found. Add .md or .txt files to .usuarios/research/",
                })

            research_text = "\n\n---\n\n".join(
                f"## {f['filename']}\n{f['content']}" for f in files
            )

            prompt = render_template("analyze", {
                "research_data": research_text,
                "file_count": len(files),
                "file_list": [f["filename"] for f in files],
                "patterns_schema": PATTERNS_SCHEMA,
            })

            # Load project-specific template if it exists
            custom = load_project_template(project_path, "analyze")
            if custom:
                prompt = custom.replace("{{RESEARCH_DATA}}", research_text)

            return prompt
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 3. Pattern Persistence
# ---------------------------------------------------------------------------

def _register_patterns(server: FastMCP) -> None:

    @server.tool()
    def save_patterns(
        project_path: str,
        patterns: str,
    ) -> str:
        """Save extracted research patterns to the project.

        Accepts the patterns as a JSON string. The patterns should follow
        the structure provided by the get_research_prompt output.

        Args:
            project_path: Absolute path to the project directory.
            patterns: JSON string with the analysis results.
        """
        try:
            patterns_path = Path(project_path) / ".usuarios" / "patterns"
            patterns_path.mkdir(parents=True, exist_ok=True)

            # Validate JSON
            data = json.loads(patterns)

            # Save as JSON
            output_file = patterns_path / "patterns.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Also save a human-readable markdown version
            md_file = patterns_path / "patterns.md"
            md_content = _patterns_to_markdown(data)
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content)

            return json.dumps({
                "status": "ok",
                "message": "Patterns saved successfully",
                "files": {
                    "json": str(output_file),
                    "markdown": str(md_file),
                },
                "next_step": "Call get_generate_prompt to generate synthetic user profiles",
            }, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return json.dumps({
                "status": "error",
                "message": f"Invalid JSON: {str(e)}",
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 4. Profile Generation and Management
# ---------------------------------------------------------------------------

def _register_profiles(server: FastMCP) -> None:

    @server.tool()
    def get_generate_prompt(
        project_path: str,
        count: Optional[int] = None,
    ) -> str:
        """Generate a prompt for creating synthetic user profiles.

        Reads the patterns file and returns a prompt with the complete
        12-dimension profile schema for you to generate rich synthetic
        user profiles.

        Args:
            project_path: Absolute path to the project directory.
            count: Optional number of profiles to generate (default: auto-detect from patterns).
        """
        try:
            patterns_path = Path(project_path) / ".usuarios" / "patterns" / "patterns.json"
            if not patterns_path.exists():
                return json.dumps({
                    "status": "error",
                    "message": "No patterns found. Run analysis first: get_research_prompt → AI processing → save_patterns",
                })

            with open(patterns_path, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            prompt = render_template("generate", {
                "patterns": json.dumps(patterns, indent=2, ensure_ascii=False),
                "profile_schema": PROFILE_SCHEMA,
                "profile_md_template": PROFILE_MD_TEMPLATE,
                "count": count or "auto-detect from patterns",
            })

            # Load project-specific template if exists
            custom = load_project_template(project_path, "generate")
            if custom:
                prompt = custom.replace(
                    "{{PATTERNS}}",
                    json.dumps(patterns, indent=2, ensure_ascii=False),
                )

            return prompt
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def save_profile(
        project_path: str,
        profile: str,
    ) -> str:
        """Save a generated synthetic user profile.

        Saves both a JSON file (for machine consumption) and a Markdown file
        (for human consumption). The profile must follow the 12-dimension
        schema provided by get_generate_prompt.

        Args:
            project_path: Absolute path to the project directory.
            profile: JSON string with the 12-dimension profile.
        """
        try:
            data = json.loads(profile)
            profile_id = data.get("id", "profile")
            result = prof_save(project_path, profile_id, data)
            return json.dumps({
                "status": "ok",
                "message": f"Profile '{profile_id}' saved",
                "files": result,
                "next_step": "Call list_profiles to see all profiles, or get_profile to review one",
            }, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return json.dumps({"status": "error", "message": f"Invalid JSON: {str(e)}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def list_profiles(project_path: str) -> str:
        """List all synthetic user profiles in the project.

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            profiles = prof_list(project_path)
            return json.dumps({
                "status": "ok",
                "project_path": project_path,
                "profiles": profiles,
                "count": len(profiles),
            }, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def get_profile(
        project_path: str,
        profile_id: str,
        format: Optional[str] = "json",
    ) -> str:
        """Get a specific profile by ID.

        Args:
            project_path: Absolute path to the project directory.
            profile_id: The profile identifier (e.g. "maria-cuidadora").
            format: Output format: "json" (structured) or "markdown" (human-readable).
        """
        try:
            result = prof_get(project_path, profile_id, format or "json")
            if isinstance(result, dict):
                return json.dumps(result, indent=2, ensure_ascii=False)
            return result
        except FileNotFoundError:
            return json.dumps({
                "status": "error",
                "message": f"Profile '{profile_id}' not found. Use list_profiles to see available profiles.",
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 5. Validation
# ---------------------------------------------------------------------------

def _register_validation(server: FastMCP) -> None:

    @server.tool()
    def get_validate_prompt(
        project_path: str,
        profile_id: str,
        design_file: str,
    ) -> str:
        """Generate a validation prompt for testing a design against a profile.

        Reads the specified profile and design document, then returns a prompt
        for you to evaluate the design against the user's criteria and needs.

        Args:
            project_path: Absolute path to the project directory.
            profile_id: The profile to validate against (e.g. "maria-cuidadora").
            design_file: Path to the design document to validate (relative to project).
        """
        try:
            # Load the profile
            profile = prof_get(project_path, profile_id, "json")
            if isinstance(profile, str):
                profile = json.loads(profile)

            # Load the design document
            design_path = Path(project_path) / design_file
            if not design_path.exists():
                return json.dumps({
                    "status": "error",
                    "message": f"Design file not found: {design_file}",
                })

            with open(design_path, "r", encoding="utf-8") as f:
                design_content = f.read()

            criteria = profile.get("criterios_validacion", {})
            mapa = profile.get("mapa_empatia", {})
            dolores = profile.get("dolores", [])
            jtbd = profile.get("jobs_to_be_done", [])
            mentalidad = profile.get("mentalidad", {})

            prompt = render_template("validate", {
                "profile_id": profile_id,
                "profile_name": profile.get("nombre", profile_id),
                "profile_json": json.dumps(profile, indent=2, ensure_ascii=False),
                "design_content": design_content,
                "design_file": design_file,
                "criteria": json.dumps(criteria, indent=2, ensure_ascii=False),
                "pain_points": json.dumps(dolores, indent=2, ensure_ascii=False),
                "jtbd": json.dumps(jtbd, indent=2, ensure_ascii=False),
                "validation_schema": VALIDATION_SCHEMA,
            })

            # Load project-specific template if exists
            custom = load_project_template(project_path, "validate")
            if custom:
                prompt = custom.replace("{{PROFILE_JSON}}", json.dumps(profile, indent=2, ensure_ascii=False))
                prompt = prompt.replace("{{DESIGN_CONTENT}}", design_content)

            return prompt
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def save_validation(
        project_path: str,
        profile_id: str,
        report: str,
    ) -> str:
        """Save a validation report.

        Args:
            project_path: Absolute path to the project directory.
            profile_id: The profile that was validated against.
            report: JSON string with the validation report.
        """
        try:
            data = json.loads(report)
            result = val_save(project_path, profile_id, data)
            return json.dumps({
                "status": "ok",
                "message": f"Validation report saved for '{profile_id}'",
                "files": result,
            }, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return json.dumps({"status": "error", "message": f"Invalid JSON: {str(e)}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def list_validations(project_path: str) -> str:
        """List all validation reports in the project.

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            validations = list_validations(project_path)
            return json.dumps({
                "status": "ok",
                "project_path": project_path,
                "validations": validations,
                "count": len(validations),
            }, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 6. Configuration
# ---------------------------------------------------------------------------

def _register_config(server: FastMCP) -> None:

    @server.tool()
    def get_project_config(project_path: str) -> str:
        """Get the current project configuration.

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            config = get_config(project_path)
            return json.dumps({
                "status": "ok",
                "config": config,
            }, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# 7. Status & Workflow Guide
# ---------------------------------------------------------------------------

def _register_status(server: FastMCP) -> None:

    @server.tool()
    def quick_status(project_path: str) -> str:
        """Get a dashboard overview of the entire project.

        Shows research files count, patterns status, profiles created,
        validations run, and project health. Call this FIRST in any workflow
        to understand the current state.

        Args:
            project_path: Absolute path to the project directory.
        """
        try:
            base = Path(project_path)
            usuarios_dir = base / ".usuarios"

            status = {
                "project": project_path,
                "initialized": usuarios_dir.exists(),
                "research": {"count": 0, "files": []},
                "patterns": {"exists": False, "segments": 0, "patterns": 0},
                "profiles": {"count": 0, "items": []},
                "validations": {"count": 0, "latest": None},
                "health": "healthy",
                "suggestions": [],
            }

            # Research
            research_dir = usuarios_dir / "research"
            if research_dir.exists():
                from internal.project.research import SUPPORTED_EXTENSIONS
                research_files = sorted(
                    [f for f in research_dir.iterdir()
                     if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS and not f.name.startswith(".")]
                )
                status["research"]["count"] = len(research_files)
                status["research"]["files"] = [f.name for f in research_files]

            # Patterns
            patterns_file = usuarios_dir / "patterns" / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file, "r", encoding="utf-8") as f:
                    patterns_data = json.load(f)
                status["patterns"]["exists"] = True
                status["patterns"]["segments"] = len(patterns_data.get("segments", []))
                status["patterns"]["patterns"] = len(patterns_data.get("patterns", []))
                status["patterns"]["pain_points"] = len(patterns_data.get("pain_points", []))

            # Profiles
            profiles_dir = usuarios_dir / "profiles"
            if profiles_dir.exists():
                for json_file in sorted(profiles_dir.glob("*.json")):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        status["profiles"]["items"].append({
                            "id": data.get("id", json_file.stem),
                            "nombre": data.get("nombre", "Unnamed"),
                            "arquetipo": data.get("arquetipo", ""),
                            "trazabilidad": data.get("trazabilidad", {}),
                        })
                    except Exception:
                        pass
                status["profiles"]["count"] = len(status["profiles"]["items"])

            # Validations
            validations_dir = usuarios_dir / "validations"
            if validations_dir.exists():
                val_files = sorted(validations_dir.glob("*.json"), reverse=True)
                status["validations"]["count"] = len(val_files)
                if val_files:
                    try:
                        with open(val_files[0], "r", encoding="utf-8") as f:
                            val_data = json.load(f)
                        status["validations"]["latest"] = {
                            "file": val_files[0].name,
                            "profile": val_data.get("metadata", {}).get("profile_id", "?"),
                            "verdict": val_data.get("verdict", "?"),
                            "date": val_data.get("metadata", {}).get("saved_at", "?"),
                        }
                    except Exception:
                        pass

            # Health & suggestions
            if not status["initialized"]:
                status["health"] = "not_initialized"
                status["suggestions"].append(
                    "🚀 Project not initialized. Say 'inicializá el proyecto' to start."
                )
            elif status["research"]["count"] == 0:
                status["health"] = "needs_research"
                status["suggestions"].append(
                    "📝 No research files yet. Add interviews/notes to .usuarios/research/"
                )
            elif not status["patterns"]["exists"]:
                status["health"] = "ready_to_analyze"
                status["suggestions"].append(
                    f"🔍 {status['research']['count']} research files ready. Say 'analizá la investigación' to extract patterns."
                )
            elif status["profiles"]["count"] == 0:
                status["health"] = "ready_to_generate"
                status["suggestions"].append(
                    "👤 Patterns ready. Say 'generá usuarios sintéticos' to create profiles."
                )
            elif status["validations"]["count"] == 0:
                status["health"] = "ready_to_validate"
                status["suggestions"].append(
                    "✅ Profiles created. Say 'validá el diseño contra <perfil>' to test your design."
                )
            else:
                status["health"] = "active"
                status["suggestions"].append(
                    "🔄 Project active. You can validate more designs or refine existing profiles."
                )

            return json.dumps(status, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @server.tool()
    def get_workflow_guide() -> str:
        """Get the complete workflow guide for using usuarios-mcp.

        Returns detailed instructions on how to use the server effectively:
        autonomous workflows, methodology, and UX principles.

        Call this when you need a refresher on the correct workflow.
        """
        return INSTRUCTIONS

def _patterns_to_markdown(data: dict) -> str:
    """Convert patterns data to human-readable markdown."""
    lines = ["# Research Patterns\n"]
    lines.append(f"**Generated**: {_now()}\n")

    # Meta
    if "meta" in data:
        meta = data["meta"]
        lines.append("## Metadata\n")
        lines.append(f"- Sources analyzed: {meta.get('sources_analyzed', 'N/A')}")
        lines.append(f"- Methods used: {meta.get('methods', 'N/A')}")
        lines.append(f"- Saturation: {meta.get('saturation', 'N/A')}\n")

    # Segments
    if "segments" in data:
        lines.append("## User Segments\n")
        for seg in data["segments"]:
            lines.append(f"### {seg.get('name', 'Unnamed')}")
            lines.append(f"- **Description**: {seg.get('description', '')}")
            lines.append(f"- **Differentiator**: {seg.get('differentiator', '')}")
            if seg.get("size_estimate"):
                lines.append(f"- **Size**: {seg['size_estimate']}")
            lines.append("")

    # Patterns
    if "patterns" in data:
        lines.append("## Behavioral Patterns\n")
        for pat in data["patterns"]:
            lines.append(f"### {pat.get('name', 'Unnamed Pattern')}")
            lines.append(f"- **Evidence strength**: {pat.get('evidence_strength', 'N/A')}")
            lines.append(f"- **Sources**: {', '.join(pat.get('sources', []))}")
            lines.append(f"- **Description**: {pat.get('description', '')}")
            if pat.get("quote"):
                lines.append(f"- **Quote**: _{pat['quote']}_")
            lines.append("")

    # Pain points
    if "pain_points" in data:
        lines.append("## Pain Points\n")
        for pp in data["pain_points"]:
            lines.append(f"- **{pp.get('name', '')}** (intensity: {pp.get('intensity', 'N/A')})")
            lines.append(f"  {pp.get('description', '')}")
            lines.append(f"  Frequency: {pp.get('frequency', 'N/A')}")
            lines.append("")

    # Goals
    if "goals" in data:
        lines.append("## Common Goals\n")
        for goal in data["goals"]:
            lines.append(f"- **{goal.get('name', '')}**")
            lines.append(f"  {goal.get('description', '')}")
            lines.append("")

    return "\n".join(lines)


def _now() -> str:
    """Get current timestamp."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
