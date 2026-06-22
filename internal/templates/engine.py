"""
Template engine for prompt generation.

Renders templates with project data. Default templates are embedded
in memory. Projects can override them by placing custom .md templates
in .usuarios/templates/ (e.g., analyze.md, generate.md, validate.md).

The template format uses simple {{KEY}} placeholders, compatible
with Python's str.format().
"""

from pathlib import Path
from typing import Optional
import os

# Template directory inside project's .usuarios/
TEMPLATE_DIR = "templates"

# Default template files
_TEMPLATES: dict[str, str] = {}


def _get_default_templates() -> dict[str, str]:
    """Load default templates from the templates/ directory."""
    global _TEMPLATES
    if _TEMPLATES:
        return _TEMPLATES

    # Try to load from filesystem first (development)
    template_dir = Path(__file__).parent.parent.parent / "templates"

    for name in ["analyze", "generate", "validate"]:
        tmpl_path = template_dir / f"{name}.md"
        if tmpl_path.exists():
            with open(tmpl_path, "r", encoding="utf-8") as f:
                _TEMPLATES[name] = f.read()

    # Fall back to embedded defaults
    from internal.templates.defaults import DEFAULT_TEMPLATES
    for name, content in DEFAULT_TEMPLATES.items():
        if name not in _TEMPLATES:
            _TEMPLATES[name] = content

    return _TEMPLATES


def render_template(name: str, variables: dict) -> str:
    """Render a template with the given variables.

    Args:
        name: Template name (e.g., "analyze", "generate", "validate").
        variables: Dictionary of variables to interpolate.

    Returns:
        The rendered template string.

    Template syntax: {{VARIABLE_NAME}} is replaced with the variable value.
    Variables can be any string. For complex data, pass JSON-encoded strings.
    """
    templates = _get_default_templates()
    template = templates.get(name)
    if not template:
        raise ValueError(f"Template '{name}' not found. Available: {list(templates.keys())}")

    # Simple template rendering: replace {{KEY}} with value
    result = template
    for key, value in variables.items():
        placeholder = "{{" + key.upper() + "}}"
        result = result.replace(placeholder, str(value))

    return result


def load_project_template(project_path: str, name: str) -> Optional[str]:
    """Load a project-specific template override.

    Args:
        project_path: Project root path.
        name: Template name (e.g., "analyze").

    Returns:
        Template content string, or None if no override exists.
    """
    tmpl_dir = Path(project_path) / ".usuarios" / TEMPLATE_DIR
    tmpl_path = tmpl_dir / f"{name}.md"

    if tmpl_path.exists():
        with open(tmpl_path, "r", encoding="utf-8") as f:
            return f.read()

    return None
