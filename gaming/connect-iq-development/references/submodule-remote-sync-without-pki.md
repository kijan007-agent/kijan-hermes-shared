# Submodule Remote Sync Without SSH-PKI

## Problem
Submodule hat lokale Commits die mit `origin/feature` divergieren. SSH-PKI Auth nicht verfügbar (`Permission denied (publickey)`). Kein GitHub Token verfügbar.

## Lösung: Content-Extraktion via `git show <sha>:<path>`

### Schritt 1: Divergenz analysieren
```bash
# Welche Commits sind nur auf origin/feature?
git log --oneline feature..origin/feature

# Welche Commits sind nur lokal?
git log --oneline origin/feature..feature

# Gemeinsamer Merge-Base
git merge-base feature origin/feature
```

### Schritt 2: Neue Remote-Commits identifizieren
```bash
# Nur die neuen Commits seit Merge-Base
git log --oneline --ancestry-path <merge-base>..origin/feature
```

### Schritt 3: Content extrahieren (ohne fetch/pull)
```bash
# Für jede geänderte Datei den Inhalt aus dem Remote-Commit holen
git show <commit>:<pfad/zur/datei> > <lokaler/pfad/zur/datei>
```

### Schritt 4: Diff auf CRLF normalisieren
```bash
# Working tree mit CRLF normalisieren
cat <file> | tr -d '\r' > /tmp/wt_normalized

# Remote version mit CRLF normalisieren
git show origin/feature:<file> | tr -d '\r' > /tmp/remote_normalized

# Diff prüfen
diff /tmp/wt_normalized /tmp/remote_normalized
```

### Schritt 5: Commit und Parent-Repo updaten
```bash
git add <datei1> <datei2> ...
git commit -m "sync: apply remote changes from <commit-sha>"
git add <submodule-path> .gitmodules
git commit -m "chore(<submodule>): sync to remote tip"
```

## Pitfalls
- **Niemals `submodule update --init` VOR dem Commit** — das resettet den Submodule-HEAD auf den recorded SHA und verliert alle Änderungen
- **CRLF-Diffs täuschen** — `git diff` zeigt oft 1000+ Zeilen wegen CRLF. Immer nach Content-Diffs filtern
- **Git-Diff vs Content-Diff** — `git diff HEAD` zeigt den Working-Tree-Diff. Für inhaltliche Prüfung: `git show` vergleichen

## Example Session
```bash
# kpt-app-ciq divergiert von origin/feature
# origin/feature hat 2 neue Commits: 0727f60 (merge) und 00872e5 (inhaltlich)

# Content von 00872e5 extrahieren
git show 00872e5:source/ActivitySync.mc > source/ActivitySync.mc
git show 00872e5:source/PacingSpoonsCheckinView.mc > source/PacingSpoonsCheckinView.mc
git show 00872e5:source/SyncNetworkManager.mc > source/SyncNetworkManager.mc

# Commit
git add source/ActivitySync.mc source/PacingSpoonsCheckinView.mc source/SyncNetworkManager.mc
git commit -m "sync: apply origin/feature tip (00872e5)"

# Parent-Repo updaten
cd /workspace/Github/KijanPersonalTracker-hermes
git add kpt-app-ciq .gitmodules
git commit -m "chore(kpt-app-ciq): sync to origin/feature tip"
```

## When to Use
- SSH-PKI nicht verfügbar für Remote-Auth
- Nur Lesepflicht für Remote-Commits (kein Push nötig)
- Remote-Commits enthalten Content-Änderungen die benötigt werden
- Git-fsck oder andere Tools nicht verfügbar für direktes Push

## Alternatives
- SSH-Key auf GitHub hinzufügen (empfohlen für langfristige Lösung)
- GitHub Personal Access Token konfigurieren
- Direkter Download der diffs als patches
