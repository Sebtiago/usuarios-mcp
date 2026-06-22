"""
Project configuration management.

Handles .usuarios/config.yaml — project-level settings that control
the behavior of the usuarios-mcp server.
"""

from pathlib import Path
from datetime import datetime, timezone
import yaml
import os

DEFAULT_CONFIG = {
    "project": {
        "name": "",
        "created_at": "",
        "updated_at": "",
    },
    "templates": {
        "override_dir": None,  # Path to custom templates, None = use defaults
    },
    "metadata": {
        "version": "0.1.0",
    },
}

USUARIOS_DIR = ".usuarios"
CONFIG_FILE = "config.yaml"


def _usuarios_path(project_path: str) -> Path:
    """Get the .usuarios directory path."""
    return Path(project_path) / USUARIOS_DIR


def _ensure_usuarios(project_path: str) -> Path:
    """Ensure .usuarios directory exists, return its path."""
    path = _usuarios_path(project_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Project not initialized at {project_path}. "
            f"Run init_project first."
        )
    return path


def init_project(project_path: str) -> dict:
    """Initialize a usuarios project structure.

    Creates:
        .usuarios/
        .usuarios/config.yaml
        .usuarios/research/
        .usuarios/patterns/
        .usuarios/profiles/
        .usuarios/validations/
    """
    base = Path(project_path)
    usuarios = base / USUARIOS_DIR

    if usuarios.exists():
        # Already initialized — update timestamps
        config = get_config(project_path)
        config["metadata"]["updated_at"] = _now()
        _write_config(project_path, config)
        return {
            "path": str(usuarios),
            "structure": _describe_structure(usuarios),
            "message": "Project already initialized, config updated.",
        }

    # Create directory structure
    dirs = [
        usuarios,
        usuarios / "research",
        usuarios / "patterns",
        usuarios / "profiles",
        usuarios / "validations",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create default config
    config = DEFAULT_CONFIG.copy()
    config["project"]["name"] = base.name
    config["project"]["created_at"] = _now()
    config["project"]["updated_at"] = _now()
    _write_config(project_path, config)

    # Create placeholder files
    (usuarios / "research" / ".gitkeep").touch()
    (usuarios / "patterns" / ".gitkeep").touch()
    (usuarios / "profiles" / ".gitkeep").touch()
    (usuarios / "validations" / ".gitkeep").touch()

    return {
        "path": str(usuarios),
        "structure": _describe_structure(usuarios),
    }


def get_config(project_path: str) -> dict:
    """Read the project configuration."""
    usuarios = _ensure_usuarios(project_path)
    config_path = usuarios / CONFIG_FILE
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or DEFAULT_CONFIG.copy()


def set_config(project_path: str, config: dict) -> None:
    """Write the project configuration."""
    _write_config(project_path, config)


def _write_config(project_path: str, config: dict) -> None:
    """Write config to disk."""
    usuarios = _usuarios_path(project_path)
    usuarios.mkdir(parents=True, exist_ok=True)
    config_path = usuarios / CONFIG_FILE
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def _describe_structure(usuarios: Path) -> dict:
    """Return a description of the project structure."""
    return {
        "config": str(usuarios / "config.yaml"),
        "research": str(usuarios / "research") + "/",
        "patterns": str(usuarios / "patterns") + "/",
        "profiles": str(usuarios / "profiles") + "/",
        "validations": str(usuarios / "validations") + "/",
    }


def _now() -> str:
    """Get current timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
