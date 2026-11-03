---
name: agent-cleanup
description: "Clean up a Claude Code setup that has grown slow or noisy: measure what loads, prompts and repeats, then cut the waste without losing behaviour the user relies on. Use when sessions feel slow, context fills early, approvals interrupt constantly, or multi-step workflows take too long. Not for rewriting a single prompt or skill."
---

# Agent cleanup

A Claude Code setup grows one instruction, skill, server, hook and workflow at a time. Each one made sense when it was added; together they slow every session. This skill cleans it up in a fixed order:

1. **Discover** what this user actually has.
2. **Measure** what it costs.
3. **Cut** what repeats, is unused or is done the expensive way.
4. **Re-measure** to prove the cut.

**Assume nothing about the setup.** Users differ in which instruction files, skills, plugins, MCP servers, hooks, CLIs, browsers or agent workflows they have. Every step below starts with "if it exists"; skip the parts that don't apply and say so in one line.

**Ground rules**
- Back up any file before editing it.
- Only change files that are the user's own: their global config, their personal settings and skills, and projects they alone maintain. A `CLAUDE.md` or `AGENTS.md` committed to a repository other people work in affects all of them, so point out the issue rather than trimming it.
- A pure fix (a crashing hook, a reference to something that no longer exists) needs no discussion. A cut that changes behaviour is a decision: present it with a recommended default and apply it on the user's OK.
- Keep a short written record of the findings, the decisions and the before/after numbers somewhere the user keeps notes.

## 1. Discover

List what is there before judging it:
- **Always-loaded instructions:** global and project `CLAUDE.md` files and everything they `@import`, `.claude/rules/` files without `paths:`, `AGENTS.md`, output styles, and anything a SessionStart hook injects.
- **On-demand capabilities:** skills (user, project and plugin), enabled plugins, MCP servers and their scopes, custom agents and slash commands.
- **Guardrails:** hooks in every `settings.json` (user, project, local) and the permission allow, ask and deny lists.
- **Workflows:** any repeatable multi-step or multi-agent process the user runs (reviews, builds, triage, reports), and the CLIs and services those depend on.
- **History:** the session transcripts in `~/.claude/projects/` are the evidence for everything below.

## 2. Measure

| Area | What to measure |
|---|---|
| Always-loaded context | Characters or tokens loaded before the first message (`/context` in a fresh session, and file sizes). If a hook injects text, run it by hand and measure its output, including whether it gets truncated. |
| Capability listings | How many skills, agents and tools are listed every session, and the total length of their descriptions. |
| Use | When each skill, MCP server, plugin and agent was last used (search the transcripts for its name). |
| Guardrails | How often each hook asks, blocks or errors, and which commands trigger permission prompts most. |
| Habits | Run `scripts/audit_transcripts.py`: calls per tool, which tool results fill the context most, repeated reads of the same expensive output, fixed waits, shell commands that duplicate a dedicated tool, repeated loads, and the busiest sessions. |
| Workflows | For each repeatable workflow, time one real run from its transcript: when each step starts and ends, what waits on what, and how long until the user gets a result. |

## 3. Cut, area by area

### Always-loaded context
Everything here is paid on every turn of every session.
- **Write it for the agent:** short imperative rules, grouped by theme. Move history, rationale and examples to a linked note.
- **Only global rules load every session.** A rule that matters to one workflow moves into that workflow's skill or agent.
- **One line per rule**, with no story. If rules live in separate files, give each a short one-line form to load.
- **Delete rules that a later rule replaced**, rather than keeping both.
- **Cap the size.** If something injects context, give it a limit and a check that fails over it. Watch for silent truncation: a harness may load only a preview of an oversized injection.

### The root instruction file: an index, not a manual
The main `CLAUDE.md` (global or project) loads in full every session, so it should stay a short index that points to the detail. A documentation strategy for agents:
- **The root file holds only what applies to almost every task:** hard rules, where things live, and a line per topic saying where to read more and when. Aim well under the documented 200 lines; a few KB is plenty.
- **Detail lives in topic files the agent reads when needed.** Write a plain-text pointer such as "Before touching the billing service, read `docs/agents/billing.md`". That costs one line until the agent needs it.
- **`@path` imports are not a saving.** Imported files load at start with the file that imports them, so they cost the same as pasting the text in. Use them only to share one source between files (for example `@AGENTS.md`), never to shrink context.
- **Let the harness load by location:**
  - A `CLAUDE.md` in a subdirectory loads only once the agent works on files in that directory. Put area-specific rules there, not in the root.
  - Rules in `.claude/rules/*.md` (or `~/.claude/rules/`) with `paths:` frontmatter load only when a matching file is read or edited. Use them for rules tied to file types or folders.
  - Rules files without `paths:` load at start like the root file, so they don't save anything.
- **One source of truth for several agents.** When a repo has `AGENTS.md` for other tools, keep `CLAUDE.md` to an `@AGENTS.md` import plus any Claude-only lines, rather than two diverging copies. Prefer the import to a symlink on Windows, where a symlink can check out as a plain text file.
- **Notes for human maintainers** go in block-level HTML comments (`<!-- … -->`). They're stripped before loading, so they cost nothing.
- **Check what loads:** `/context` lists the memory files loaded in a session, and `/memory` shows where they live. `/doctor` warns about oversized files.

### Capabilities (skills, plugins, agents, MCP servers)
- **List only what is used**, and keep the rest available unlisted or as plain files. Every listed description costs tokens in every session.
- **Short descriptions:** when to use it, the words that should trigger it, and when not to (naming the alternative).
- **Split big skills:** a short main file that says which reference file to read at which step.
- **Take only what you use** from large bundles, and disable the rest.
- **Remove MCP servers** unused for weeks, and scope project-specific ones to their project. Where a CLI does the same job, prefer it: no always-loaded tool schemas and no extra process. Check servers that start processes or containers for leftovers.
- **Fix dead references:** a step that calls something removed or disabled fails silently.

### Guardrails (hooks and permissions)
- **Fix erroring hooks first.** Check transcripts for hook errors; one bug often accounts for most of them (on Windows, look for long-path failures).
- **A hook should ask or block only where the risk is real.**
  - Let clearly disposable targets through (temp, scratch and cache folders).
  - Keep asking for anything ambiguous: wildcards, variables, root folders, mixed targets.
  - Throttle hooks that do slow work, and make them handle the user's real environment (git worktrees, long paths, other shells).
- **Allowlist the read-only commands that prompt most**: the get, list, query, view and help forms of the CLIs the user runs. Never allowlist interpreters, shells, package runners, wildcard task runners, or anything that writes, deletes, pushes or posts.
- **Run each check at the right stage.** A gate that runs everything at one moment (every test before every action) costs more than running each check where it belongs. Agree the stages with the user.

### How work gets done
Agree a default with the user and write it down as a short always-loaded rule:
- **For a requested change:** find what to change, change it, run the checks that cover just that change, and say in a line what changed and what wasn't checked.
- **Extras only when asked:** plans, write-ups, commits, full test suites, extra verification passes and documentation.
- **Stay in scope:** suggest improvements, don't make them unasked.

### Habits (from the transcript audit)
Each pattern is generic, though the tools behind it differ by user:
- **Repeated expensive reads.** Reading the same large output again (images, big files, long logs, large API responses). Read once, note what mattered, and use a cheaper text form to check state when one exists.
- **Fixed waits.** Sleeping for a set time and then checking. Wait on the condition instead (an output, a file, a status, a completion notification), or run the work in the background.
- **Shell duplicates of dedicated tools.** Mostly harmless; act only when they are large or repeated.
- **Repeated lookups.** The same help page, skill or tool schema loaded again and again. Put the answer in the skill or rule that needs it.
- **Unbounded autonomous runs.** Loops or goal modes with no stop condition rack up calls re-checking state. Give them a stop condition and a time or call budget.
- **Long commands in the foreground.** Run them in the background so the session isn't blocked.

### Workflows (multi-step and multi-agent)
Time a real run, then cut from the longest phase down:
- **Run only the steps or agents this input needs.** Pick them by what changed, not "all of them every time".
- **Use a script for mechanical checks.** If a check has a deterministic answer (does this quoted text exist at this location, does this file parse), a script is faster and more consistent than an agent.
- **Verify only what matters:** one independent check for each high-stakes finding, not several rounds for every finding.
- **Do each piece of work once.** Agents return findings; the final wording is drafted once, for what survives.
- **Don't idle.** Start work that doesn't depend on a slow step (an install, a build, a fetch) straight away, and cache slow steps that repeat.
- **Give open-ended steps a scope and a time box**, such as how much to explore and when to stop.
- **Orchestrators route; agents work.** The coordinating agent reads only what it needs and doesn't redo the agents' work.
- **One output for the human, at the decision point:** what was done, the evidence, what to weigh, and what happens next. Not a log of every step. Publish it once.
- **Use the right container for each role.** Short, read-only roles fit lightweight subagents; roles the user wants to watch or steer get their own session.
- **Route on completion signals**, not on files appearing, and use a fresh scratch space per run so leftovers from an earlier run can't mislead it.

## 4. Re-measure and record

- Repeat the step 2 measurements, and time one real run of each workflow you changed.
- Record a before/after table: always-loaded size, listed capabilities and their description size, servers, hook errors, prompts per session, repeated expensive reads, waiting time, and workflow minutes by phase.
- Save each behavioural decision as a short rule where the agent will see it, and remove the rules it replaces, so the cleanup survives new sessions.
