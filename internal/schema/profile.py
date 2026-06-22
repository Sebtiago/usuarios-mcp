"""
Schema for synthetic user profiles — the 12-dimension structure.

Based on the service design methodology from:
- "This Is Service Design Doing" (Stickdorn et al.)
- "Mapping Experiences" (Kalbach)
- "Good Services" (Downe)
- Touchpoint Journal — AI in Service Design
"""

PROFILE_SCHEMA = """{
  // ============================================================
  // 1. IDENTITY — Initial empathy
  // ============================================================
  "id": "unique-profile-id",
  "nombre": "Full name",
  "arquetipo": "Memorable archetype name (e.g., 'La Cuidadora Incansable')",
  "cita": "'Direct quote from research, not AI-generated'",
  "fuente_cita": "entrevista-X.md:line",
  "imagen": "assets/profile-image.jpg",

  // Minimal demographics — only what is contextually relevant
  "demografia": {
    "rango_etario": "e.g., 45-55",
    "ubicacion": "e.g., Bogotá, zona urbana",
    "rol_laboral": "e.g., Enfermera jefe de piso",
    "composicion_familiar": "e.g., Vive con su madre de 78 años",
    "nivel_estudios": "e.g., Técnico profesional en enfermería"
  },

  // ============================================================
  // 2. EMPATHY MAP
  // ============================================================
  "mapa_empatia": {
    "que_ve": [
      "What they see in their environment related to the service"
    ],
    "que_oye": [
      "What they hear from others (quotes they report)"
    ],
    "que_piensa_y_siente": [
      "Internal thoughts and emotions (anxieties, pride, hopes)"
    ],
    "que_dice_y_hace": [
      "Observable behaviors and statements"
    ]
  },

  // ============================================================
  // 3. JOBS-TO-BE-DONE
  // ============================================================
  "jobs_to_be_done": [
    {
      "situacion": "When [trigger situation]",
      "motivacion": "I want to [motivation or forces]",
      "resultado": "So I can [expected outcome]",
      "dimension": "functional|emotional|social",
      "traza": "directo|inferido|especulativo",
      "fuente": "entrevista-X.md:line"
    }
  ],

  // ============================================================
  // 4. PAIN POINTS & FRUSTRATIONS
  // ============================================================
  "dolores": [
    {
      "dolor": "Description of the pain",
      "intensidad": "alta|media|baja",
      "frecuencia": "diaria|semanal|por evento",
      "contexto": "When does this occur",
      "traza": "directo|inferido|especulativo",
      "fuente": "entrevista-X.md:line"
    }
  ],

  // ============================================================
  // 5. BEHAVIORS & HABITS
  // ============================================================
  "comportamientos": [
    {
      "patron": "Recurring behavior pattern",
      "disparador": "What triggers this behavior",
      "frecuencia": "How often",
      "traza": "directo|inferido|especulativo",
      "fuente": "shadowing-sesion-X.md:line"
    }
  ],

  // ============================================================
  // 6. MINDSET & BELIEFS
  // ============================================================
  "mentalidad": {
    "creencias_facilitadoras": [
      "Beliefs that help them (e.g., 'My role is to protect the patient')"
    ],
    "creencias_limitantes": [
      "Beliefs that hold them back (e.g., 'Technology always fails')"
    ],
    "actitud_hacia_el_cambio": {
      "nivel": "early adopter|pragmatic|conservative|resistant",
      "condicion_para_adoptar": "What would make them adopt something new"
    },
    "relacion_con_tecnologia": {
      "nivel_alfabetizacion": "beginner|intermediate|advanced|expert",
      "paradigma_interaccion": "Herramienta|Presencia|Entidad",
      "dispositivos_que_usa": ["Device 1", "Device 2"]
    }
  },

  // ============================================================
  // 7. CURRENT ECOSYSTEM & TOOLS
  // ============================================================
  "ecosistema_actual": {
    "herramientas_digitales": [
      {
        "nombre": "Tool name",
        "uso": "How they use it",
        "satisfaccion": "alta|media|baja"
      }
    ],
    "herramientas_fisicas": [
      {
        "nombre": "Physical tool or artifact",
        "uso": "How they use it",
        "satisfaccion": "alta|media|baja"
      }
    ],
    "personas_clave_en_su_red": [
      "Key people in their support network"
    ]
  },

  // ============================================================
  // 8. USAGE SCENARIOS
  // ============================================================
  "escenarios": [
    {
      "nombre": "Scenario name",
      "situacion": "Trigger or context",
      "flujo_actual": [
        "Step 1 of current process",
        "Step 2 of current process"
      ],
      "puntos_friccion": [
        "Friction point 1",
        "Friction point 2"
      ],
      "estado_emocional": "emotional arc (e.g., 'ansiosa → enfocada → frustrada')",
      "tiempo_promedio": "How long this currently takes",
      "traza": "directo|inferido",
      "fuente": "shadowing-sesion-X.md:line"
    }
  ],

  // ============================================================
  // 9. EMOTIONAL JOURNEY
  // ============================================================
  "journey_emocional": {
    "etapas": [
      {
        "etapa": "Stage name",
        "emocion": "Primary emotion",
        "intensidad": 5,
        "descripcion": "What happens in this stage"
      }
    ]
  },

  // ============================================================
  // 10. VALIDATION CRITERIA (Intent Principles)
  // ============================================================
  "criterios_validacion": {
    "principios_intencion": [
      "A good experience for [name] does/doesn't [criterion]"
    ],
    "preguntas_de_validacion": [
      "Can [name] complete [task] in under [time]?",
      "Does [feature] work without [constraint]?"
    ],
    "umbral_exito": {
      "metrica_1": "Target value",
      "metrica_2": "Target value"
    }
  },

  // ============================================================
  // 11. TRACEABILITY & QUALITY
  // ============================================================
  "trazabilidad": {
    "porcentaje_directo": 68,
    "porcentaje_inferido": 25,
    "porcentaje_especulativo": 7,
    "total_fuentes_primarias": 5,
    "fuentes": [
      {
        "id": "source-id",
        "tipo": "Entrevista contextual|Shadowing|Focus group|Encuesta",
        "participante": "Brief description",
        "fecha": "2026-06-10",
        "lineas_referenciadas": [23, 42, 56]
      }
    ],
    "triangulacion": {
      "metodo": "Methods used for cross-validation",
      "estado": "Saturación alcanzada|En progreso|Parcial"
    }
  },

  // ============================================================
  // 12. PROFILE METADATA
  // ============================================================
  "metadata": {
    "version": "1.0.0",
    "fecha_creacion": "2026-06-22",
    "fecha_expiracion": "2027-06-22",
    "fecha_ultima_validacion": "2026-06-22",
    "creado_por": "Equipo de Diseño de Servicios",
    "proyecto": "Project Name",
    "sprint_actual": "Sprint 3",
    "evolucion": [
      {
        "version": "1.0.0",
        "fecha": "2026-06-22",
        "cambios": "Initial creation"
      }
    ],
    "validado_por_humano": false,
    "auditoria_pendiente": true
  }
}"""

# Markdown template for human-readable profile output
PROFILE_MD_TEMPLATE = """# {{nombre}}
### {{arquetipo}}

> {{cita}}
> *— {{fuente_cita}}*

**ID**: `{{id}}`
**Traza**: {{trazabilidad.porcentaje_directo}}% directo, {{trazabilidad.porcentaje_inferido}}% inferido

## Demografía Contextual
- Key: value pairs from demografia

## Mapa de Empatía
[Empathy map sections]

## Jobs-to-be-Done
[JTBD in When/I want/So I can format with traceability]

## Dolores y Frustraciones
[Pain points with intensity and frequency]

## Comportamientos
[Behavior patterns with triggers]

## Mentalidad
[Beliefs, attitude to change, tech literacy]

## Ecosistema Actual
[Current tools and key people]

## Escenarios
[Usage scenarios with emotional states]

## Criterios de Validación
[Intent principles and testable questions]

## Journey Emocional
[Emotional journey table]

## Trazabilidad
[Sources and traceability metrics]

---
**Versión**: {{metadata.version}}
**Expira**: {{metadata.fecha_expiracion}}
"""
