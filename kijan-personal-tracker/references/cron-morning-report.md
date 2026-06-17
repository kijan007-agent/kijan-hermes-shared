# Morning Report Cron Delivery Pattern

## Pattern
When the user says "bericht mir morgen vormittag" or equivalent:

1. Create the full report/analysis as a `.md` file in the project workspace (e.g., `kpt-doc/_tasks/REVIEW_SUMMARY.md`)
2. Create a one-shot cron job:
   ```
   cronjob create name="<name>" schedule="YYYY-MM-DDT08:00:00" repeat="1" deliver="origin" prompt="<brief instructions>"
   ```
3. The prompt should:
   - Reference the full report file path
   - Instruct to read the file and send a **concise summary** (not the full file)
   - Include focus points (critical items, next steps)
4. Confirm to user: "Cron-Job um 08:00 sendet dir morgen eine prägnante Zusammenfassung"

## Key Principle
- **Full detail** in the markdown file (for reference)
- **Concise summary** in the delivered message (for quick reading)
- Never dump the entire analysis in the cron prompt itself

## Example cron job
```
name: feature-branch-review-delivery
schedule: 2025-05-11T08:00:00
deliver: origin
prompt: |
  Sende Jan die Feature-Branch-Review-Zusammenfassung.
  Der Review ist unter: /workspace/Github/.../REVIEW_SUMMARY.md
  Lies die Datei und sende eine prägnante Zusammenfassung.
  Fokus: 1) Was hat sich geändert 2) Kritische Files 3) Nächste Schritte
```