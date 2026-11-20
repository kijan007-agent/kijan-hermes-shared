#!/usr/bin/env python3
"""set-compression-limits.py — cross-profile setzen der Kontext-Kompaktierungs-Deckel.

Warum: Jedes Profil laedt seine eigene config.yaml (HERMES_HOME=<profil>); die globale
Config wird NICHT geerbt (hermes_cli/config.py: _load_config_impl merged DEFAULT_CONFIG mit
genau EINER Datei: get_config_path()). Ohne explizite Werte faellt daher jedes Profil auf
die Defaults zurueck: context_total_ceiling_seconds=600 und ein
auxiliary.compression.timeout, der auf den Floor von 300 s (agent/auxiliary_client.py:
_COMPRESSION_TIMEOUT_FLOOR_SECONDS) gehoben wird. Bei sehr grossen Kontexten (~133k Tokens,
Lauf 62846) bricht die Zusammenfassung nach 300 s ab, der Fence laeuft nach 600 s in die
Deckel-Meldung "Context compression reached its total ceiling" — die Kompaktierung greift
dann nicht mehr.

Dieses Skript setzt die drei Deckel idempotent in der globalen Config und in allen
Profil-Configs. Die Dateien werden zeilenweise editiert (Kommentare, Reihenfolge und
Formatierung bleiben erhalten); danach wird das Ergebnis mit yaml.safe_load validiert.

Aufruf:
  scripts/set-compression-limits.py --dry-run
  scripts/set-compression-limits.py --profiles-root /workspace/.hermes/profiles
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import yaml

DEFAULT_CEILING = 1800
DEFAULT_IDLE = 300
DEFAULT_AUX_TIMEOUT = 900

KEYS = (
    (("compression", "context_total_ceiling_seconds"), DEFAULT_CEILING),
    (("compression", "context_timeout_seconds"), DEFAULT_IDLE),
    (("auxiliary", "compression", "timeout"), DEFAULT_AUX_TIMEOUT),
)


def _find_key(lines, key, indent, start=0, end=None):
    """Index + Inline-Rest der Zeile ``key:`` mit exakt ``indent`` Eingerueckung."""
    pat = re.compile(r"^ {%d}%s:\s*(.*)$" % (indent, re.escape(key)))
    end = len(lines) if end is None else end
    for i in range(start, end):
        m = pat.match(lines[i])
        if m:
            return i, m.group(1)
    return None, None


def _child_indent(lines, start, indent):
    """Eingerueckung der Kinder eines Blockes (Standard: parent + 2)."""
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cur = len(line) - len(line.lstrip())
        if cur <= indent:
            break
        return cur
    return indent + 2


def _split_comment(rest):
    """Inline-Kommentar einer YAML-Zeile erhalten (``value  # comment``)."""
    m = re.search(r"\s+#", rest)
    if m:
        return rest[: m.start()].strip(), "  " + rest[m.start():].strip()
    return rest.strip(), ""


def _block_end(lines, start, indent):
    """Index der letzten Zeile des Blockes, der bei ``start`` (Indent ``indent``) beginnt."""
    last = start
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if len(line) - len(line.lstrip()) <= indent:
            break
        last = i
    return last


def _top_insert_pos(lines):
    """Top-Level-Eintrag hinter fuehrenden Kommentar-/Leerzeilen und ggf. ``---``."""
    at = 0
    while at < len(lines) and (not lines[at].strip() or lines[at].lstrip().startswith("#")):
        at += 1
    if at < len(lines) and lines[at].strip() == "---":
        at += 1
    return at


def _set_in_parent(lines, parent_idx, parent_indent, key, value):
    """Setzt ``key: value`` als Kind von ``parent_idx``. Sucht NUR in dessen Block."""
    end = _block_end(lines, parent_idx, parent_indent)
    child_indent = _child_indent(lines, parent_idx, parent_indent)
    idx, rest = _find_key(lines, key, child_indent, parent_idx + 1, end + 1)
    if idx is not None:
        _, comment = _split_comment(rest)
        new = "%s%s: %s%s" % (" " * child_indent, key, value, comment)
        if lines[idx] == new:
            return False
        lines[idx] = new
        return True
    lines.insert(parent_idx + 1, "%s%s: %s" % (" " * child_indent, key, value))
    return True


def _set_path(lines, path, value):
    """Setzt ``path[-1]: value``; legt fehlende Zwischenbloecke an. True bei Aenderung.

    Die Suche nach jedem Pfadschritt ist auf den Block des Elternschrittes beschraenkt —
    sonst trifft ein gaengiger Name (z. B. ``timeout``) das erste Vorkommen in einer
    anderen Sektion.
    """
    indent = 0
    parent_idx = None
    parent_indent = 0
    for depth, key in enumerate(path[:-1]):
        lo = parent_idx + 1 if parent_idx is not None else 0
        hi = _block_end(lines, parent_idx, parent_indent) + 1 if parent_idx is not None else len(lines)
        idx, rest = _find_key(lines, key, indent, lo, hi)
        if idx is None:
            at = _top_insert_pos(lines) if parent_idx is None else parent_idx + 1
            lines.insert(at, "%s%s:" % (" " * indent, key))
            idx, parent_idx, parent_indent = at, at, indent
        else:
            if rest.strip():
                # Inline-Skalar -> Block umwandeln, naechstes Pfadelement als Kind anlegen.
                lines[idx] = "%s%s:" % (" " * indent, key)
                lines.insert(idx + 1, "%s%s:" % (" " * (indent + 2), path[depth + 1]))
            parent_idx, parent_indent = idx, indent
        indent = _child_indent(lines, parent_idx, parent_indent)
    if parent_idx is None:
        idx, rest = _find_key(lines, path[-1], 0)
        if idx is None:
            lines.insert(_top_insert_pos(lines), "%s: %s" % (path[-1], value))
        else:
            _, comment = _split_comment(rest)
            lines[idx] = "%s: %s%s" % (path[-1], value, comment)
        return True
    return _set_in_parent(lines, parent_idx, parent_indent, path[-1], value)


def set_limits(text, values):
    """Setzt alle Keys in einem Config-Text. Gibt (neuer_text, liste_der_aenderungen) zurueck."""
    lines = text.splitlines()
    changed = []
    for path, default in KEYS:
        value = values.get(path, default)
        before = list(lines)
        if _set_path(lines, path, value):
            changed.append(".".join(path))
        else:
            lines = before
    return "\n".join(lines) + "\n", changed


def expected(cfg, values):
    """Prueft die gesetzten Werte in einem geparsten Config-Dict."""
    problems = []
    for path, value in values.items():
        node = cfg
        for part in path:
            if not isinstance(node, dict) or part not in node:
                problems.append("%s fehlt" % ".".join(path))
                node = None
                break
            node = node[part]
        if node is None:
            continue
        if node != value:
            problems.append("%s = %r (erwartet %r)" % (".".join(path), node, value))
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kompaktierungs-Deckel cross-profile setzen")
    ap.add_argument("--profiles-root", default="/workspace/.hermes/profiles")
    ap.add_argument("--global-config", default=None,
                    help="globale config.yaml (Default: <profiles-root>/../config.yaml)")
    ap.add_argument("--ceiling", type=int, default=DEFAULT_CEILING)
    ap.add_argument("--idle", type=int, default=DEFAULT_IDLE)
    ap.add_argument("--aux-timeout", type=int, default=DEFAULT_AUX_TIMEOUT)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    values = {
        ("compression", "context_total_ceiling_seconds"): args.ceiling,
        ("compression", "context_timeout_seconds"): args.idle,
        ("auxiliary", "compression", "timeout"): args.aux_timeout,
    }

    profiles_root = os.path.abspath(args.profiles_root)
    global_config = args.global_config or os.path.join(os.path.dirname(profiles_root), "config.yaml")
    targets = []
    if os.path.isfile(global_config):
        targets.append(global_config)
    for name in sorted(os.listdir(profiles_root)):
        cfg = os.path.join(profiles_root, name, "config.yaml")
        if os.path.isfile(cfg):
            targets.append(cfg)

    failures = 0
    for path in targets:
        name = os.path.basename(os.path.dirname(path)) if "profiles" in path else "GLOBAL"
        original = open(path, encoding="utf-8").read()
        try:
            new_text, changed = set_limits(original, values)
        except Exception as exc:  # pragma: no cover - defensiv
            print("[set-compression-limits] %s: FEHLER beim Editieren: %s" % (name, exc))
            failures += 1
            continue
        if not changed:
            print("[set-compression-limits] %s: bereits korrekt — keine Aenderung" % name)
            continue
        try:
            parsed = yaml.safe_load(new_text)
        except Exception as exc:
            print("[set-compression-limits] %s: YAML ungueltig nach Edit (%s) — Datei unveraendert"
                  % (name, str(exc).splitlines()[0]))
            failures += 1
            continue
        problems = expected(parsed or {}, values)
        if problems:
            print("[set-compression-limits] %s: Validierung fehlgeschlagen — Datei unveraendert: %s"
                  % (name, "; ".join(problems)))
            failures += 1
            continue
        if args.dry_run:
            print("[set-compression-limits] %s: DRY-RUN — wuerde setzen: %s" % (name, ", ".join(changed)))
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        print("[set-compression-limits] %s: gesetzt: %s" % (name, ", ".join(changed)))
    print("[set-compression-limits] %d Datei(en) geprueft, %d Fehler" % (len(targets), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
