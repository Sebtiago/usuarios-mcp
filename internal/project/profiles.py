"""
Profile and validation file management.

Handles saving and loading synthetic user profiles (JSON + Markdown)
and validation reports from the project's .usuarios/ directory.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

USUARIOS_DIR = ".usuarios"
PROFILES_DIR = "profiles"
VALIDATIONS_DIR = "validations"


def _profiles_path(project_path: str) -> Path:
    """Get the profiles directory path."""
    path = Path(project_path) / USUARIOS_DIR / PROFILES_DIR
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path


def _validations_path(project_path: str) -> Path:
    """Get the validations directory path."""
    path = Path(project_path) / USUARIOS_DIR / VALIDATIONS_DIR
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path


def save_profile(project_path: str, profile_id: str, data: dict) -> dict:
    """Save a synthetic user profile as JSON and Markdown.

    Args:
        project_path: Project root path.
        profile_id: Unique profile identifier.
        data: Profile data dict following the 12-dimension schema.

    Returns:
        Dict with paths to saved files.
    """
    profiles = _profiles_path(project_path)

    # Add/update metadata
    if "metadata" not in data:
        data["metadata"] = {}
    data["metadata"]["updated_at"] = _now()

    # Save JSON
    json_path = profiles / f"{profile_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Generate and save Markdown
    md_content = _profile_to_markdown(data)
    md_path = profiles / f"{profile_id}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return {
        "json": str(json_path),
        "markdown": str(md_path),
    }


def list_profiles(project_path: str) -> list[dict]:
    """List all saved profiles with summaries."""
    profiles_dir = _profiles_path(project_path)
    results = []

    for json_file in sorted(profiles_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            results.append({
                "id": data.get("id", json_file.stem),
                "nombre": data.get("nombre", "Unnamed"),
                "arquetipo": data.get("arquetipo", ""),
                "cita": data.get("cita", ""),
                "trazabilidad": data.get("trazabilidad", {}),
                "metadata": data.get("metadata", {}),
                "file": str(json_file),
            })
        except (json.JSONDecodeError, KeyError):
            results.append({
                "id": json_file.stem,
                "nombre": "[Error reading profile]",
                "arquetipo": "",
                "cita": "",
                "file": str(json_file),
            })

    return results


def get_profile(
    project_path: str,
    profile_id: str,
    format: str = "json",
) -> str | dict:
    """Get a profile by ID.

    Args:
        project_path: Project root path.
        profile_id: Profile identifier.
        format: "json" for structured, "markdown" for human-readable.

    Returns:
        Profile data as dict (json format) or markdown string.
    """
    profiles_dir = _profiles_path(project_path)
    json_path = profiles_dir / f"{profile_id}.json"

    if not json_path.exists():
        raise FileNotFoundError(f"Profile '{profile_id}' not found")

    if format == "markdown":
        md_path = profiles_dir / f"{profile_id}.md"
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                return f.read()
        # Generate markdown from JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _profile_to_markdown(data)

    # Default: return JSON dict
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_validation(
    project_path: str,
    profile_id: str,
    report: dict,
) -> dict:
    """Save a validation report.

    Args:
        project_path: Project root path.
        profile_id: The profile that was validated.
        report: Validation report dict.

    Returns:
        Dict with paths to saved files.
    """
    validations = _validations_path(project_path)
    timestamp = _now().replace(":", "-").replace("T", "-")[:19]
    file_id = f"{timestamp}-{profile_id}"

    if "metadata" not in report:
        report["metadata"] = {}
    report["metadata"]["saved_at"] = _now()
    report["metadata"]["profile_id"] = profile_id

    json_path = validations / f"{file_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    md_path = validations / f"{file_id}.md"
    md_content = _validation_to_markdown(report)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return {"json": str(json_path), "markdown": str(md_path)}


def list_validations(project_path: str) -> list[dict]:
    """List all validation reports."""
    validations_dir = _validations_path(project_path)
    results = []

    for json_file in sorted(validations_dir.glob("*.json"), reverse=True):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            results.append({
                "file_id": json_file.stem,
                "profile_id": data.get("metadata", {}).get("profile_id", "unknown"),
                "type": data.get("type", "validation"),
                "verdict": data.get("verdict", "unknown"),
                "saved_at": data.get("metadata", {}).get("saved_at", ""),
                "file": str(json_file),
            })
        except (json.JSONDecodeError, KeyError):
            pass

    return results


def get_validation(project_path: str, file_id: str) -> dict:
    """Get a specific validation report."""
    validations_dir = _validations_path(project_path)
    json_path = validations_dir / f"{file_id}.json"

    if not json_path.exists():
        raise FileNotFoundError(f"Validation '{file_id}' not found")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _profile_to_markdown(data: dict) -> str:
    """Convert a profile dict to rich Markdown."""
    p = data
    lines = []

    # Header
    nombre = p.get("nombre", p.get("id", "Unnamed"))
    arquetipo = p.get("arquetipo", "")
    lines.append(f"# {nombre}")
    if arquetipo:
        lines.append(f"### {arquetipo}")
    lines.append("")

    # Quote
    cita = p.get("cita", "")
    if cita:
        lines.append(f"> {cita}")
        fuente = p.get("fuente_cita", "")
        if fuente:
            lines.append(f"> *— {fuente}*")
        lines.append("")

    # ID and traceability
    lines.append(f"**ID**: `{p.get('id', 'N/A')}`")
    traz = p.get("trazabilidad", {})
    if traz:
        lines.append(f"**Trazabilidad**: {traz.get('porcentaje_directo', '?')}% directo, "
                     f"{traz.get('porcentaje_inferido', '?')}% inferido, "
                     f"{traz.get('porcentaje_especulativo', '?')}% especulativo")
    lines.append("")

    # Demografía
    dem = p.get("demografia", {})
    if dem:
        lines.append("## 📋 Demografía Contextual")
        lines.append("")
        for key, value in dem.items():
            label = key.replace("_", " ").title()
            lines.append(f"- **{label}**: {value}")
        lines.append("")

    # Mapa de empatía
    mapa = p.get("mapa_empatia", {})
    if mapa:
        lines.append("## 🧠 Mapa de Empatía")
        lines.append("")

        que_ve = mapa.get("que_ve", [])
        if que_ve:
            lines.append("### 👁️ ¿Qué ve?")
            for item in que_ve:
                lines.append(f"- {item}")
            lines.append("")

        que_oye = mapa.get("que_oye", [])
        if que_oye:
            lines.append("### 👂 ¿Qué oye?")
            for item in que_oye:
                lines.append(f"- {item}")
            lines.append("")

        que_piensa = mapa.get("que_piensa_y_siente", [])
        if que_piensa:
            lines.append("### 💭 ¿Qué piensa y siente?")
            for item in que_piensa:
                lines.append(f"- {item}")
            lines.append("")

        que_hace = mapa.get("que_dice_y_hace", [])
        if que_hace:
            lines.append("### 🗣️ ¿Qué dice y hace?")
            for item in que_hace:
                lines.append(f"- {item}")
            lines.append("")

    # Jobs-to-be-done
    jtbd = p.get("jobs_to_be_done", [])
    if jtbd:
        lines.append("## 🎯 Jobs-to-be-Done")
        lines.append("")
        for i, job in enumerate(jtbd, 1):
            lines.append(f"### Job {i}: {job.get('dimension', 'funcional').title()}")
            lines.append(f"**Situación**: {job.get('situacion', '')}")
            lines.append(f"**Motivación**: {job.get('motivacion', '')}")
            lines.append(f"**Resultado esperado**: {job.get('resultado', '')}")
            if job.get("traza"):
                lines.append(f"_{job['traza']}_ — {job.get('fuente', 'N/A')}")
            lines.append("")

    # Dolores
    dolores = p.get("dolores", [])
    if dolores:
        lines.append("## 😣 Dolores y Frustraciones")
        lines.append("")
        for dolor in dolores:
            lines.append(f"- **{dolor.get('dolor', '')}**")
            lines.append(f"  Intensidad: {dolor.get('intensidad', 'N/A')} | "
                         f"Frecuencia: {dolor.get('frecuencia', 'N/A')}")
            lines.append(f"  Contexto: {dolor.get('contexto', '')}")
            if dolor.get("traza"):
                lines.append(f"  _{dolor['traza']}_ — {dolor.get('fuente', 'N/A')}")
            lines.append("")

    # Comportamientos
    comps = p.get("comportamientos", [])
    if comps:
        lines.append("## 🔄 Comportamientos y Hábitos")
        lines.append("")
        for comp in comps:
            lines.append(f"- **{comp.get('patron', '')}**")
            lines.append(f"  Disparador: {comp.get('disparador', '')} | "
                         f"Frecuencia: {comp.get('frecuencia', '')}")
            if comp.get("traza"):
                lines.append(f"  _{comp['traza']}_ — {comp.get('fuente', 'N/A')}")
            lines.append("")

    # Mentalidad
    ment = p.get("mentalidad", {})
    if ment:
        lines.append("## 💡 Mentalidad y Creencias")
        lines.append("")
        if ment.get("creencias_facilitadoras"):
            lines.append("### Creencias que facilitan")
            for c in ment["creencias_facilitadoras"]:
                lines.append(f"- {c}")
            lines.append("")
        if ment.get("creencias_limitantes"):
            lines.append("### Creencias que limitan")
            for c in ment["creencias_limitantes"]:
                lines.append(f"- {c}")
            lines.append("")
        if ment.get("relacion_con_tecnologia"):
            tech = ment["relacion_con_tecnologia"]
            lines.append(f"- **Alfabetización digital**: {tech.get('nivel_alfabetizacion', 'N/A')}")
            lines.append(f"- **Paradigma de interacción**: {tech.get('paradigma_interaccion', 'N/A')}")
            lines.append("")

    # Escenarios
    escenarios = p.get("escenarios", [])
    if escenarios:
        lines.append("## 🎬 Escenarios de Uso")
        lines.append("")
        for esc in escenarios:
            lines.append(f"### {esc.get('nombre', 'Escenario')}")
            lines.append(f"**Situación**: {esc.get('situacion', '')}")
            if esc.get("tiempo_promedio"):
                lines.append(f"**Tiempo promedio**: {esc['tiempo_promedio']}")
            if esc.get("estado_emocional"):
                lines.append(f"**Estado emocional**: {esc['estado_emocional']}")
            lines.append("")

    # Journey emocional
    journey = p.get("journey_emocional", {})
    if journey:
        lines.append("## 📈 Journey Emocional")
        lines.append("")
        lines.append("| Etapa | Emoción | Intensidad |")
        lines.append("|-------|---------|------------|")
        for etapa in journey.get("etapas", []):
            lines.append(f"| {etapa.get('etapa', '')} | {etapa.get('emocion', '')} | {'⭐' * etapa.get('intensidad', 1)} |")
        lines.append("")

    # Criterios de validación
    crit = p.get("criterios_validacion", {})
    if crit:
        lines.append("## ✅ Criterios de Validación")
        lines.append("")
        principios = crit.get("principios_intencion", [])
        if principios:
            lines.append("### Principios de intención")
            for pr in principios:
                lines.append(f"- {pr}")
            lines.append("")
        preguntas = crit.get("preguntas_de_validacion", [])
        if preguntas:
            lines.append("### Preguntas de validación")
            for pq in preguntas:
                lines.append(f"- {pq}")
            lines.append("")

    # Ecosystem
    eco = p.get("ecosistema_actual", {})
    if eco:
        lines.append("## 🔧 Ecosistema Actual")
        lines.append("")
        tools = eco.get("herramientas_digitales", [])
        if tools:
            lines.append("### Herramientas digitales")
            for t in tools:
                lines.append(f"- **{t.get('nombre', '')}**: {t.get('uso', '')} (Satisfacción: {t.get('satisfaccion', 'N/A')})")
            lines.append("")

    # Metadata
    meta = p.get("metadata", {})
    if meta:
        lines.append("---")
        lines.append("")
        lines.append(f"**Versión**: {meta.get('version', 'N/A')}")
        lines.append(f"**Creado**: {meta.get('fecha_creacion', 'N/A')}")
        lines.append(f"**Expira**: {meta.get('fecha_expiracion', 'N/A')}")
        if meta.get("validado_por_humano"):
            lines.append("**✅ Validado por humano**")
        lines.append("")

    return "\n".join(lines)


def _validation_to_markdown(report: dict) -> str:
    """Convert validation report to markdown."""
    lines = []
    lines.append(f"# Validation Report")
    lines.append(f"**Profile**: {report.get('metadata', {}).get('profile_id', 'N/A')}")
    lines.append(f"**Saved**: {report.get('metadata', {}).get('saved_at', 'N/A')}")
    lines.append("")

    verdict = report.get("verdict", "unknown")
    emoji = {"approved": "✅", "needs_work": "⚠️", "rejected": "❌"}.get(verdict, "❓")
    lines.append(f"## Verdict: {emoji} {verdict}")
    lines.append("")

    summary = report.get("summary", "")
    if summary:
        lines.append(summary)
        lines.append("")

    findings = report.get("findings", [])
    if findings:
        lines.append("## Findings")
        lines.append("")
        for f in findings:
            severity = f.get("severity", "info").upper()
            lines.append(f"- **[{severity}]** {f.get('finding', '')}")
            lines.append(f"  Criterion: {f.get('criterion', 'N/A')}")
            suggestion = f.get("suggestion", "")
            if suggestion:
                lines.append(f"  Suggestion: {suggestion}")
            lines.append("")

    next_steps = report.get("next_steps", [])
    if next_steps:
        lines.append("## Next Steps")
        for step in next_steps:
            lines.append(f"- {step}")
        lines.append("")

    return "\n".join(lines)


def _now() -> str:
    """Get current timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
