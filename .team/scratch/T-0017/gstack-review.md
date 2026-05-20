APPROVED

## Scope Check: CLEAN

变更范围完全在 allowed_paths（prompts/**）和 runtime_dir（.team/）内。

## Plan Completion Audit

- **intent**: DONE — 强化上下文加载逻辑
- **scope**: DONE — 仅修改 heartbeat prompt 和同步文件
- **likely files**: DONE — prompts/team-heartbeat.claude.md, .team/prompts/*
- **test/eval approach**: DONE — DoD exec checks
- **risks and rollback**: DONE — 单 commit 可 revert

## Production-risk Findings

无。仅修改 prompt 文本，不影响运行时代码或配置。

## Test/Eval Gaps

无。DoD 3 项全部通过：
- heartbeat-has-context-section: pass (grep -c context = 1)
- planner-has-context-section: pass (grep -c context = 2)
- prompt-valid: pass (head -1 grep "#" = 1)

## Required Fixes

无。
