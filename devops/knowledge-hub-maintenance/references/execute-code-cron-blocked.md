# execute_code in Cron-Runs

**Stand 2026-09-25:** `execute_code` war in früheren Cron-Läufen teils blockiert; verlässlicher Weg
im Cron-Modus ist `terminal(command='python3 -c "..."')` (Einzelpython, kein Kernel-State).
Fallback-Reihenfolge:
1. `terminal` + `python3 -c` (kurze, gebundene Ausgaben; `| head -N` gegen CCR-Masking)
2. `execute_code` (persistenter Kernel) — nur wenn verfügbar; bei CCR-Platzhalter `<<ccr:...>>` Output via Datei/Zwischen-Pipe binden
3. Bei CCR-Platzhalter `<<ccr:...>>`: Skill `cli-ccr-output-truncation` — Ausgabe klein halten, Datei schreiben, `read_file` mit limit
