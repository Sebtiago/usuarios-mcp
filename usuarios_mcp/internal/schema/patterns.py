"""
Schema for research analysis patterns.

This is the expected output structure when the AI host processes
the analyze template. It represents the extracted insights from
raw research data.
"""

PATTERNS_SCHEMA = """{
  "meta": {
    "sources_analyzed": 5,
    "methods_used": ["entrevistas contextuales", "shadowing", "focus group"],
    "saturation": "Alta en patrones de coordinación, moderada en uso de tecnología",
    "analysis_date": "2026-06-22",
    "triangulation": "Entrevistas contextuales + shadowing + focus group"
  },
  "segments": [
    {
      "name": "Nombre del segmento",
      "description": "Descripción breve del segmento y su contexto",
      "differentiator": "Qué los distingue de otros segmentos (comportamiento, no demografía)",
      "size_estimate": "Estimado basado en la muestra (ej. 60% de entrevistados)",
      "key_goals": ["Meta principal 1", "Meta principal 2"],
      "key_pains": ["Dolor principal 1", "Dolor principal 2"]
    }
  ],
  "patterns": [
    {
      "name": "Nombre del patrón de comportamiento",
      "description": "Descripción detallada del patrón observado",
      "evidence_strength": "strong|moderate|weak",
      "sources": ["entrevista-1.md", "observacion-2.md"],
      "frequency": "Cómo de frecuente es este patrón en la muestra",
      "quote": "Cita textual que ilustra el patrón (opcional pero recomendado)",
      "quote_source": "entrevista-3.md:45"
    }
  ],
  "pain_points": [
    {
      "name": "Nombre del punto de dolor",
      "description": "Descripción del problema",
      "intensity": "high|medium|low",
      "frequency": "Cómo de frecuentemente ocurre",
      "context": "En qué situación aparece",
      "affected_segments": ["Segmento A", "Segmento B"],
      "sources": ["entrevista-1.md:23", "entrevista-5.md:56"],
      "current_workaround": "Cómo lo resuelven actualmente los usuarios"
    }
  ],
  "goals": [
    {
      "name": "Nombre de la meta",
      "description": "Qué intenta lograr el usuario",
      "dimension": "functional|emotional|social",
      "evidence_strength": "strong|moderate|weak",
      "affected_segments": ["Segmento A"],
      "sources": ["entrevista-2.md:89"],
      "jtbd_format": "Cuando [situación], quiero [motivación], para [resultado]"
    }
  ],
  "contradictions": [
    {
      "description": "Contradicción encontrada (ej. 'dicen que quieren X pero hacen Y')",
      "sources": ["entrevista-1.md:45 vs observacion-1.md:12"]
    }
  ],
  "gaps": [
    {
      "description": "Vacío de información identificado, necesita más investigación",
      "suggested_method": "Método sugerido para cerrar este vacío"
    }
  ]
}"""

# Human-readable description of the pattern fields
PATTERNS_FIELDS = """
Each pattern should include:
- name: Short, descriptive label (e.g., "Bypass del sistema oficial")
- description: What users actually do, in their context
- evidence_strength: strong (3+ sources), moderate (2 sources), weak (1 source or inferido)
- sources: List of filenames where this pattern was observed
- frequency: How often this occurs (e.g., "diario", "cada cambio de turno", "80% de entrevistados")
- quote: (optional) A direct quote that illustrates the pattern
- quote_source: Where the quote came from

Each pain point should include:
- name: Short label
- description: The problem in the user's own context
- intensity: high (blocks the task), medium (slows it down), low (annoying but manageable)
- frequency: How often it occurs
- context: When/where it happens
- affected_segments: Which user segments experience this
- sources: Traceability (filename:line or context)
- current_workaround: How users cope today
"""
