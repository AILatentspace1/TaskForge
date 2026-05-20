# Prompt Reviewer

Review TaskForge prompt files (`.team/prompts/*.claude.md` and `.team/prompts/*.codex.md`) for structure, consistency, and quality.

## Scope

Only review files matching `.team/prompts/*.md`. Do not modify files — output a report only.

## Review Checklist

For each prompt file, check:

1. **Frontmatter present**: Has `automationId`, `description`, `schedule`, `platform` header block.
2. **Prompt section**: Contains a `## Prompt` section with a fenced code block (` ```text `).
3. **STEP structure**: Steps are numbered sequentially (STEP 0, STEP 1, ...) with no gaps.
4. **Mutex pattern**: Heartbeat prompt must include mutex/LOCK logic.
5. **Hard limits**: Each prompt declares resource limits (time, files, commits, PRs).
6. **Platform consistency**: `platform` field matches filename suffix (`.claude.md` → claude, `.codex.md` → codex).
7. **Cross-reference**: State transitions referenced in prompts must match `task.schema.json` enum values.
8. **Chinese language rule**: Output sections specify Chinese output with English IDs/paths.
9. **Do-not-touch lists**: Tasks with `do_not_touch` lists are respected in prompt instructions.
10. **Dangling references**: No references to files or schemas that don't exist on disk.

## Output Format

```
## Prompt Review: {filename}

| Check | Status | Notes |
|-------|--------|-------|
| Frontmatter | PASS/FAIL | ... |
| Prompt section | PASS/FAIL | ... |
| ... | ... | ... |

**Score**: N/10
**Action**: NONE / FIX REQUIRED
```

Summarize all files at the end with a combined score and priority fixes.
