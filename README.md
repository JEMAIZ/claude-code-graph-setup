# claude-code-graph-setup

> **EN** — Automatically configure Claude Code with knowledge graph tools, adapted to your project size.
>
> **FR** — Configure automatiquement Claude Code avec des outils de knowledge graph, adaptés à la taille de ton projet.

---

## English

### The problem

Every Claude Code session, the model re-reads your entire codebase to orient itself. On a 500-file project, that's 20,000+ tokens burned before a single useful question. Multiply by 10 sessions a day and the cost becomes significant.

### The solution

This repo provides a single Python script that:

- **Counts** tracked code files in your git repo
- **Decides** which graph tools make sense based on project size
- **Detects** what's already installed
- **Checks** whether existing graphs are stale vs. the last commit
- **Merges** cleanly into your existing `CLAUDE.md` without overwriting anything

### The three tools orchestrated

| Tool | Role | Activated above |
|---|---|---|
| [Graphify](https://github.com/safishamsi/graphify) | Structural map of the codebase | 80 files |
| [Understand Anything](https://github.com/Lum1104/Understand-Anything) | Visual dashboard + business domain view | 80 files |
| [code-review-graph](https://github.com/tirth8205/code-review-graph) | AST call graph, test coverage, PR review | 50 files |

Below 50 files: Claude reads files directly — no graph overhead needed.

### Quick start

```bash
# Clone or download setup_claude.py into your project root
cd your-project

# Preview without writing anything
python setup_claude.py --dry-run

# Apply
python setup_claude.py
```

### What it writes

The script injects a `<!-- graph-tools:start -->` / `<!-- graph-tools:end -->` block into your `CLAUDE.md`. Re-running it updates only that block — the rest of your `CLAUDE.md` is never touched.

**Example output for a mature project (200+ files):**

```markdown
## 🗺️ Codebase navigation

Project: 247 code files detected — mature profile.

### Active tools
- Graphify ✅ → graphify-out/GRAPH_REPORT.md
- Understand Anything ✅ → .understand-anything/knowledge-graph.json
- code-review-graph ✅ → via MCP

### Refresh rules
| Graph | Auto-update | If stale |
|---|---|---|
| Graphify | git post-commit hook | /graphify . |
| Understand Anything | --auto-update | /understand |
| code-review-graph | on every file edit | nothing |
```

**Example output for a small project (< 50 files):**

```markdown
## 🗺️ Codebase navigation

Project: 23 code files — early stage.
Read files directly — no graph needed.
Run /clear between independent tasks.
```

### Requirements

- Python 3.10+
- git (for tracking file count and commit dates)

---

## Français

### Le problème

À chaque session Claude Code, le modèle relit l'intégralité du projet pour s'orienter. Sur 500 fichiers, ce sont 20 000+ tokens brûlés avant la moindre question utile. Multiplié par 10 sessions par jour, le coût devient significatif.

### La solution

Ce repo fournit un script Python qui :

- **Compte** les fichiers de code trackés par git
- **Décide** quels outils de graph ont du sens selon la taille du projet
- **Détecte** ce qui est déjà installé
- **Vérifie** si les graphs existants sont obsolètes par rapport au dernier commit
- **Fusionne** proprement dans ton `CLAUDE.md` existant sans rien écraser

### Les trois outils orchestrés

| Outil | Rôle | Activé au-dessus de |
|---|---|---|
| [Graphify](https://github.com/safishamsi/graphify) | Carte structurelle du codebase | 80 fichiers |
| [Understand Anything](https://github.com/Lum1104/Understand-Anything) | Dashboard visuel + domaines métier | 80 fichiers |
| [code-review-graph](https://github.com/tirth8205/code-review-graph) | Graphe AST, couverture de tests, PR review | 50 fichiers |

Sous 50 fichiers : Claude lit les fichiers directement — pas besoin de graph.

### Démarrage rapide

```bash
# Clone ou télécharge setup_claude.py à la racine de ton projet
cd ton-projet

# Aperçu sans rien écrire
python setup_claude.py --dry-run

# Applique
python setup_claude.py
```

### Ce que ça écrit

Le script injecte un bloc `<!-- graph-tools:start -->` / `<!-- graph-tools:end -->` dans ton `CLAUDE.md`. À chaque ré-exécution, il met à jour uniquement ce bloc — le reste du `CLAUDE.md` n'est jamais touché.

### Prérequis

- Python 3.10+
- git (pour le comptage de fichiers et les dates de commit)

---

## Repository structure

```
claude-code-graph-setup/
├── setup_claude.py          # main script
├── prompt_setup_universel.md # Claude Code prompt to install tools + merge CLAUDE.md
├── .claude/
│   └── graphs.md            # detailed graph tool reference (loaded on demand)
└── README.md
```

---

## License

MIT — use freely, contributions welcome.
