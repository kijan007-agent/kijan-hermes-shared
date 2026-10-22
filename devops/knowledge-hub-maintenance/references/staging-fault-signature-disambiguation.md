# Staging-Fault-Signatures: HTTP 000 und HTTP 500 richtig entziffern

Stand: 2026-10-22. Quelle: kpt-Board #589–#592 (Diagnose kijan-backend-staging:8011).

## HTTP 000 ist ein Timeout, kein Netzwerkfehler
`curl -w %{http_code}` liefert bei `--max-time`-Überschreitung die Ziffernfolge `000`. Das sieht wie
"Verbindung unmöglich" aus, ist aber ein **Request-Timeout**. Gegenprobe:
- `openssl s_client` / TCP-Connect auf den Port → in 1 ms erreichbar?
- `/health` → 200? `/openapi.json` → 200?
- Dann ist es kein Netzwerk-/Firewall-Problem, sondern eine **Blockierung auf Anwendungsebene**.

Häufigste Ursache in dieser Klasse: **DB-Lock-bedingter Request-Timeout** — der Connection-Pool
blockiert während eines nächtlichen Prod→Staging-DB-Resyncs. Nicht: Crash-Loop, OOM, not-listening.

## Ein HTTP 500 kann zwei völlig verschiedene Ursachen haben
Im selben Service, zur selben Zeit, mit derselben Symptomklasse:
1. **Jinja2-Template-Fehler** — `jinja2.exceptions.UndefinedError: '_b' is undefined`
   (`templates/components/analytics.html:155`, eingebunden von `personal_dashboard.html:540`).
2. **TypeError im Template** — `TypeError: get expected at most 2 arguments, got 3`
   (`templates/pacing.html:201`).
Beide laufen in einem **Catch-all-Handler** (`app/main.py:884-902`, `logger.error` mit vollem Traceback)
und werden als HTTP 500 beantwortet. Ein 500er im Log ohne Exception-Text ist nicht interpretierbar.

## Wenn die Primär-Evidenz fehlt
Container-Logs waren aus dem Worker-Container nicht abrufbar (kein Docker/SSH auf dem Staging-Host).
Belastbarer Ersatz: **deterministische Reproduktion aus dem exakt deployten Commit** — hier `22ebe168`,
mit identischem Exception-Wortlaut inkl. Datei und Zeile. Besser als eine Vermutung über
Provider-Limits oder Quotas.

## Regeln
- **Fehlersignal ≠ Ursache.** HTTP-Code, Timeout-Flag und Exception-Text immer getrennt auflösen.
- **Downstream-Check ausschliessen:** gezielt nach Provider-/Quota-Begriffen im betroffenen Codepfad
  suchen, bevor ein Provider-Problem angenommen wird.
- **Merge-zu-Detection-Latenz messen** (hier 17 min) — sie zeigt, ob der Fehler live deployed war.
- **Fix-Status über alle Umgebungen prüfen:** Fix auf Staging vorhanden, aber `upstream/prod`
  enthielt ihn noch — Staging-„grün" ist kein Prod-„grün".
