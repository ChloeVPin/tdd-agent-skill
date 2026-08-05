# Changelog

This project uses [Semantic Versioning](https://semver.org/) and the
[Keep a Changelog](https://keepachangelog.com/) format.

## [2.0.0] - 2026-08-05

This release rebuilds the skill. It adds an evidence base and three sections that address
failures specific to agents.

### Added

- **Evidence table and reference file.** Six empirical claims, each with a citation, the design
  of the study, and a statement of its limits. See
  `skills/test-driven-development/references/evidence.md`.
- **Step 0: Find the Test Commands.** The agent finds the real test command before it writes
  code. The CI configuration is the authority. This replaces the hardcoded commands in earlier
  versions.
- **Prevent Reward Hacking.** A list of prohibited actions and a holdout-test honesty check.
  This section addresses measured behaviour in coding models, which hardcode expected values
  and exit test harnesses early to fake success.
- **Prove That the Tests Are Real.** A manual mutation check that takes approximately 30
  seconds. A table of mutation tools for five ecosystems.
- **Select the Test Level.** Guidance on unit, integration, and end-to-end tests, with size
  defined by the resources that a test uses.
- **Write Tests That Survive a Refactor.** Rules on state against interactions, DAMP against
  DRY, an order of preference for test doubles, and determinism.
- **A completion gate of eleven items.** Each item refers to an observation, not to a belief.
- Repository documentation: `README.md`, `docs/INSTALL.md`, `docs/USAGE.md`, `docs/DESIGN.md`,
  and `docs/STYLE.md`.

### Changed

- **All text now uses ASD-STE100 Simplified Technical English.** Short sentences, the active
  voice, one instruction in one sentence, and a controlled vocabulary. There are no emoji and
  no em dashes. The reason is technical. An agent reads this file as instructions, and
  ambiguous prose produces ambiguous behaviour.
- **Coverage is demoted.** Earlier versions treated coverage as a measure of quality. Coverage
  correlates only weakly with fault detection when suite size is controlled. The skill now
  directs the agent to mutation checks.
- **The rationalisation table gained four entries.** The new entries answer arguments about
  coverage and about flaky tests.
- **The red flags list now includes agent-specific failures.** Examples: a default test command
  that the agent did not verify, and a report of success without the output of the runner.
- **The section on delegation now requires the output of the test runner in the summary of the
  subagent.** A summary is a self-report. The output is evidence.
- The `author` field is now `chloevpin`.

### Removed

- Hardcoded `pytest` and `npm test` commands in the examples of the main cycle.
- The advice that permitted a hardcoded value to survive to a commit. The skill now names that
  action as reward hacking.

## [1.1.0] - Earlier

The version that Hermes Agent shipped, adapted from
[obra/superpowers](https://github.com/obra/superpowers).

### Contents

- The RED, GREEN, REFACTOR cycle with mandatory verification steps.
- The Iron Law: no production code without a failing test first.
- A section on vertical slices against horizontal slices.
- A table of rationalisations with eleven entries.
- A list of red flags.
- A verification checklist of eight items.
- Integration notes for the `terminal` tool and for `delegate_task`.
