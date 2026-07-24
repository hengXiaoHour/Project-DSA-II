# Project-DSA-II — Cross-Session Context

- **Project**: RUPP Campus Navigation (Smart Building Mapping and Navigation System)
- **Stack**: Python 3 (Graph, Tree, Hash Table)
- **Group**: Group 1 — Heng Hour (Leader), Heng Pengly, Yos Sak, Han KimHeng, Sem VatanakPanha
- **Topic**: Smart Building Mapping and Navigation System for RUPP Campus 1 Using Graphs, Trees, and Hash Tables

## Key Files

- `docs/ARCHITECTURE.md` — System architecture (Graph + Tree + Hash)
- `docs/G1-PBLw2.docx.md` — Problem statement and system design

## Session History

### 2026-07-24 — Full OpenCode bootstrap: skills, MCP, cross-session memory, workflow enforcement
- **Goal**: Complete the OpenCode agent environment with automated context retrieval, workflow discipline, subagent orchestration, scaffold guards, vision/UI testing, and doc auto-sync
- **Done**:
  - Created `session-start` skill (auto-retrieves claude-mem + all docs at session start, proposes plan)
  - Created `dev-workflow` skill (Scout → Architect → Builder phase enforcement)
  - Created `subagent-orchestrator` skill (delegates to explore/general/vision/UI subagents)
  - Created `scaffold-guard` skill (prevents files that break directory structure)
  - Created `test-cleaner` skill (deletes stale tests before loop test)
  - Created `vision-evaluator` skill (screenshot review via Playwright + Read tool)
  - Created `ui-tester` skill (interactive UI flow testing via Playwright)
  - Wired all 12 skills into `global-instructions.md` as agent directives
  - Fixed `export.js` to use opencode-bootstrap path and correct DB schema
  - Stored 7 initial memories in claude-mem (2 global + 5 project)
  - Exported memories to backup files
  - Pushed all to `hengXiaoHour/opencode-bootstrap` on GitHub
- **Files changed**: global-instructions.md, export.js, test-loop/SKILL.md, + 7 new skill dirs
- **Decisions**: Skills load on-demand via `skill` tool; global-instructions forces session-start at init; dev-workflow gates every feature; scaffold-guard prevents structural drift
- **Pending**: Implement core data structures (Graph, Tree, Hash Table) for RUPP Campus Navigation
