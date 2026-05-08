# Graph Tools — Detailed Reference

> This file is loaded on demand by Claude Code, not at every session start.
> Reference it when you need specifics on a tool or command.

---

## Graphify

**Role**: Structural map of the entire codebase — files, functions, dependencies, god nodes, community clusters.

**Key files**
- `graphify-out/GRAPH_REPORT.md` — one-page audit, read this first
- `graphify-out/graph.json` — full queryable graph
- `graphify-out/graph.html` — interactive browser view

**Commands**
```bash
/graphify .                  # build or rebuild the graph
/graphify .  --dedup-llm     # deduplicate inferred relationships
```

**Auto-update**: git post-commit hook (installed via `graphify claude install`)

**Check hook is active**:
```bash
ls -la .git/hooks/post-commit
# If missing → run: graphify claude install
```

**When to use**
- Start of session: read `GRAPH_REPORT.md` before any Glob/Grep
- "Where is X defined?" → god nodes section
- "What depends on Y?" → community structure

---

## Understand Anything

**Role**: Visual interactive dashboard + business domain extraction + plain-English explanations.

**Key files**
- `.understand-anything/knowledge-graph.json` — full graph
- Dashboard opens automatically after `/understand`

**Commands**
```bash
/understand                          # build or rebuild
/understand --auto-update            # enable post-commit auto-rebuild
/understand-chat <question>          # ask anything in plain English
/understand-explain src/auth/login.ts # deep-dive a specific file
/understand-diff                     # impact of current changes
/understand-domain                   # business domain view
/understand-onboard                  # generate onboarding guide
```

**When to use**
- "How does the payment flow work?" → `/understand-chat`
- Before a PR → `/understand-diff`
- New team member → `/understand-onboard`
- Understanding business logic → `/understand-domain`

---

## code-review-graph

**Role**: AST-level call graph — who calls what, inheritance, test coverage. Integrated via MCP.

**Auto-update**: on every file edit and git commit — no manual action needed.

**MCP workflow templates**
```
review_changes      # review current changes
pre_merge_check     # safety check before merge
architecture_map    # structural impact view
debug_issue         # trace a bug through the call graph
onboard_developer   # codebase tour for new devs
```

**MCP tools**
```
query_graph_tool           # search the graph
semantic_search_nodes_tool # semantic search
detect_changes_tool        # what changed since last review
```

**When to use**
- "Who calls function Y?" → `query_graph_tool`
- Before any PR merge → `pre_merge_check`
- Debugging a regression → `debug_issue`

---

## Staleness check (run at session start)

```bash
# Last commit date
git log -1 --format=%ci

# Compare with graph file modification dates:
# graphify-out/GRAPH_REPORT.md
# .understand-anything/knowledge-graph.json
```

If a graph is older than the last commit → rebuild before using it.

---

## Token budget rules

| Action | Do |
|---|---|
| Session start | Read `GRAPH_REPORT.md` only |
| Need business context | `/understand-chat` |
| Need call relationships | `query_graph_tool` |
| Raw file search | Last resort only |
| Context at 60% | `/compact` |
| New independent task | `/clear` |
