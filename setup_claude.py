#!/usr/bin/env python3
"""
setup_claude.py — Analyse le repo et génère/met à jour CLAUDE.md
en activant Graphify et code-review-graph uniquement si pertinent.

Usage :
  python setup_claude.py           # depuis la racine du repo
  python setup_claude.py --dry-run # aperçu sans écrire
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# ── Seuils ────────────────────────────────────────────────────────────────────
THRESHOLD_GRAPHIFY = 80        # fichiers code minimum pour activer Graphify
THRESHOLD_CRG      = 50        # fichiers code minimum pour activer code-review-graph
THRESHOLD_UA       = 80        # fichiers code minimum pour activer Understand Anything

# Extensions considérées comme du code
CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java",
    ".c", ".cpp", ".cs", ".rb", ".php", ".swift", ".kt", ".scala",
    ".vue", ".svelte", ".ex", ".exs", ".zig", ".lua"
}

DRY_RUN = "--dry-run" in sys.argv

# ── Analyse du repo ────────────────────────────────────────────────────────────
def count_code_files(root: Path) -> tuple[int, list[str]]:
    """Compte les fichiers de code trackés par git (ou tous si pas de git)."""
    try:
        result = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, cwd=root
        )
        files = [f for f in result.stdout.splitlines() if Path(f).suffix in CODE_EXTENSIONS]
    except Exception:
        files = [
            str(p.relative_to(root))
            for p in root.rglob("*")
            if p.suffix in CODE_EXTENSIONS and ".git" not in p.parts
        ]
    return len(files), files


def get_last_commit_date(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci"], capture_output=True, text=True, cwd=root
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def check_installed(root: Path) -> dict[str, bool]:
    """Détecte ce qui est déjà installé."""
    return {
        "graphify":         (root / "graphify-out" / "GRAPH_REPORT.md").exists(),
        "understand":       (root / ".understand-anything").exists(),
        "crg":              _crg_in_mcp(root),
        "graphify_hook":    (root / ".git" / "hooks" / "post-commit").exists(),
    }


def _crg_in_mcp(root: Path) -> bool:
    for fname in [".mcp.json", ".claude/settings.json"]:
        p = root / fname
        if p.exists() and "code-review-graph" in p.read_text(encoding="utf-8", errors="replace"):
            return True
    return False


def graph_is_stale(graph_path: Path, root: Path) -> bool:
    """Retourne True si le graph est plus vieux que le dernier commit."""
    if not graph_path.exists():
        return False
    last_commit = get_last_commit_date(root)
    if not last_commit:
        return False
    graph_mtime = datetime.fromtimestamp(graph_path.stat().st_mtime)
    commit_dt   = datetime.fromisoformat(last_commit[:19])
    return graph_mtime < commit_dt


# ── Génération du CLAUDE.md ────────────────────────────────────────────────────
def build_section(file_count: int, installed: dict, root: Path) -> str:
    use_graphify  = file_count >= THRESHOLD_GRAPHIFY
    use_crg       = file_count >= THRESHOLD_CRG
    use_ua        = file_count >= THRESHOLD_UA

    lines = ["## 🗺️ Navigation du codebase\n"]
    lines.append(f"_Projet : **{file_count} fichiers de code** détectés — "
                 f"profil {'mature' if file_count >= THRESHOLD_GRAPHIFY else 'en construction'}._\n")

    # ── Outils actifs ──
    if not any([use_graphify, use_crg, use_ua]):
        lines.append(
            "Ce projet est petit (< 50 fichiers). "
            "Lis les fichiers directement — pas besoin de graph.\n"
            "Lance `/clear` entre chaque tâche indépendante.\n"
        )
        return "\n".join(lines)

    lines.append("### Outils activés\n")

    if use_graphify:
        stale = graph_is_stale(root / "graphify-out" / "GRAPH_REPORT.md", root)
        status = "⚠️ graph obsolète — relance `/graphify .`" if stale else ("✅ installé" if installed["graphify"] else "❌ non installé")
        lines.append(f"- **Graphify** ({status}) → `graphify-out/GRAPH_REPORT.md`")
        lines.append("  - Lis ce fichier AVANT tout Glob/Grep")
        lines.append("  - Ne relis pas les sources si le graph répond déjà\n")

    if use_ua:
        status = "✅ installé" if installed["understand"] else "❌ non installé"
        lines.append(f"- **Understand Anything** ({status}) → `.understand-anything/knowledge-graph.json`")
        lines.append("  - Pour les flux métier : `/understand-chat <question>`")
        lines.append("  - Avant un PR : `/understand-diff`\n")

    if use_crg:
        status = "✅ installé" if installed["crg"] else "❌ non installé"
        lines.append(f"- **code-review-graph** ({status}) → via MCP")
        lines.append("  - Qui appelle quoi : `query_graph_tool`")
        lines.append("  - Avant merge : `pre_merge_check`\n")

    # ── Workflow ──
    lines.append("### Workflow par situation\n")
    lines.append("| Situation | Action |")
    lines.append("|---|---|")
    if use_graphify:
        lines.append("| Où est défini X ? | `graphify-out/GRAPH_REPORT.md` |")
    if use_crg:
        lines.append("| Qui appelle Y ? | `query_graph_tool` |")
    if use_ua:
        lines.append("| Impact de mon changement ? | `/understand-diff` |")
    lines.append("| Chercher dans les fichiers | Dernier recours uniquement |\n")

    # ── Refresh ──
    if use_graphify or use_ua:
        lines.append("### Refresh des graphs\n")
        lines.append("Au démarrage, compare la date du graph avec `git log -1 --format=%ci` :\n")
        lines.append("| Graph | Auto-update | Si obsolète |")
        lines.append("|---|---|---|")
        if use_graphify:
            lines.append("| Graphify | hook git post-commit | `/graphify .` |")
        if use_ua:
            lines.append("| Understand Anything | `--auto-update` | `/understand` |")
        if use_crg:
            lines.append("| code-review-graph | à chaque édition | rien à faire |")
        lines.append("")

    # ── Contexte ──
    lines.append("### Gestion du contexte\n")
    lines.append("- `/compact` dès 60% de contexte utilisé")
    lines.append("- `/clear` à chaque nouvelle tâche indépendante\n")

    return "\n".join(lines)


def merge_into_claude_md(root: Path, new_section: str) -> None:
    claude_md = root / "CLAUDE.md"
    marker_start = "<!-- graph-tools:start -->"
    marker_end   = "<!-- graph-tools:end -->"

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8", errors="replace")
        if marker_start in content:
            # Remplace le bloc existant
            before = content.split(marker_start)[0]
            after  = content.split(marker_end)[-1]
            updated = f"{before}{marker_start}\n{new_section}\n{marker_end}{after}"
        else:
            # Ajoute à la fin
            updated = content.rstrip() + f"\n\n{marker_start}\n{new_section}\n{marker_end}\n"
    else:
        updated = f"{marker_start}\n{new_section}\n{marker_end}\n"

    if DRY_RUN:
        print("── DRY RUN — contenu qui serait écrit ──────────────────")
        print(updated)
        print("────────────────────────────────────────────────────────")
    else:
        claude_md.write_text(updated, encoding="utf-8")
        print(f"✅ CLAUDE.md mis à jour ({claude_md})")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    root = Path.cwd()
    print(f"📁 Analyse de : {root}")

    file_count, _ = count_code_files(root)
    installed     = check_installed(root)

    print(f"   Fichiers de code : {file_count}")
    print(f"   Graphify         : {'✅' if installed['graphify'] else '❌'}"
          f"{'  (hook git ✅)' if installed['graphify_hook'] else '  (hook git ❌)'}")
    print(f"   Understand Anything : {'✅' if installed['understand'] else '❌'}")
    print(f"   code-review-graph   : {'✅' if installed['crg'] else '❌'}")
    print()

    # Alertes de fraîcheur
    if installed["graphify"]:
        if graph_is_stale(root / "graphify-out" / "GRAPH_REPORT.md", root):
            print("⚠️  Graphify : graph obsolète par rapport au dernier commit → /graphify .")
    if installed["understand"]:
        if graph_is_stale(root / ".understand-anything" / "knowledge-graph.json", root):
            print("⚠️  Understand Anything : graph obsolète → /understand")

    section = build_section(file_count, installed, root)
    merge_into_claude_md(root, section)

    if DRY_RUN:
        print("\n(Aucun fichier modifié — mode dry-run)")


if __name__ == "__main__":
    main()
