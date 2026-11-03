# agent-cleanup

A Claude Code skill that cleans up a setup that has grown slow or noisy. It works through four steps:

1. **Discover** what you have.
2. **Measure** what it costs.
3. **Cut** the waste.
4. **Re-measure** to prove it.

It covers always-loaded instructions, skills, plugins, MCP servers, hooks, permission prompts, everyday tool habits and multi-step agent workflows. It doesn't assume any particular tools: each step applies only if you have that thing.

## Install

Copy the folder into your skills directory:

```bash
cp -r agent-cleanup ~/.claude/skills/
```

Then ask Claude something like "clean up my Claude Code setup" or "audit why my sessions are slow", or invoke the skill by name.

## What's inside

| File | Purpose |
|---|---|
| `SKILL.md` | The procedure Claude follows |
| `scripts/audit_transcripts.py` | Read-only report of tool use from your local session transcripts |

Run the audit script on its own:

```bash
python ~/.claude/skills/agent-cleanup/scripts/audit_transcripts.py --sessions 80
```

It needs only the Python 3 standard library.

## Do

- **Measure before cutting.** Every change should trace back to a number: size, count, minutes or errors.
- **Back up each file before editing it**, and keep the before/after numbers.
- **Approve behaviour changes one at a time.** Claude should present each cut that changes how it works as a decision with a recommended default. Pure fixes (a crashing hook, a dead reference) can go straight in.
- **Keep the root `CLAUDE.md` a short index.** Put detail in topic files it points to, in subdirectory `CLAUDE.md` files, or in path-scoped `.claude/rules/`.
- **Write each decision down as a short rule**, and delete the rule it replaces, so the cleanup survives new sessions.
- **Re-run the measurements afterwards**, and time one real run of any workflow you changed.

## Don't

- **Don't trim instruction files that other people maintain**, such as a `CLAUDE.md` or `AGENTS.md` committed to a shared repository. Your changes would affect everyone who works in it. Suggest the change to its maintainers instead.
- **Don't use `@imports` to shrink context.** Imported files still load at start.
- **Don't allowlist anything that can run arbitrary code or write**: interpreters, shells, package runners, wildcard task runners, or commands that delete, push or post. Allowlist only read-only commands.
- **Don't remove a safety hook outright** because it prompts a lot. Narrow it so it asks only where the risk is real.
- **Don't delete skills, servers or rules on a hunch.** Check the transcripts for when they were last used.
- **Don't raise a size cap to make a check pass.** Move a rule out instead.

## Privacy

- Your transcripts (`~/.claude/projects/`) can contain anything from past sessions, including secrets. `audit_transcripts.py` only reads them and prints counts, tool names, character totals and short session IDs. It never prints commands, file contents or tool output, and it makes no network calls.
- **Before sharing the script's output, check the tool-name list.** MCP tool names (`mcp__<server>__<tool>`) can reveal server names you may not want public.

## Requirements

- Claude Code, with session transcripts under `~/.claude/projects/` (the default).
- Python 3.9+ for the audit script.
- Works on macOS, Linux and Windows. The script handles Windows long paths.
