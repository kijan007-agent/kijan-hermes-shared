# Kijan Frontend — Spezifikationsreferenz

**Referenz für:** HAL-API-Integration, Mobile/Web-Entwicklung, Design-Tokens

---

## 1. Verfügbare Spezifikationen

Alle in `kpt-doc/_specs/kijan-frontend/`:

| Datei | Inhalt |
|-------|--------|
| `001-system-overview.md` | Systemarchitektur, Flutter-Auswahl, Tech Stack, Design-Ziele, Bearable Feature Map |
| `DESIGN.md` | Google Design System: Farben, Typografie, Layout, Components, WCAG 2.1 AA |
| `001-mobile-app-spec.md` | Flutter App Structure, Screen-Flows, Pain Scale, Envelope, HealthSync, Offline-First |
| `001-web-dashboard-spec.md` | React Dashboard Layout, Analytics, Report Builder, Pain Heatmap, Responsive Design |
| `002-implementation-plan.md` | 6 Phasen, 6 Meilensteine, Shared Code Matrix, API-Usage-Matrix, Test-Konzept |
| `003-morning-briefing.md` | Facts, RCA, Mockups für Morgenbriefing |
| `004-architectural-decisions.md` | 7 ADRs (Flutter, Next.js, State, Pain, Offline, i18n, Health) |

## 2. Frontend ↔ HAL API Mapping

### Shared Code (80-90%)
- **Data Models** → TypeScript-Definitionen + Python Pydantic
- **i18n Messages** → Shared JSON-Dateien (DE, EN, FR, ES, IT)
- **DESIGN.md Tokens** → Flutter Theme + Tailwind Config
- **Bearable Mapping** → Shared Mapping-Tables

### Mobile (Flutter)
| API-Endpoint | Flutter Service | Platform-Code |
|-------------|----------------|---------------|
| `/symptoms` | SymptomApiService | — |
| `/symptoms/{id}/logs` | SymptomApiService | — |
| `/factors` | FactorApiService | — |
| `/factors/{id}/logs` | FactorApiService | — |
| `/daily-logs` | DailyLogApiService | — |
| `/health-metrics` | HealthMetricApiService | HealthKit/HealthConnect |
| `/aggregations` | AggregationApiService | (read-only) |
| `/reports/generate` | ReportApiService | — |
| `/reports/{id}` | ReportApiService | (read-only) |
| `/import/bearable/csv` | ImportApiService | — |
| `/import/bearable/batch` | ImportApiService | — |
| `/health/config` | ConfigApiService | — |
| `/health/config/pacing` | ConfigApiService | — |
| `/health/pain/scale` | ConfigApiService | — |

**PITFALL:** `/trends/calculate` und `/correlations/compute` sind NUR Web — nicht auf Mobile verfügbar.

### Web (React/Next.js)
| Feature | API-Endpunkt | Komponente |
|---------|-------------|-----------|
| Pain Heatmap | `/symptoms/{id}/logs` | PainHeatmap |
| Trends | `/trends/calculate` | TrendChart |
| Korrelationen | `/correlations/compute` | CorrelationMatrix |
| Report Builder | `/reports/generate` + `/reports/{id}` | ReportBuilder |
| Report Viewer | `/reports/{id}` | ReportViewer |
| Bearable Import | `/import/bearable/csv` | ImportUploader |

## 3. Pain Scale (Shared Color System)

| Score | Hex | Mobile (Flutter) | Web (Tailwind) |
|-------|-----|-----------------|----------------|
| 0 | transparent | `Colors.transparent` | `bg-transparent` |
| 1-3 | #FFD93D | `Color(0xFFFFD93D)` | `bg-yellow-300` |
| 4-6 | #FFA07A | `Color(0xFFFFA07A)` | `bg-orange-300` |
| 7-9 | #FF6B6B | `Color(0xFFFF6B6B)` | `bg-red-400` |
| 10 | #C62828 | `Color(0xFFC62828)` | `bg-red-800` |

**PITFALL:** Immer warmes Farbspektrum verwenden — niemals Rot/Grün für Schmerzskala (Farbblindheit).

## 4. i18n Messages (Shared JSON)

```json
{
  "dashboard": { "title": "Dashboard", "energy": "Energie", "pain": "Schmerz", "sleep": "Schlaf", "pacing": "Pacing" },
  "symptoms": { "title": "Symptome", "add": "Symptom hinzufügen", "severity": "Intensität" },
  "reports": { "title": "Berichte", "statistical": "Statistischer Bericht", "ai_report": "KI-Bericht", "weekly": "Wöchentlicher Bericht", "monthly": "Monatlicher Bericht" },
  "severity": { "0": "Keine", "1-3": "Leicht", "4-6": "Mäßig", "7-9": "Stark", "10": "Extrem" },
  "trend": { "improving": "Verbesserung", "worsening": "Verschlechterung", "stable": "Stabil" }
}
```

## 5. Test-Konzept

| Test-Typ | Mobile (Flutter) | Web (React) |
|----------|-----------------|-------------|
| Unit | flutter_test (Models, Services) | Vitest (Components, Utils) |
| Widget | flutter_test | RTL |
| Integration | integration_test | Supertest (API) |
| E2E | flutter_driver | Cypress |

**PITFALL:** HealthSync (HealthKit/Health Connect) nur auf physischen Geräten testbar — nicht in Simulatoren/Emulatoren.
