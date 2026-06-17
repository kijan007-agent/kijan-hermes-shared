# Empty-Shell-Silence Rule

When a status-check cron job finds:
1. Spec files exist (e.g., in `kpt-doc/_specs/`)
2. Implementation files count = 0 (no models, DAL, routers, migrations)
3. All repos are empty shells (zero commits) or remotes unreachable
4. No prior implementation work to report progress on

→ Respond `[SILENT]` instead of generating a verbose zero-status report.

**Rationale:** A report stating "0% implemented, everything blocked" is noise, not signal. It provides no actionable information. Only report when there is genuine progress or a blocker requiring user action (e.g., "Remote repo deleted — needs re-clone").

**Trigger for reporting instead of silence:** When the blocker itself is new and requires user intervention (e.g., remote repo was previously accessible and is now gone).
