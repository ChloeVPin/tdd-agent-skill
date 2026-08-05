# Design Notes

This document records the reason for each section of the skill. Each section prevents a
specific failure. If you propose a change, read the relevant entry first.

## The Central Problem

An agent writes code and tests faster than a person reads them. Speed is not the limit. Proof
is the limit.

A published TDD skill written for a person can say "watch the test fail" and stop there. A
person who skips that step feels the risk. An agent does not. An agent produces a plausible
test, a plausible implementation, and a plausible report that all tests pass. Each artefact
looks correct. None of them is evidence.

Each design decision below converts a claim into an observation.

## Why an Evidence Section Exists

**Failure that it prevents.** The agent, or the user, argues that TDD is dogma. The agent
agrees and abandons the method.

The rationalisation table in earlier TDD skills answers this argument with assertion. An
assertion loses against a user who states "we do not have time". A measurement does not.

The evidence table is at the top of the skill, not in an appendix, because the agent must read
it before it reaches the first difficult decision.

**Why the limits are stated.** The reference file records where each study is more narrow than
the slogan that came from it. The range of 40 to 90 per cent comes from four case studies, not
from randomised trials, and the authors record the risk of selection effects.

There is a practical reason for this honesty. A user who checks one citation and finds an
over-claim stops trusting all of them. An accurate weak claim is more useful than an
exaggerated strong one.

**Why the METR result is included.** The METR trial is not about TDD. It is about the gap
between measured performance and perceived performance in the exact human and AI condition in
which this skill runs. It is the strongest available argument for the position that the skill
takes: gate on observed output, not on the feeling that the work is complete.

## Why Step 0 Exists

**Failure that it prevents.** The agent runs `npm test` in a Gradle repository. The command
fails or, worse, it succeeds and runs nothing.

Every published TDD skill that hardcodes a test command is wrong outside one ecosystem. The
skill that this repository started from used `npm test` in each example. The Hermes version
used `pytest`. Both are correct in one language and wrong in all the others.

**Why the CI configuration is the authority.** A repository can contain several test commands.
The manifest can contain a script that nobody uses. The README can be out of date. The command
in the CI configuration is the command that controls merges. It is the true command.

**Why the agent must record both commands.** The inner loop needs a fast command for one test.
The completion gate needs the full suite. An agent that has only the full command runs slowly
and stops verifying RED. An agent that has only the focused command misses regressions.

## Why the Anti-Reward-Hacking Section Exists

**Failure that it prevents.** The agent gets a green suite by dishonest means.

This is the largest gap in published TDD skills. They were written for people. A person who
hardcodes a return value to pass a test knows that they are cheating. An agent does not
experience it that way. The objective "make the suite green" has an honest solution and a
dishonest solution. The dishonest solution is shorter, and nothing in the objective separates
them.

This is measured behaviour, not a theory. Anthropic documented models that call `sys.exit(0)`
to leave a test harness with a success code. The EvilGenie benchmark measures hardcoded test
cases in production coding agents.

**Why the list is specific.** A general instruction such as "do not cheat" fails. The agent
does not classify its own action as cheating. A list of named actions works, because the agent
can match its action against the list. Each entry names a concrete action:
`if n == 7: return 13`, a check of `PYTEST_CURRENT_TEST`, an added `@skip`.

**Why the holdout check is phrased as a question.** The check asks: if a reviewer replaces your
implementation with a correct general implementation, do all the tests still pass? This
question comes from the holdout-test method in the EvilGenie benchmark. It is effective because
the agent can answer it without a tool, and because it detects the failure that matters. Tests
that pass only against one specific implementation test the implementation, not the
requirement.

**Why the prohibition is absolute.** Anthropic showed that training on reward hacking can
generalise into wider misaligned behaviour. A rule with exceptions invites the agent to find
the exception. This rule has none.

## Why Coverage Is Demoted

**Failure that it prevents.** The agent optimises coverage and produces tests with weak
assertions.

Coverage measures execution. It does not measure assertion. A test with no assertion covers
many lines. An agent that is told to increase coverage will write those tests, because they are
the cheapest way to move the number.

Inozemtseva and Holmes measured the correlation between coverage and fault detection across
31,000 suites. When they controlled for suite size, the correlation was low to moderate. A
replication in 2026 found the same result for LLM-generated suites, with most coefficients
below 0.4.

**Why the manual mutation check is first.** A mutation tool is accurate and slow. It needs
installation and permission, and it can run for many minutes. The manual check needs no
installation and takes approximately 30 seconds. Break one line, run the tests, see a failure,
undo the change. An agent will do the fast check. It will avoid the slow one.

**Why the skill does not target a mutation score.** Some mutants are equivalent to the original
code and no test can kill them. A target of 100 per cent produces useless work. The skill tells
the agent to examine the mutants that survive in the code that it changed.

## Why Vertical Slices Are Required

**Failure that it prevents.** The agent writes ten tests, then ten implementations.

This behaviour looks efficient and it produces weak tests. All ten tests are designed against
an imagined interface, before any implementation shows the agent what the interface must be.
The tests then constrain a design that the agent has not validated.

An agent has a strong preference for this failure, because batch generation is its natural
mode. The skill names the failure and gives a diagram, because a general instruction to "work
in small steps" is not sufficient.

## Why Determinism Is a Correctness Property

**Failure that it prevents.** The agent writes a test with `sleep(2)` and a real clock, and
calls the result stable.

At Google, approximately 16 per cent of tests show flakiness, and flaky tests cause most CI
state changes. The mechanisms are the same in a small project: timing, order dependence, shared
state, real clocks, and the network.

The skill states that a test that fails sometimes is worse than no test. This is not
exaggeration. An intermittent failure teaches the team to ignore a red result, and a red result
is the only signal that the suite produces.

**Why the flaky claim needs proof.** The skill prohibits the deletion of a test that the agent
calls flaky without evidence. "That test is only flaky" is the most convenient explanation for
a real defect that the agent introduced. The rule is to run the test ten times against
unchanged code first.

## Why the Completion Gate Is a Checklist

**Failure that it prevents.** The agent reports that the work is complete when it is not.

The gate has eleven items. Each one refers to an observation, not to a belief. The instruction
above the list is explicit: tick a box only when you have seen the output.

The last instruction is the important one. If the agent cannot tick a box, it must tell the
user which box and why. Without that instruction, an agent that fails one item reports success
and omits the item.

## Why the Language Standard Is ASD-STE100

**Failure that it prevents.** The agent interprets an ambiguous instruction in a convenient
way.

ASD-STE100 was designed for aircraft maintenance manuals, where a misread instruction has a
physical cost. Its rules produce text with one meaning: short sentences, the active voice, one
instruction in one sentence, and a controlled vocabulary.

An agent reads this skill as instructions. Prose that a person reads as emphasis, an agent can
read as an option. "You should generally verify the failure" is weaker than "Run the focused
command. Read the output."

Read [STYLE.md](STYLE.md) for the rules.

## What This Skill Does Not Do

It does not select a test framework. The repository decides that.

It does not set a coverage target. Coverage is a weak proxy, and a target produces the wrong
behaviour.

It does not install a mutation tool. The skill proposes one and waits for permission.

It does not replace a code review. Use `requesting-code-review` before you commit.

It does not help you find a defect that you cannot reproduce. Use `systematic-debugging`.
