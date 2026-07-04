# Multi-Perspektive Checkliste für Kijan Tasks

## Kontext
Jede Task muss durch folgende Perspektiven gefiltert werden — NICHT optional.

## Perspektiven

### 1. Patient / Nutzer
- Ist die Bedienung klar und intuitiv?
- Werden Fehler verständlich kommuniziert?
- Ist die App ohne medizinische Vorkenntnisse bedienbar?
- Feedback-Schleifen (Bestätigung, Loading, Error) vorhanden?
- Pacing-Werte verständlich dargestellt? (Spoon-Icons, Farben)

### 2. Arzt / Kliniker
- Sind Daten klinisch relevant und interpretierbar?
- Sind Trends/Verläufe nachvollziehbar?
- Alarm-/Warnwerte klar visualisiert?
- Datengenauigkeit für medizinische Entscheidungen ausreichend?
- GDPR/DSGVO-konforme Datenverarbeitung?

### 3. UI/UX Designer
- Konsistente Navigation in App UND Dashboard?
- Gleiche Terminologie in App und Dashboard?
- Gleiche Hierarchie-Tiefe?
- Visuelle Konsistenz (Farben, Icons, Layout-Patterns)?
- Spoon-Levels: >=20 green, >=10 yellow, <10 red — konsistent?
- Touch-Targets auf Garmin-Display ausreichend groß?

### 4. Data-Spezialist (medizinische Daten)
- Ist die Datenmodellierung klinisch valide?
- Partitionierung nach medizinischen Kriterien?
- Datenqualität und -integrität gesichert?
- Nullable-Spalten (134x) gerechtfertigt?
- Alembic-Migrationen für 4 separate DBs konsistent?

### 5. Data Engineer
- ETL/ELT-Pipelines robust?
- Sync zwischen Watch ↔ Backend → Dashboard?
- Cold-Start-Sync korrekt?
- Rate Limiting aktiviert (slowapi)?
- DAL commits mit rollback?

### 6. Systemarchitekt
- 4-DB-Architektur (admin/activity/projects/health) gerechtfertigt?
- CORS korrekt konfiguriert?
- Secrets Management (SECRET_KEY, Fernet, REGISTRATION_KEY) sicher?
- Submodule-Strategie (Ghost-Repo vs working tree) stabil?
- Alembic-Chain lückenlos?

### 7. Softwareentwickler
- Code-Qualität (Clean Code, SOLID, KISS)?
- Error Handling (try/except) vollständig?
- Division-by-zero geschützt?
- Password-Hashing konsistent (PBKDF2-HMAC-SHA256)?
- Connect IQ: onUpdate() ohne Allocation? has: checks für API?

### 8. Produktmanager
- User Stories vollständig abgedeckt?
- Pacing-Feature klinisch sinnvoll?
- Spoon-Visualisierung ausreichend?
- Dashboard vs App Feature-Parität?
- Priorisierung (P0/P1/P2) klinischer Nutzen?

### 9. Projektmanager
- Task-Größe angemessen?
- Dependencies zwischen Tasks bekannt?
- Testabdeckung (E2E, Unit, Integration)?
- Timeline realistisch?
- Risikobewertung (Ghost-Submodule, CORS, DAL)?

### 10. Stakeholder (Investor/Betreiber)
- ROI des Features?
- Betriebskosten (4 DBs, Docker, CI/CD)?
- Skalierbarkeit?
- Wartbarkeit?
- Dokumentation aktuell?

## Integration Checkliste (pro Task)
- [ ] Alle 10 Perspektiven durchgegangen?
- [ ] App-Dashboard Navigation konsistent?
- [ ] Spoon/Pacing-Werte im Dashboard?
- [ ] Branch erstellt → implementiert → getestet → in feature gemergt?
- [ ] Telegram Report gesendet?
- [ ] Board aktualisiert?