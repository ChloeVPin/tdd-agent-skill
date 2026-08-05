<div align="center">

<img src="assets/logo-256.png" alt="Project logo" width="128" height="128">

# Test-Driven Development for AI Coding Agents

**A research-backed Agent Skill that makes coding agents prove their work.**

[![License: MIT](https://img.shields.io/badge/License-MIT-1f2328.svg?style=flat-square)](LICENSE)
[![Skill Version](https://img.shields.io/badge/skill-v2.0.0-1f2328.svg?style=flat-square)](skills/test-driven-development/SKILL.md)
[![Format: Agent Skills](https://img.shields.io/badge/format-SKILL.md-1f2328.svg?style=flat-square)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
[![English: ASD-STE100](https://img.shields.io/badge/English-ASD--STE100-1f2328.svg?style=flat-square)](https://www.asd-ste100.org/)

[Install](#install) · [Why This Exists](#why-this-exists) · [Evidence](skills/test-driven-development/references/evidence.md) · [Docs](docs/)

</div>

---

## What This Is

This repository contains one Agent Skill. The skill teaches an AI coding agent to use
test-driven development with hard gates that the agent cannot pass on belief alone.

The skill works with Claude Code, Hermes Agent, VS Code, OpenAI Codex, and any tool that reads
the `SKILL.md` format.

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

### Claude Code

```bash
git clone https://github.com/chloevpin/tdd-skill-repo.git
cp -R tdd-skill-repo/skills/test-driven-development ~/.claude/skills/
```

### Hermes Agent

```bash
git clone https://github.com/chloevpin/tdd-skill-repo.git
cp -R tdd-skill-repo/skills/test-driven-development ~/.hermes/skills/software-development/
```

### VS Code

```bash
git clone https://github.com/chloevpin/tdd-skill-repo.git
cp -R tdd-skill-repo/skills/test-driven-development .github/skills/
```

### Any other agent

Copy the `skills/test-driven-development/` directory into the skills directory of your tool.
The skill has no dependencies and runs no scripts.

Read [docs/INSTALL.md](docs/INSTALL.md) for verification steps and for the layout of each tool.

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

## Documentation

| Document | Contents |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Installation for each agent, and how to verify it |
| [docs/USAGE.md](docs/USAGE.md) | How to invoke the skill, worked examples, and delegation |
| [docs/DESIGN.md](docs/DESIGN.md) | Why each section exists, and which failure it prevents |
| [docs/STYLE.md](docs/STYLE.md) | The ASD-STE100 writing rules for this repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to propose a change |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

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
