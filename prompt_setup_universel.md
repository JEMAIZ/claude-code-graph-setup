# Prompt universel — Setup + fusion CLAUDE.md + refresh des graphs

Copie-colle ce prompt dans Claude Code sur chaque repo.

---

```
Avant toute chose, fais un diagnostic complet de ce projet :

1. Vérifie si ces éléments existent :
   - graphify-out/GRAPH_REPORT.md       → Graphify installé ?
   - .understand-anything/              → Understand Anything installé ?
   - .mcp.json ou settings.json contenant code-review-graph → installé ?
   - .git/hooks/post-commit             → hook git Graphify actif ?
   - Un fichier CLAUDE.md existant ?

2. En fonction de ce que tu trouves, installe ce qui manque :

   Si Graphify manque :
     pip install graphifyy
     graphify install
     graphify claude install
     puis lance : /graphify .

   Si le hook git Graphify est absent ou inactif :
     graphify claude install
     vérifie que .git/hooks/post-commit existe et est exécutable

   Si code-review-graph manque :
     pip install code-review-graph
     code-review-graph install --platform claude-code

   Si Understand Anything manque :
     /plugin marketplace add Lum1104/Understand-Anything
     /plugin install understand-anything
     puis lance : /understand --auto-update

   Si Understand Anything est installé mais --auto-update inactif :
     /understand --auto-update

3. Vérifie la fraîcheur des graphs déjà présents :

   Pour Graphify :
     Compare la date de graphify-out/GRAPH_REPORT.md
     avec le dernier git commit (git log -1 --format=%ci)
     Si le graph est plus ancien → lance /graphify .

   Pour Understand Anything :
     Compare la date de .understand-anything/knowledge-graph.json
     avec le dernier git commit
     Si le graph est plus ancien → lance /understand

   Pour code-review-graph :
     Pas besoin — il se met à jour automatiquement à chaque édition

4. Une fois les trois outils installés, configurés et à jour,
   fusionne les instructions ci-dessous dans le CLAUDE.md
   existant de ce projet :
   - Si une section similaire existe déjà → enrichis-la
   - Si c'est nouveau → ajoute à la fin
   - Ne supprime rien de l'existant
   - Conserve le style du CLAUDE.md actuel
   - Montre-moi le résultat final avant d'écrire le fichier

--- DÉBUT DES INSTRUCTIONS À FUSIONNER ---

## 🗺️ Knowledge Graphs disponibles

Ce projet utilise trois outils complémentaires de graph. Lis-les dans cet ordre au démarrage :

1. **Graphify** → `graphify-out/GRAPH_REPORT.md`
   - Consulte ce fichier AVANT toute recherche par Glob ou Grep
   - Ne relis jamais les fichiers sources si l'information est dans le graph

2. **Understand Anything** → `.understand-anything/knowledge-graph.json`
   - Utilise-le pour comprendre l'architecture métier et les flux fonctionnels

3. **code-review-graph** → disponible via MCP
   - Utilise-le pour les revues de code et l'analyse d'impact

---

## 🔄 Refresh des graphs — règles automatiques

### Au démarrage de chaque session, vérifie la fraîcheur :

  # Date du dernier commit
  git log -1 --format=%ci

  # Comparer avec les dates de modification de :
  # graphify-out/GRAPH_REPORT.md
  # .understand-anything/knowledge-graph.json

| Graph | Mise à jour automatique | Action si obsolète |
|---|---|---|
| Graphify | Hook git post-commit | `/graphify .` |
| Understand Anything | `--auto-update` activé | `/understand` |
| code-review-graph | À chaque édition de fichier | Rien à faire |

Règle absolue : si un graph est plus ancien que le dernier commit,
reconstruit-le avant de l'utiliser.

### Si le hook Graphify ne fonctionne plus :
  ls -la .git/hooks/post-commit
  # Si absent → relancer : graphify claude install

---

## 🚀 Workflow par situation

| Situation | Outil |
|---|---|
| Où est défini X ? | `graphify-out/GRAPH_REPORT.md` → god nodes |
| Qui appelle la fonction Y ? | `query_graph_tool` (code-review-graph MCP) |
| Comment fonctionne le flux Z ? | `/understand-chat` |
| Impact de mon changement ? | `/understand-diff` puis `pre_merge_check` |
| Chercher dans les fichiers bruts | Dernier recours uniquement |

### Au démarrage de chaque session
1. Vérifie la fraîcheur des graphs (voir section Refresh)
2. Lis `graphify-out/GRAPH_REPORT.md` pour t'orienter
3. Si la tâche implique un domaine métier → `/understand-chat <question>`
4. Ne relis pas les fichiers sources tant que le graph répond

### Avant un PR / merge
1. `/understand-diff` — analyser l'impact
2. `pre_merge_check` via code-review-graph MCP
3. Vérifier la couverture de tests

---

## 💡 Gestion du contexte

- Lance `/compact` dès que le contexte atteint 60%
- Lance `/clear` à chaque nouvelle tâche indépendante
- Ne charge jamais un fichier entier si le graph répond déjà

---

## 🚫 À ne pas faire

- Ne pas relire tous les fichiers sources au démarrage
- Ne pas utiliser Grep/Glob avant d'avoir consulté le graph
- Ne pas laisser le contexte dépasser 80% sans `/compact`
- Ne pas utiliser un graph plus ancien que le dernier commit

--- FIN DES INSTRUCTIONS À FUSIONNER ---
```
