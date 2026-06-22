"""
Schema for design validation reports.

This is the expected output structure when validating a design
against a synthetic user profile.
"""

VALIDATION_SCHEMA = """{
  "type": "design_validation",
  "verdict": "approved|needs_work|rejected",
  "summary": "1-2 paragraph executive summary of the validation",
  "score": {
    "total_criteria": 10,
    "passed": 6,
    "partial": 3,
    "failed": 1,
    "not_applicable": 0
  },
  "findings": [
    {
      "criterion": "The specific criterion being evaluated",
      "criterion_source": "principio_intencion|pregunta_validacion|umbral_exito",
      "finding": "What was found when evaluating against this criterion",
      "severity": "critical|major|minor|positive",
      "rating": "STRONG|ADEQUATE|WEAK|MISSING|CONFLICT",
      "evidence": "Specific reference to the design document",
      "user_impact": "How this affects the user's ability to achieve their goal",
      "suggestion": "Concrete, actionable suggestion for improvement"
    }
  ],
  "emotional_impact": {
    "positive_triggers": [
      "Aspects of the design that would create positive emotions"
    ],
    "negative_triggers": [
      "Aspects that would trigger frustration, anxiety, or confusion"
    ],
    "overall_emotional_arc": "Description of the likely emotional journey"
  },
  "risk_assessment": {
    "high_risks": [
      {
        "risk": "Description of the risk",
        "likelihood": "high|medium|low",
        "impact": "high|medium|low",
        "mitigation": "Suggested mitigation"
      }
    ],
    "medium_risks": [],
    "opportunities": [
      "Unexpected positive opportunities found in the design"
    ]
  },
  "next_steps": [
    "Actionable next step 1",
    "Actionable next step 2"
  ],
  "metadata": {
    "profile_id": "profile-id",
    "design_file": "path/to/design.md",
    "saved_at": "ISO timestamp"
  }
}"""

VALIDATION_FIELDS = """
For each finding:
- criterion: Reference the exact criterion from the user's profile
- rating: STRONG (fully meets), ADEQUATE (mostly meets), WEAK (barely meets),
  MISSING (not addressed), CONFLICT (works against the user)
- evidence: Cite specific parts of the design document
- user_impact: Frame it from the user's perspective, not the system's
- suggestion: Be CONCRETE and ACTIONABLE. "Add voice note option for step 3"
  vs "improve accessibility"

Severity levels:
- critical: Blocks a core job-to-be-done or violates a safety principle
- major: Significantly degrades the experience
- minor: Annoying but manageable
- positive: Something the design does well that should be preserved
"""
