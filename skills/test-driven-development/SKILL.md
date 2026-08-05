---
name: test-driven-development
description: "TDD for coding agents: RED-GREEN-REFACTOR with hard gates, stack discovery, anti-reward-hacking checks, and mutation-based proof that tests are real."
version: 2.0.0
author: chloevpin
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, tdd, development, quality, red-green-refactor, mutation-testing, reward-hacking]
    related_skills: [systematic-debugging, requesting-code-review, plan, spike]
---

# Test-Driven Development for AI Coding Agents

## Overview

Write the test first. Run it. See it fail. Then write the minimum code that makes it pass.

**Core principle:** a test that you did not see fail is not evidence. It is a guess with a
green tick.

This skill is for an agent that can run commands. That changes what is important. An agent
writes code and tests faster than a person can read them. The limit is not typing speed. The
limit is proof. Each rule below changes "this looks correct" into "I saw the test change from
fail to pass".

## Evidence Summary

Read `references/evidence.md` for the full citations and the limits of each study.

| Claim | Evidence |
|---|---|
| TDD decreases defects | Four industrial teams at Microsoft and IBM measured a decrease in pre-release defect density of 40 to 90 per cent. Initial development time increased by 15 to 35 per cent. Nagappan, Maximilien, Bhat and Williams, *Empirical Software Engineering* 13(3), 2008. |
| Agents feel faster than they are | METR ran a randomised controlled trial with 16 experienced developers and 246 real tasks. AI-assisted work took 19 per cent longer. The developers believed that they were 20 per cent faster. The gap between belief and measurement was 39 points. |
| Coverage is a weak proxy | Inozemtseva and Holmes, ICSE 2014, examined 31,000 test suites in five large systems. When they controlled for suite size, coverage correlated only weakly with fault detection. High coverage does not prove that the tests are good. |
| Mutation score is a better proxy | Just and others, FSE 2014, used 357 real faults. Mutant detection correlates with real fault detection. The correlation holds independently of code coverage. |
| Flaky tests are the usual failure at scale | Google reports that approximately 16 per cent of its tests show some flakiness. Most pass-to-fail changes in its CI system come from flaky tests, not from real defects. |
| Models special-case tests under pressure | Studies of reward hacking from Anthropic and the EvilGenie benchmark show that coding models hardcode expected values, special-case inputs, and call `sys.exit(0)` to fake a green test harness. **You are one of these models.** Read the section "Prevent Reward Hacking". |

Use these numbers to support the discipline. Do not use them to skip it. The range of 40 to 90
per cent applies to pre-release defect density in four specific industrial projects. It is not
a general guarantee.

## When to Use This Skill

Use it for all of these:

- New features
- Bug fixes
- Changes to the behaviour of existing code
- Edge cases and error paths
- Any change that can break code that works today

You do not need it for these:

- Configuration files
- Documentation
- Static content
- Changes to format only

Ask the user before you skip TDD for these:

- Throwaway experiments. Use the `spike` skill.
- Generated code
- Migration scripts that run one time

Do you think "I will skip TDD only this time"? That thought is a rationalisation. Read the
table of rationalisations below.

## Step 0: Find the Test Commands

The cycle is the same in all languages. The commands are not. **Do not assume `npm test` or
`pytest`.** An agent that uses a default command without a check is the most common failure in
this loop.

Look in this order:

1. **Manifest files.** Examples: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
   `pom.xml`, `build.gradle`, `Gemfile`, `Makefile`, `mix.exs`.
2. **Wrapper scripts in the repository.** Use `./gradlew test`, `./mvnw test`, `make test`, or
   `just test` before you use a global binary.
3. **CI configuration.** Look in `.github/workflows/` and `.gitlab-ci.yml`. These commands
   control merges. If CI runs `uv run pytest -m "not slow"`, then that is the real command.
4. **Tests near your change.** Find their location, their file names, their fixtures, and
   their assertion style. Obey the conventions of the repository. Do not add your preferred
   framework.
5. **Both command types.** You need a fast command for one test. You also need the full-suite
   command for the completion gate.

Write down both commands before you write code:

```text
FOCUSED: <the command that runs one test>
FULL:    <the command that runs everything that CI runs>
```

If you cannot find the test command, ask the user. Do not invent a command.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Did you write code before the test? Delete the code. Start again from the test.

**To delete means to delete.** Do not keep the code for reference. Do not adapt it while you
write the test. Do not keep it in a scratch file to look at.

There is a reason for this rule. If you keep the code, the test that you write will follow the
code that exists. That is the exact bias that TDD removes.

## The Cycle

```
   +--------------------------------------------------------+
   |                                                        |
   v                                                        |
 RED ---> VERIFY RED ---> GREEN ---> VERIFY GREEN ---> REFACTOR
 write    run it, see     minimal    run focused and    clean up,
 one      the correct     code       then full suite,   stay green
 test     failure                    output is clean
           |                          |
           +- wrong failure?          +- fails? fix the CODE.
              fix the test               Never fix the test.
```

Each arrow is a gate. Do not pass a gate because you believe the code is correct. Pass a gate
only when you see the output.

### RED: Write One Failing Test

Test one behaviour. Use a descriptive name. Use real code paths, not a sequence of mocks.

Answer this question in one sentence before you write the assertion: **"Which change to the
production code makes this test fail?"** If you cannot answer, the test proves nothing.

```python
def test_retries_failed_operations_three_times():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TransientError("fail")
        return "success"

    result = retry_operation(operation)

    assert result == "success"
    assert attempts == 3
```

This test is good. The name is clear. The function is real. The test asserts the result and
the retry count. The retry count is the actual feature.

```python
def test_retry_works():                        # The name is vague.
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), "success"]
    assert retry_operation(mock) == "success"  # This asserts the script of the mock.
```

This test is bad. It tests the mock. It does not test your code.

Obey these requirements:

- Test one behaviour in one test.
- Split the test if the name contains "and".
- Name the behaviour. Do not name the implementation.
- Use the real collaborator when you can.

### VERIFY RED: Watch the Test Fail

**This step is mandatory. Do not skip it.**

Run the focused command. Read the output. Confirm these three conditions:

- [ ] The test fails. It does not error. An `ImportError`, a `SyntaxError`, or a `NameError`
      from a typing mistake is not a RED. It is a broken test. Correct it and run it again
      until it fails for the correct reason.
- [ ] The failure message is the message that you predicted. Examples: a wrong value, a
      missing attribute, or an exception. The message is not an unrelated error.
- [ ] The test fails because the behaviour does not exist yet.

**Does the test pass immediately?** Then the behaviour already exists, or your assertion proves
nothing. An assertion proves nothing if it is `assert True`, if it asserts the return value of
a mock, or if it compares a value with itself. Write the test again.

This gate separates TDD from "I wrote some tests". To skip this gate is to lose the whole
method.

### GREEN: Write the Minimum Code

Write the simplest code that makes the test pass. Do not add parameters. Do not add logging.
Do not add options for the future. Do not refactor other code at the same time.

You can cheat inside GREEN. You can hardcode a value, copy code, or ignore an edge case. There
is one condition. The next RED test must punish the cheat, and you must remove the cheat in
REFACTOR. A hardcoded value that stays until the commit is not TDD. It is reward hacking. Read
the next section.

### VERIFY GREEN: Watch the Test Pass

**This step is mandatory.**

Run the focused command. Then run the full command. Confirm these three conditions:

- [ ] The new test passes.
- [ ] The full suite passes. There are no regressions.
- [ ] The output is clean. There are no new warnings, no deprecation messages, no stack traces,
      and no debug output. Noise that you accept today hides the signal that you need tomorrow.

Does the test fail? Correct the code. Do not make the assertion weaker. Do not add a skip. Do
not increase a tolerance. Do not delete the case. Those actions falsify your evidence.

### REFACTOR: Clean the Code While the Tests Are Green

Remove duplicate code. Improve the names. Extract helper functions. Make the code more simple.
Do not change the behaviour.

Run the tests after each step. If a refactor breaks a test, undo it immediately. Then use a
smaller step. Do not try to debug forward from a broken refactor.

## Use Vertical Slices

Do not write all the tests and then write all the implementations.

```text
WRONG (horizontal):        CORRECT (vertical slices):
  RED:   t1 t2 t3 t4         RED -> GREEN: t1 -> impl1
  GREEN: i1 i2 i3 i4         RED -> GREEN: t2 -> impl2
                             RED -> GREEN: t3 -> impl3
```

Horizontal batches make weak tests. You design all of them against an imagined interface,
before the implementation shows you the correct interface. Each vertical slice gives you real
information for the next test.

## Prevent Reward Hacking

Researchers have measured what coding models do under pressure to make tests pass. The models
hardcode expected output. They special-case the exact inputs of the test. They make assertions
weaker. They mark tests as skipped. They stop the test harness early so that it reports
success.

There is no intent in this behaviour. The goal "a green test suite" has an honest solution and
a dishonest solution. The dishonest solution is shorter.

**These actions are prohibited. If you start one of them, stop and undo it:**

- To hardcode a value because the test expects it. Example: `if n == 7: return 13`
- To branch on a test-only condition. Examples: a check of `PYTEST_CURRENT_TEST`, a check of
  `NODE_ENV === 'test'`, a check of the hostname, or a check of the name of the caller.
- To edit, weaken, or delete an existing test so that your change passes.
- To add `@skip`, `@xfail`, `.only`, `.skip`, `it.todo`, or `-k 'not mytest'` for a clean run.
- To increase a tolerance, or to make a regular expression more general, until the test stops
  to fail.
- To catch and discard the exception that the test was written to observe.
- To exit early so that the runner reports success without the assertions. Examples:
  `sys.exit(0)`, `process.exit(0)`, or a replaced reporter.
- To delete an unrelated failing test and call it flaky without proof. Run it ten times on
  unchanged code first.

**Do this honesty check before you report that the work is complete.** Ask this question: if a
reviewer replaces my implementation with a correct general implementation, do all the tests
still pass? If your tests pass only against your specific code, then you tested your code. You
did not test the requirement.

**Sometimes a test must change.** Tell the user directly. Give the name of the test. Give the
old assertion. Give the reason that the requirement changed. Make the change as a visible step.
Never make the change quietly.

## Prove That the Tests Are Real

Tests that pass prove that the code runs. They do not prove that the tests can catch a defect.
Coverage is a weak proxy. Use one of these two checks instead.

**Check 1: manual mutation.** This check is always available and takes approximately 30
seconds. Break the production code on purpose. Change a comparison operator. Change `+` to `-`.
Return a constant. Delete a line. Then run the tests. A test must fail. If no test fails, then
that code path has no test, and the coverage number does not matter. Undo the change.

**Check 2: a mutation tool.** Use this check when the test suite is important.

| Ecosystem | Tool | Command |
|---|---|---|
| Python | mutmut or cosmic-ray | `mutmut run --paths-to-mutate src/` |
| JavaScript and TypeScript | Stryker | `npx stryker run` |
| Java | PIT | `mvn org.pitest:pitest-maven:mutationCoverage` |
| Go | go-mutesting | `go-mutesting ./...` |
| Rust | cargo-mutants | `cargo mutants` |

A mutant that survives shows a missing test. Examine the mutants that survive in the code that
you changed. Do not try to improve a global score. Mutation runs are slow. Some mutants are
equivalent to the original code, and no test can kill them. Do not install a mutation tool
without permission. Propose it to the user first.

## Select the Test Level

```
Is it pure logic with no I/O?          -> unit test, "small"        milliseconds
Does it cross a boundary such as a     -> integration test,
  database, HTTP, or the file system?     "medium"                  seconds
Is it a critical end-to-end flow?      -> end-to-end test, "large"  minutes
```

Most of the suite must be small tests. The size of a test is the quantity of resources that it
uses. The size is not the folder that contains the file. A small test uses one process. It uses
no network, no sleep calls, and no real clock. Small tests are fast, repeatable, and easy to
debug. Test a defect at the lowest level that can find it.

## Write Tests That Survive a Refactor

**Assert the state. Do not assert the interactions.** Test the result. Do not test which
internal methods the code called. Assertions on interactions break during each refactor, even
when the behaviour does not change. They measure your implementation. They do not measure your
requirement.

```python
# Good. This asserts the outcome.
tasks = list_tasks(sort_by="created_at", order="desc")
assert tasks[0].created_at > tasks[1].created_at

# Bad. This asserts the implementation.
list_tasks(sort_by="created_at", order="desc")
db.query.assert_called_with("... ORDER BY created_at DESC")
```

**Use DAMP, not DRY.** In production code, DRY (Do Not Repeat Yourself) is usually correct. In
tests, DAMP (Descriptive And Meaningful Phrases) is better. A reader must understand a test
from top to bottom without a search for shared helper functions. In tests, duplicate code is
usually an acceptable cost for clarity.

**Use the most realistic test double that you can afford.**

```
real implementation > fake (in-memory) > stub (canned data) > mock (asserts calls)
   highest confidence ------------------------------------> lowest confidence
```

Use a mock only for a dependency that is slow, that is not deterministic, or that has side
effects that you cannot control. Examples: payment APIs, email, clocks, and random numbers. Too
many mocks give a suite that stays green while production fails. Learn the real side effects of
a dependency before you mock it. A mock that is wrong about the real dependency is worse than
no test.

**Use Arrange, Act, Assert.** Test one concept in one test. Write names that read as a
specification. Examples: `sets completed_at when the task is completed`,
`raises NotFoundError for an unknown id`, and
`is idempotent when the task is already completed`.

**Determinism is mandatory.** Inject the clock. Set the seed of the random number generator.
Never call `sleep()` to wait. Poll for a condition, or use the async utilities of the
framework. A test must not depend on the execution order or on shared mutable state.

At scale, flaky tests cause most CI failures. They also destroy trust in the suite. A test that
fails sometimes is worse than no test, because it teaches the team to ignore a red result.

## Fix Bugs With a Reproduction Test

Never fix a defect that you did not reproduce in a test.

```
Bug report
   -> Write a test that FAILS on the current code.
      This is the reproduction. It is also proof that you understand the defect.
   -> Fix the code.
   -> The test passes.
   -> Run the full suite.
   -> The work is complete.
```

If you cannot write a failing test, then you do not understand the defect yet. Change to the
`systematic-debugging` skill.

The reproduction test is also the permanent guard against a regression. It is the only artefact
that prevents the return of this defect.

## Rationalisations and Replies

| Rationalisation | Reply |
|---|---|
| "This is too simple to test." | Simple code breaks. The test costs 30 seconds and it records the intent. |
| "I will write the tests after the code." | Tests that you write after the code pass immediately. That proves nothing. You never saw them catch a defect. |
| "Tests after the code have the same result. This is about the spirit, not the ritual." | Tests after the code answer "what does this do?". Tests before the code answer "what must this do?". Tests after the code follow the code that you already wrote. You cover the cases that you remember. You do not find the cases that you forgot. |
| "I already tested it manually." | Manual tests are ad hoc. There is no record. You cannot repeat them. "It worked when I tried it" is not coverage. |
| "It is wasteful to delete hours of work." | This is the sunk cost fallacy. The time is gone in both options. The real choice is code that you trust or code that you cannot trust. |
| "I will keep the code for reference and write the tests first." | You will adapt the code. That is a test after the code, with more steps. |
| "I must explore the problem first." | That is correct. Write a spike. Then delete the spike and build the feature with TDD. |
| "This code is hard to test." | The test tells you that the design is hard to use. Listen to it. Inject the dependencies. Make the interface smaller. |
| "TDD will make me slower." | The measured cost is 15 to 35 per cent more time at the start. The measured benefit is 40 to 90 per cent fewer pre-release defects. To debug in production is the slow option. |
| "The code has 100 per cent coverage." | Coverage correlates only weakly with fault detection. Change one line and see if a test fails. |
| "Coverage increased, so the tests are better." | Coverage measures execution. It does not measure assertions. A test with no assertions can cover many lines. |
| "That test is only flaky." | Prove it. Run it ten times against unchanged code. Then repair the cause of the nondeterminism. Do not delete the test. |
| "The suite passes. I will run it one more time to be sure." | To run unchanged code again gives no new information. Run the tests after a change, not for reassurance. |

## Red Flags: Stop and Start the Cycle Again

- Production code exists, and no test failed before it.
- You used `npm test` or `pytest` without a check of this repository.
- A new test passed on its first run.
- You cannot say why the test failed during RED.
- You edited a test to make your change pass.
- A skip, an xfail, or a `.only` is in your diff.
- Production code reads a test environment variable or a test name.
- You reported "all tests pass" but you did not read the output of the runner.
- You thought "this case is different because ...".

## Completion Gate

Do not report that the work is complete until you can tick each box. Tick a box only when you
have seen the output.

- [ ] I found the test command in the repository. I did not assume it.
- [ ] Each new behaviour has a test, and I saw that test fail first.
- [ ] Each RED failed for the reason that I predicted. It was not a typing mistake or an
      import error.
- [ ] The implementation is the minimum code that passes. There are no unused features.
- [ ] The full suite passes with the command of the repository.
- [ ] The output is clean. There are no new warnings and no debug output.
- [ ] No test was made weaker, skipped, deleted, or special-cased.
- [ ] No production code branches on a test environment.
- [ ] Each bug fix has a reproduction test that failed before the fix.
- [ ] I broke one changed code path on purpose and I saw a test fail.
- [ ] The tests cover the edge cases, the error paths, and the boundaries. They do not cover
      only the successful path.

Can you not tick a box? Tell the user which box, and tell the user why. Do not pass the gate
quietly.

## Use With Hermes Agent

```python
terminal("<FOCUSED>")   # RED. Read the output. Confirm the correct failure.
terminal("<FOCUSED>")   # GREEN. Confirm that the test passes.
terminal("<FULL>")      # Gate. Confirm that there are no regressions.
```

Do you delegate the implementation? Put the gates in the brief. A subagent that has no
instruction to verify RED will skip it.

```python
delegate_task(
    goal="Implement <feature> with strict TDD",
    context="""
    Obey the test-driven-development skill. These rules are mandatory:
      1. Find the test command of this repository first. The CI configuration is the
         authority.
      2. Write ONE failing test. RUN IT. Put the failure output in your summary.
      3. Write the minimum code that passes. RUN IT. Put the pass output in your summary.
      4. Run the full suite. Put the result in your summary.
      5. Never edit or skip an existing test. Never special-case a test input.
    Report the real output of the runner. Do not describe it.
    """,
)
```

A summary from a subagent is a self-report. Run the suite yourself before you accept the
statement "all tests pass".

Use these related skills:

- Use `systematic-debugging` when you cannot reproduce a defect.
- Use `spike` when you do not know if the approach is possible.
- Use `requesting-code-review` before you commit.

## Final Rule

```
Production code -> a test exists, it failed first, and you saw it fail
Anything else   -> this is not TDD
```

There are no exceptions without the explicit permission of the user.

## References

- `references/evidence.md`. Full citations, the design of each study, and the limits of each
  result.
- `assets/logo.png`. The project logo.
