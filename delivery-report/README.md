# Delivery Report

A skill that helps you build a record of the work you have delivered, and keep it up to date.

You tell your AI assistant what you do and what period you want to cover. It works out which tools it can read, collects the evidence, and writes a report you can use for a review, a CV, or a chat with your manager. Every number in the report comes with a source, so you can check it.

## Who it's for

Anyone who wants to show what they have delivered: developers, product owners, QA, designers, tech leads. You don't need to use any particular tools. The skill starts by finding out what you have.

## What you get

- A short block of headline numbers, grouped into two or three themes
- A handful of pieces of work, each with when it happened, what you did, and what came of it
- A chart or table showing where your work landed
- Links back to the tickets, pull requests or documents behind the numbers
- A note at the bottom saying where the figures came from and what was left out

## How to use it

1. Put the `delivery-report` folder where your assistant looks for skills. For Claude Code, that is `.claude/skills/delivery-report/` inside your project, or in your home folder to use it everywhere.
2. Start a chat and ask something like "Build me a delivery report for the last six months."
3. Answer the questions it asks. It will tell you which of your tools it can already read, and what to do if one is missing.
4. Check the list of things it plans to count, and say yes or change it.
5. Read the report. Anything it couldn't prove is listed separately instead of being counted.

## Keeping it up to date

Ask your assistant to refresh the report. It reads the old report, collects only what has happened since the last refresh, and updates the numbers. It will also tell you what changed.

## What it will and won't do

- It only reads. It doesn't change anything in your tools unless you ask.
- It never makes up numbers. If it can't prove something, it leaves it out and says so.
- It doesn't read your private messages or copy passwords, keys or customer details into the report.
- It credits other people's work to them.

## If a tool can't be reached

The skill tells you what's missing and the simplest way to fix it, such as connecting the tool, exporting a spreadsheet, or pasting a list. You are never stuck.

## Files

- `SKILL.md`: the instructions your assistant follows
- `README.md`: this page
