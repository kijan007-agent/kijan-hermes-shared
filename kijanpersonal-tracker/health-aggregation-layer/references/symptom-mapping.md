# Symptom Mapping — Bearable → Kijan Categories

## Standard Mapping

| Bearable Category | Kijan Category | Notes |
|------------------|----------------|-------|
| Symptoms: Pain | pain | Direct mapping |
| Symptoms: Fatigue | fatigue | Direct mapping |
| Symptoms: Cognitive | cognitive | Direct mapping |
| Symptoms: Mood | mood | Direct mapping |
| Symptoms: Sleep | sleep | Direct mapping |
| Symptoms: Gastrointestinal | gastro | Direct mapping |
| Symptoms: Neurological | neuro | Direct mapping |
| Mood | mood | Mood entries → mood_logs |
| Factors | factor | Factors → factor_definitions/logs |
| Health | health_measurement | Health metrics → health_measurements |
| Medications | medication | Meds → medication_logs |
| Supplements | medication | Supplements → medication_logs |

## Fuzzy Matching for Unknown Symptoms

When Bearable symptom name doesn't match any Kijan definition:

1. **Exact match:** `symptom_def.name == bearable_name` (case-insensitive)
2. **i18n match:** `symptom_def.name_de == bearable_name` or `symptom_def.name_en == bearable_name`
3. **Category fallback:** If no match but category is known, suggest user confirm mapping
4. **Create new:** If user confirms, create new SymptomDefinition with category from Bearable

## Mapping Rules

- **Symptom name is user-defined** → always preserve original Bearable name in `name` column
- **Category comes from Bearable category** → map to Kijan category using table above
- **Bearable detail field** → stored in `notes` column
- **Severity 0 (none)** → stored as severity=0, severity_label="none"
- **i18n keys** → generated for new definitions: `symptom.{created_name_de}` + `symptom.{created_name_en}`