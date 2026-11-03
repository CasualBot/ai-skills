---
name: delivery-report
description: Build and refresh an evidence-based delivery report of a person's work (product owners, developers, QA, designers, tech leads) when the tools they use are unknown. Use when someone asks for a delivery report, work record, impact summary, performance-review evidence, CV highlights, or "what have I delivered", or wants to refresh an existing one. Discovers available tools first, never assumes Jira, Bitbucket or GitHub, and works read-only.
---

# Delivery Report

Build a readable, evidence-based record of what someone delivered, how much, and with what impact, then make it easy to refresh later. Work read-only unless the user says otherwise.

## Rules

- Never invent or estimate numbers. Every figure needs a source (tool, query, date). If a figure is uncertain, label it an estimate and say how it was derived.
- Anything unverifiable goes under "Not counted", never into the totals.
- Credit other people's work as theirs. Lead with outcomes, not activity. Don't overclaim.
- Don't read private messages or personal data beyond what the report needs. Never copy secrets, credentials, tokens or customer details into the report.
- Ask only what you can't discover yourself, in one short batch at a time.

## Inputs (ask if not given)

- **Role:** product owner, developer, QA, designer, tech lead, other.
- **Period:** for example "last 6 months" or "since 2025-02-01".
- **Audience:** the user, their manager, a performance review, a CV.
- **Output format:** document, slide, web page or Markdown.

If a previous report exists, read it first and follow "Refreshing" below instead of starting over.

## Step 1: Discover the tools

1. List the tools actually reachable in this session (connectors, MCP servers, CLIs, local folders, browser). State which are available and which are not.
2. Ask the user which of these they use for their work, in plain language, and wait for the answer:
   - Planning: Jira, Linear, Azure DevOps, Asana, Trello, spreadsheets
   - Code: Bitbucket, GitHub, GitLab, local git repositories
   - Docs: Confluence, Notion, Google Docs, SharePoint
   - Design and research: Figma, Miro, survey tools
   - Quality and release: test tools, CI/CD, release notes, incident tools
   - Communication: Teams, Slack, email (meeting notes and decisions only)
3. For each tool named, say whether it can be read now. If not, say what access or setup is missing and the simplest way to get it ("connect X", "export a CSV", "paste a list"). Always offer a manual fallback so the user is never blocked.

## Step 2: Pick what to measure

From the role and the available tools, propose 6 to 10 measures and ask the user to confirm. Examples:

- **Developers:** merged pull requests, repositories touched, reviews done, issues closed, releases shipped.
- **Product owners:** features or epics delivered, tickets written and accepted, decisions made, launches, stakeholder requests handled.
- **QA:** test cases written, defects found and verified, releases signed off.
- **Anyone:** documents authored, projects led, people mentored or onboarded, incidents handled.

Only count what can be shown with evidence.

## Step 3: Collect

Gather evidence for the period. For each figure, record the source, the query or filter used, and the date collected. Count merged or accepted work only, not work still in review. List everything that couldn't be verified under "Not counted".

## Step 4: Build the report

Produce one readable page in the chosen format with:

- **At a glance:** 8 to 12 headline numbers in 2 or 3 groups (for example Delivery, Leadership, Quality).
- **Themes:** 4 to 8 pieces of work, each with the period, what was done, the outcome, and a one-line summary reusable in a CV or review.
- **Where the work landed:** a small chart or table by project, product or repository.
- **Links** to the underlying tickets, pull requests or documents where possible.
- **Method note:** sources, what was excluded, and the last refresh date, kept low-key at the bottom.

Write in plain language in the user's voice.

## Step 5: Make it refreshable

Save the report where the user can find it. Also record, in the report or beside it:

- the date of the last refresh,
- the exact sources and queries used for every figure,
- anything listed under "Not counted" and why.

Offer to set up a recurring refresh if the user's tools allow it.

## Refreshing

1. Read the existing report and its recorded sources and last refresh date.
2. Collect only what is new since that date, using the same sources and queries.
3. Update the numbers, themes and charts, and the refresh date.
4. Say what changed since the last version.

## Start

Begin with Step 1. Report which tools are reachable, then ask the user which of the listed tools they actually use.
