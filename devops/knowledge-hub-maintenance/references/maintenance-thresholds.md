# System Health Thresholds (Knowledge Hub)

| Metrik | Schwelle | Aktion |
|---|---|---|
| state.db Größe | >30 MB | beobachten; >30 MB → `state-db-cleanup` Skill/Cron triggern |
| state.db Größe (korrigiert 2026-10-23) | > 400 MB | `state-db-cleanup` löst erst hier aus (`VACUUM` nach Löschung). 400–500 MB = beobachten, > 500 MB = `state-db-acceleration-response` + `PRAGMA integrity_check` |
| state.db Wachstum | >+10 MB/7d | Wachstumsursache prüfen (messages-Tabelle). Achtung: Wachstum kommt in Schüben — ein Flach-Fenster (60 s) widerlegt den Trend nicht, ein Plateau über ≥ 24 h schon |
| state.db Wachstumsrate | > 1 MB/h über 4 h | `state-db-acceleration-response` (nicht bei < 400 MB — Schwellen 400/500 MB sind die Trigger) |
| Kanban-Boards leer | >100 Tage | Struktur-Status berichten, KEINE fiktive Aktivität (Integrität > Aktivität) |
| kanban.db/projects.db | Größe konstant | "0 Zeilen in allen Tabellen" live via sqlite3 bestätigen |
| Pipe-Noise `^\|{2,}` | >0 Zeilen | Sofort bereinigen (HUB DATENKORROSION #3) |
| Dangling Skill-References | >0 | Vor Hub-Write fixen (Dateien erstellen oder Ref entfernen) |
| Cron median Inter-Arrival | Drift >25% vom Soll | Schedule-Problem prüfen |
| Profil-DBs | Plateau >7 Tage | dokumentieren (aktive Loops laufen im Hauptprofil) |
