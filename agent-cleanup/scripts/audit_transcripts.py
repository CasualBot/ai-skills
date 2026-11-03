#!/usr/bin/env python3
"""Measure how Claude Code spends tool calls, using your local session transcripts.

    python audit_transcripts.py [--sessions 80] [--root ~/.claude/projects]

Prints: calls per tool, which tools fill the context most, image reads and re-reads,
fixed sleeps, shell commands that duplicate a dedicated tool, help lookups, repeated
skill/tool loads, the busiest sessions, and per-session minutes from first to last call.
Read-only: it never changes a transcript.
"""
import argparse
import collections
import glob
import json
import os
import re
from datetime import datetime

IMAGE = re.compile(r"\.(png|jpe?g|gif|webp)$", re.I)
SLEEP = re.compile(r"\bsleep (\d+)|Start-Sleep\s+(?:-Seconds\s+)?(\d+)")
READ_LIKE = re.compile(r"^\s*(cat|head|tail|sed -n)\b")
SEARCH_LIKE = re.compile(r"^\s*(grep|rg|find|ls)\b")
HELP = re.compile(r"(--help\b|\bhelp\b)")


def long_path(path):
    path = os.path.abspath(path)
    if os.name == "nt" and len(path) >= 250:
        return "\\\\?\\" + path
    return path


def timestamp(entry):
    value = entry.get("timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def load(path):
    entries = []
    with open(long_path(path), encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def audit(files):
    calls = collections.Counter()
    result_chars = collections.Counter()
    shell = collections.Counter()
    sleeps = []
    image_reads = image_rereads = 0
    repeat_loads = 0
    sessions = []
    for path in files:
        entries = load(path)
        names = {}
        seen_images = collections.Counter()
        seen_loads = collections.Counter()
        session_calls = 0
        times = [t for t in (timestamp(e) for e in entries) if t]
        for entry in entries:
            content = (entry.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "tool_use":
                    name = item.get("name", "?")
                    args = item.get("input") or {}
                    names[item.get("id")] = name
                    calls[name] += 1
                    session_calls += 1
                    if name == "Read" and IMAGE.search(args.get("file_path", "")):
                        image_reads += 1
                        seen_images[args["file_path"]] += 1
                    if name in ("Skill", "ToolSearch"):
                        seen_loads[json.dumps(args, sort_keys=True)] += 1
                    if name in ("Bash", "PowerShell"):
                        command = args.get("command", "")
                        first = command.strip().split("\n")[0]
                        simple = not re.search(r"[|;&]", first)
                        if simple and READ_LIKE.match(first):
                            shell["cat/head/tail/sed (Read would do)"] += 1
                        if simple and SEARCH_LIKE.match(first):
                            shell["grep/find/ls (Grep/Glob would do)"] += 1
                        if HELP.search(command):
                            shell["--help / help lookups"] += 1
                        if re.search(r"\bgit (status|log|diff)\b", command):
                            shell["git status/log/diff"] += 1
                        for match in SLEEP.finditer(command):
                            sleeps.append(int(match.group(1) or match.group(2)))
                elif item.get("type") == "tool_result":
                    body = item.get("content")
                    size = len(body) if isinstance(body, str) else len(json.dumps(body or []))
                    result_chars[names.get(item.get("tool_use_id"), "?")] += size
        image_rereads += sum(n - 1 for n in seen_images.values() if n > 1)
        repeat_loads += sum(n - 1 for n in seen_loads.values() if n > 1)
        minutes = (max(times) - min(times)).total_seconds() / 60 if len(times) > 1 else 0
        sessions.append((session_calls, round(minutes), os.path.basename(path)[:8]))
    return calls, result_chars, shell, sleeps, image_reads, image_rereads, repeat_loads, sessions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sessions", type=int, default=80)
    parser.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    args = parser.parse_args()
    files = glob.glob(os.path.join(args.root, "*", "*.jsonl"))
    files = sorted(files, key=lambda p: os.stat(long_path(p)).st_mtime, reverse=True)[: args.sessions]
    calls, result_chars, shell, sleeps, images, rereads, reloads, sessions = audit(files)
    total = sum(calls.values())
    print(f"{len(files)} sessions, {total} tool calls\n")
    print("Calls per tool:")
    for name, n in calls.most_common(20):
        print(f"  {n:6}  {n * 100 / max(total, 1):4.1f}%  {name}")
    print("\nContext filled by tool results (k chars; images count as base64):")
    for name, n in result_chars.most_common(10):
        print(f"  {n // 1000:8}  {name}")
    print(f"\nImage reads: {images} ({rereads} re-reads of an image already seen that session)")
    print(f"Fixed sleeps: {len(sleeps)} commands, {sum(sleeps) // 60} minutes in all")
    print(f"Repeated Skill/ToolSearch loads in one session: {reloads}")
    print("\nShell habits:")
    for kind, n in shell.most_common():
        print(f"  {n:6}  {kind}")
    print("\nBusiest sessions (calls, minutes, id):")
    for row in sorted(sessions, reverse=True)[:8]:
        print(f"  {row}")


if __name__ == "__main__":
    main()
