APPROVED

## Scope Check: CLEAN

变更范围完全在 allowed_paths（prompts/**）和 runtime_dir（.team/）内。

## Plan Completion Audit

- **intent**: DONE — 增加 audit 和 pattern 检测
- **scope**: DONE — 仅修改 retro prompt
- **likely files**: DONE — prompts/team-retro.claude.md
- **test/eval approach**: DONE — DoD exec checks
- **risks and rollback**: DONE — 单 commit 可 revert

## Production-risk Findings

无。仅修改 prompt 文本。

## Test/Eval Gaps

无。DoD 3 项全部通过。

## Required Fixes

无。
