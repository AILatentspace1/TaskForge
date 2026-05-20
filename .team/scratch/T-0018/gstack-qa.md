SMOKE_OK

## QA Evidence

### DoD Verification

1. `retro-has-audit-section`: `grep -c audit .team/prompts/team-retro.claude.md` → 4 (pass)
2. `retro-has-pattern-section`: `grep -c pattern .team/prompts/team-retro.claude.md` → 4 (pass)
3. `prompt-valid-markdown`: `head -1 .team/prompts/team-retro.claude.md | grep -c "#"` → 1 (pass)

### Diff Summary

```
prompts/team-retro.claude.md — STEP 2 增加 audit 上下文加载 + daily report 增加 audit/pattern 段落
.team/prompts/team-retro.claude.md — 同步
```
