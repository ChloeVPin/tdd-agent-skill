<div align="center">

<img src="assets/logo-256.png" alt="TDD Agent Skill logo" width="128" height="128">

# TDD Agent Skill

**A research-backed test-driven development skill for AI coding agents.**

Makes Claude Code, OpenAI Codex, and any `SKILL.md` agent prove their work instead of
reporting that the work is complete.

[![CI](https://img.shields.io/github/actions/workflow/status/ChloeVPin/tdd-agent-skill/validate.yml?style=flat&logo=githubactions&logoColor=white)](https://github.com/ChloeVPin/tdd-agent-skill/actions/workflows/validate.yml)
[![Licence](https://img.shields.io/badge/licence-MIT-3DA639?style=flat&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ChloeVPin/tdd-agent-skill?style=flat&logo=semanticrelease&logoColor=white)](https://github.com/ChloeVPin/tdd-agent-skill/releases/latest)
[![Stars](https://img.shields.io/github/stars/ChloeVPin/tdd-agent-skill?style=flat&logo=github&logoColor=white)](https://github.com/ChloeVPin/tdd-agent-skill/stargazers)
[![Install](https://img.shields.io/badge/install-npx_skills_add-000000?style=flat&logo=npm&logoColor=white)](#install)
[![Format](https://img.shields.io/badge/format-Agent_Skills-8A63D2?style=flat&logo=anthropic&logoColor=white)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
[![Style](https://img.shields.io/badge/style-ASD--STE100-0A7BBB?style=flat&logo=readthedocs&logoColor=white)](https://www.asd-ste100.org/)

[Install](#install) · [Why This Exists](#why-this-exists) · [Evidence](skills/test-driven-development/references/evidence.md) · [FAQ](#frequently-asked-questions) · [Docs](docs/)

</div>

---

## What This Is

This repository contains one Agent Skill for test-driven development. The skill teaches an AI
coding agent to write the test first, to run it, and to see it fail before it writes the
implementation. The gates are hard. The agent cannot pass them because it believes that the
code is correct.

The skill works with Claude Code, OpenAI Codex, GitHub Copilot in VS Code, Hermes Agent, and
any tool that reads the `SKILL.md` Agent Skills format.

```
skills/test-driven-development/
├── SKILL.md                  the skill itself
├── assets/
│   └── logo.png              the project logo
└── references/
    └── evidence.md           full citations, study designs, and limits
```

## Why This Exists

Most published TDD skills give the same instructions. Write the test first. Watch it fail.
Keep the code minimum. Those instructions are correct, and they are not sufficient for an
agent.

Published TDD skills have four gaps. This skill closes them.

| Gap | Effect on an agent | The fix in this skill |
|---|---|---|
| No evidence for the rules | The agent accepts the argument "TDD is dogmatic, I am being pragmatic" and stops | An evidence table with six studies, and a reference file that states the limits of each one |
| A hardcoded test command such as `npm test` | The agent runs the wrong command, or invents one, in any repository that is not JavaScript | Step 0 finds the real command. The CI configuration is the authority |
| No defence against reward hacking | The agent hardcodes values, weakens assertions, or exits the harness early to get a green result | A list of prohibited actions and a holdout-test honesty check |
| Coverage treated as the goal | The agent optimises a number that correlates weakly with defect detection | Coverage is demoted with data. A 30-second manual mutation check replaces it |

## The Core Idea

An agent writes code and tests faster than a person reads them. Speed is not the limit. Proof
is the limit.

Each rule in this skill changes "this looks correct" into "I saw the test change from fail to
pass".

```
 RED ---> VERIFY RED ---> GREEN ---> VERIFY GREEN ---> REFACTOR
 write    run it, see     minimal    run focused and    clean up,
 one      the correct     code       then full suite,   stay green
 test     failure                    output is clean
```

Each arrow is a gate. The agent passes a gate only when it has seen the output.

## Install

### Recommended: the skills CLI

```bash
npx skills add ChloeVPin/tdd-agent-skill
```

The CLI finds the agents that you have installed. Then it puts the skill in the correct
directory for each one. It supports Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Cline,
OpenCode, and more than 30 other agents.

Install for one agent only:

```bash
npx skills add ChloeVPin/tdd-agent-skill -a claude-code
```

Install without a prompt, for a script or for CI:

```bash
npx skills add ChloeVPin/tdd-agent-skill -a claude-code -g -y
```

The CLI needs Node.js 22.20 or newer. Read the
[skills CLI documentation](https://github.com/vercel-labs/skills) for the other options.

### Read the skill before you install it

A skill tells an agent what to do on your computer. Read it first. This rule applies to this
skill and to every other skill.

```bash
npx skills use ChloeVPin/tdd-agent-skill --skill test-driven-development
```

You can also read [SKILL.md](skills/test-driven-development/SKILL.md) in your browser.

### Manual installation with git

Use this method if you do not have Node.js, or if you want to control the destination.

```bash
git clone https://github.com/ChloeVPin/tdd-agent-skill.git
```

Then copy the directory into the skills directory of your agent.

| Agent | Destination |
|---|---|
| Claude Code | `~/.claude/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| GitHub Copilot in VS Code | `.github/skills/` |
| Hermes Agent | `~/.hermes/skills/software-development/` |

```bash
cp -R tdd-agent-skill/skills/test-driven-development ~/.claude/skills/
```

The skill has no dependencies and it runs no scripts.

Read [docs/INSTALL.md](docs/INSTALL.md) for the verification steps and for the layout of each
tool.

## Evidence Summary

The skill makes six empirical claims. Each one has a citation, a study design, and a statement
of its limits in [references/evidence.md](skills/test-driven-development/references/evidence.md).

| Claim | Source |
|---|---|
| TDD decreased pre-release defect density by 40 to 90 per cent in four industrial teams, for 15 to 35 per cent more time at the start | Nagappan, Maximilien, Bhat, and Williams. *Empirical Software Engineering* 13(3), 2008 |
| Developers with AI tools took 19 per cent longer while they believed that they were 20 per cent faster | METR randomised controlled trial, 2025. arXiv:2507.09089 |
| Coverage correlates only weakly with fault detection when suite size is controlled | Inozemtseva and Holmes. ICSE 2014 |
| Mutation score correlates with real fault detection, independently of coverage | Just and others. FSE 2014 |
| Approximately 16 per cent of Google tests show flakiness, and flaky tests cause most CI state changes | Parry, Kapfhammer, Hilton, and McMinn. ACM TOSEM, 2021 |
| Coding models hardcode test values and exit harnesses early to fake success | Anthropic, 2025. EvilGenie benchmark, arXiv:2511.21654 |

The reference file states where each result is more narrow than the slogan that came from it.
The range of 40 to 90 per cent is one example. It comes from case studies, not from randomised
trials, and the authors record the risk of selection effects.

## Frequently Asked Questions

### Which agents does this skill support?

It supports Claude Code, OpenAI Codex, GitHub Copilot in VS Code, Cursor, Cline, OpenCode,
Hermes Agent, and any tool that reads the `SKILL.md` Agent Skills format. The skill is
Markdown. It has no dependencies and it runs no scripts.

### What is the fastest way to install the skill?

Run `npx skills add ChloeVPin/tdd-agent-skill`. The skills CLI finds the agents that you have
installed and puts the skill in the correct directory for each one. The CLI needs Node.js
22.20 or newer. If you do not have Node.js, clone the repository and copy the directory.

### Is it safe to install a skill?

A skill tells an agent what to do on your computer. Read it before you install it. Run
`npx skills use ChloeVPin/tdd-agent-skill --skill test-driven-development` to print the skill,
or read [SKILL.md](skills/test-driven-development/SKILL.md) in your browser.
[SECURITY.md](SECURITY.md) lists the actions that this skill instructs an agent to do.

### How is this different from other TDD skills?

Other TDD skills give correct instructions for a person. This skill closes four gaps that
appear when an agent follows those instructions. It gives evidence for each rule. It finds the
test command of the repository instead of assuming one. It prohibits the specific actions that
models use to fake a green test suite. It replaces coverage with a mutation check.

### Why does the skill prohibit an increase in code coverage as a goal?

Coverage measures execution. It does not measure assertion. A test with no assertion covers
many lines. Inozemtseva and Holmes measured 31,000 test suites and found that coverage
correlates only weakly with fault detection when suite size is controlled. The skill directs
the agent to a mutation check instead.

### What is reward hacking in a coding agent?

Reward hacking is any action that satisfies the measured goal without the intended work. In a
test harness, it looks like a hardcoded expected value, a special case for the exact input of
the test, a weaker assertion, an added skip, or a call to `sys.exit(0)` that makes the runner
report success. Anthropic and the EvilGenie benchmark have measured these actions in
production coding agents. The skill lists them and prohibits them.

### Does this skill slow the agent down?

Yes, at the start. Four industrial teams measured 15 to 35 per cent more time at the start and
40 to 90 per cent fewer pre-release defects. The trade is more time before the commit against
less debugging after the release.

### Can I use the skill for a language other than Python or JavaScript?

Yes. The cycle is the same in all languages. Step 0 tells the agent to find the test command of
the repository from the manifest, the wrapper scripts, and the CI configuration. The mutation
table covers Python, JavaScript, TypeScript, Java, Go, and Rust.

### Why is the documentation written in this style?

The repository uses ASD-STE100 Simplified Technical English, which is the international
standard for technical documentation. An agent reads these files as instructions. Ambiguous
prose produces ambiguous behaviour. Read [docs/STYLE.md](docs/STYLE.md).

### How do I verify that the skill is active?

Give the agent a small task in a repository that has tests. The skill is active if the agent
finds the test command first, writes one test, runs it, and shows you the failure before it
writes the implementation. Read [docs/INSTALL.md](docs/INSTALL.md).

## Documentation

| Document | Contents |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Installation for each agent, and how to verify it |
| [docs/USAGE.md](docs/USAGE.md) | How to invoke the skill, worked examples, and delegation |
| [docs/DESIGN.md](docs/DESIGN.md) | Why each section exists, and which failure it prevents |
| [docs/STYLE.md](docs/STYLE.md) | The ASD-STE100 writing rules for this repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to propose a change |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [SECURITY.md](SECURITY.md) | How to report a security problem |

## Language Standard

All documents in this repository use ASD-STE100 Simplified Technical English. The rules are
short sentences, the active voice, one instruction in one sentence, and a controlled
vocabulary. There are no emoji and no em dashes.

There is a technical reason for this standard. An agent reads these documents as instructions.
Ambiguous prose produces ambiguous behaviour. Read [docs/STYLE.md](docs/STYLE.md) for the full
rules.

## Credits

The RED, GREEN, REFACTOR structure and the list of rationalisations come from
[obra/superpowers](https://github.com/obra/superpowers), under the MIT licence. The
stack-discovery step follows the approach in
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).

This version adds the evidence base, the anti-reward-hacking section, the mutation checks, and
the ASD-STE100 rewrite.

## Licence

MIT. Read [LICENSE](LICENSE).
