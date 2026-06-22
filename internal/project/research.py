"""
Research file management.

Handles reading and listing research files (.md, .txt) from the
project's .usuarios/research/ directory.
"""

from pathlib import Path
from typing import Optional

USUARIOS_DIR = ".usuarios"
RESEARCH_DIR = "research"
SUPPORTED_EXTENSIONS = {".md", ".txt", ".json", ".csv"}


def _research_path(project_path: str) -> Path:
    """Get the research directory path."""
    path = Path(project_path) / USUARIOS_DIR / RESEARCH_DIR
    if not path.exists():
        raise FileNotFoundError(
            f"Research directory not found at {path}. "
            f"Run init_project first."
        )
    return path


def list_research_files(project_path: str) -> list[dict]:
    """List all research files with metadata."""
    research_dir = _research_path(project_path)
    files = []

    for file_path in sorted(research_dir.iterdir()):
        if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
            stat = file_path.stat()
            files.append({
                "filename": file_path.name,
                "path": str(file_path),
                "size_bytes": stat.st_size,
                "extension": file_path.suffix,
                "modified": _format_timestamp(stat.st_mtime),
            })

    return files


def read_research_files(
    project_path: str,
    source_files: Optional[list[str]] = None,
    max_chars_per_file: int = 100000,
) -> list[dict]:
    """Read research files and return their content.

    Args:
        project_path: Project path.
        source_files: Optional list of filenames to read. None = all.
        max_chars_per_file: Maximum characters to read per file.
    """
    research_dir = _research_path(project_path)
    results = []

    all_files = list(research_dir.iterdir())
    if source_files:
        # Filter to specified files
        all_files = [f for f in all_files if f.name in source_files]

    for file_path in sorted(all_files):
        if not file_path.is_file():
            continue
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue
        if file_path.name.startswith("."):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(max_chars_per_file)

            results.append({
                "filename": file_path.name,
                "path": str(file_path),
                "content": content,
                "char_count": len(content),
                "extension": file_path.suffix,
            })
        except UnicodeDecodeError:
            results.append({
                "filename": file_path.name,
                "path": str(file_path),
                "content": f"[Binary file — cannot read as text]",
                "char_count": 0,
                "extension": file_path.suffix,
            })

    return results


def _format_timestamp(ts: float) -> str:
    """Format a file timestamp."""
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
