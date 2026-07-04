# Monkey.jungle test Annotation Exclude

## Problem
Monkeyc kompiliert `(:test)`-annotierte Dateien STANDARDMÄSSIG in die App. Test-Dateien wie `TestScreenFlowController.mc` enthalten Methoden die in produktiven SDKs nicht existieren (`:setCurrentScreen`, etc.).

## Lösung
In `monkey.jungle` (und allen `monkey-{env}.jungle`):
```
base.excludeAnnotations = prod;staging;test
```

## WICHTIG
- `test` MUSS explizit in excludeAnnotations stehen — es wird NICHT automatisch excluded
- Ohne `test` in excludeAnnotations: 100+ Compile-Fehler durch Test-Code
- Für dev/staging builds muss die jeweils andere Annotation excluded werden:
  - `monkey-dev.jungle`: `base.excludeAnnotations = prod;staging;test`
  - `monkey-staging.jungle`: `base.excludeAnnotations = prod;dev;test`
  - `monkey-prod.jungle`: `base.excludeAnnotations = dev;staging;test`

## Test-Dateien identifizieren
```bash
# Alle (:test) annotierte Dateien finden
grep -r "(:test)" source/ --include="*.mc"
```

## Typische Test-Dateien
- `Test*.mc` — Test-Framework Klassen
- `TestScreenFlowController.mc` — enthält `setCurrentScreen(:screen)` calls (ungültig in SDK)
- `TestFeedback.mc` — Test-Callbacks

## Verify
Nach dem Update von `monkey.jungle`:
```bash
monkeyc -f monkey.jungle -d <device> -o /tmp/test.prg -y key.der -t -l 3 2>&1 | grep -c "error"
# Sollte 0 sein (oder nur echte Code-Fehler, keine Test-Fehler)
```
