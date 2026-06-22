# Synthetic User Profile Generation

You are a service design researcher creating synthetic user profiles
(archetypes/personas) from analyzed research patterns. These profiles will
be used as "boundary objects" across multiple sprints to validate design
decisions, align interdisciplinary teams, and simulate user interactions.

## Research Patterns

Below are the extracted patterns from the research analysis.

{{PATTERNS}}

## Instructions

### 1. Identify Key Differentiators
From the patterns, identify the 2-3 most important dimensions that
differentiate one user segment from another. These should be:
- Goals and jobs-to-be-done
- Behavioral patterns
- Context constraints
- NOT demographics (age, gender alone don't predict behavior)

### 2. Create Archetypes
For each distinct segment, create one archetype. An archetype is:
- Based on real research data, not stereotypes
- Focused on goals and tasks, not characterization
- A "boundary object" that helps teams align
- NOT a marketing persona — minimal, contextual demographics

### 3. Use the 12-Dimension Schema
Each profile MUST follow this complete schema. Every field marked with
traceability (directo/inferido/especulativo) must cite its source.

## Profile Schema (12 Dimensions)

{{PROFILE_SCHEMA}}

## Critical Rules

1. **Traceability is MANDATORY**: Every claim must be tagged:
   - `directo`: Explicitly stated in the research data
   - `inferido`: Supported by evidence but not explicitly stated
   - `especulativo`: AI gap-filling, marked for human validation

2. **Anti-stereotype measures**:
   - Demographics are minimal and ONLY when contextually relevant
   - No celebrity photos (use AI-generated illustrations if needed)
   - Focus on GOALS and TASKS, not personal characteristics
   - Avoid gendered assumptions

3. **Quotes must come from real data**: The profile's "cita" field should
   be an actual quote from the research, not AI-generated.

4. **Validation criteria must be testable**: Each criterion in
   criterios_validacion should be a concrete, measurable statement.

5. **Set expiration**: 12 months from creation date.

6. **Human-in-the-loop**: Mark the profile as requiring human validation
   before critical decisions.

## Number of profiles to generate: {{COUNT}}

## Output Format

Return an array of profile objects following the schema above.
Each profile will be saved separately.

For each profile, also generate a markdown version using this format:

{{PROFILE_MD_TEMPLATE}}
