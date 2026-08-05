# Security Policy

## What This Repository Contains

This repository contains Markdown documents only. It has no executable code, no dependencies,
and no build step. The skill runs no scripts.

The one exception is the GitHub Actions workflow in `.github/workflows/validate.yml`. That
workflow validates the documents. It runs only in this repository.

## The Risk to Understand

An Agent Skill is a set of instructions for an AI agent. An agent reads the skill and then acts
on your computer and in your repository.

Read a skill before you install it. This rule applies to this skill and to every other skill.
The text tells the agent what to do. A skill from an unknown author can tell an agent to do
something that you do not want.

This skill instructs an agent to do these actions:

- Read the manifest files, the CI configuration, and the existing tests of your repository.
- Run the test command of your repository.
- Write test files and implementation files.
- Break one line of code on purpose and then undo the change, as a check of test quality.

The skill does not instruct an agent to install software. It proposes a mutation tool and it
tells the agent to ask you first.

## Report a Problem

Report a security problem with GitHub private vulnerability reporting.

1. Open the Security tab of this repository.
2. Select "Report a vulnerability".

Do not open a public issue for a security problem.

Give this information in your report:

- The file and the section.
- The behaviour that an agent produces.
- The reason that the behaviour is a risk.
- The agent and the model that you used, if the report is about behaviour.

## Response

I will confirm the report within seven days. I will give an assessment within 30 days.

## Supported Versions

The most recent release gets fixes. Earlier versions do not.

| Version | Supported |
|---|---|
| 2.0.x | Yes |
| 1.x | No |
