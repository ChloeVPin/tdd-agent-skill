# Usage

## How the Agent Loads the Skill

The agent reads the `description` field of each installed skill at the start of a session. It
reads the body of `SKILL.md` only when the task matches the description. This behaviour is
called progressive disclosure. It keeps the context window small.

The description of this skill is:

```
TDD for coding agents: RED-GREEN-REFACTOR with hard gates, stack discovery,
anti-reward-hacking checks, and mutation-based proof that tests are real.
```

The agent loads the skill automatically for tasks about tests, defects, or new behaviour. You
can also load it directly.

## Load the Skill Directly

Name the skill in your instruction:

```
Use the test-driven-development skill. Add retry logic to the HTTP client.
```

Some tools have a command for this action:

```
/skill test-driven-development
```

## What Correct Behaviour Looks Like

The agent must produce this sequence. Each step has visible output.

**Step 1. The agent finds the test commands.**

```
I examined pyproject.toml and .github/workflows/ci.yml.
FOCUSED: uv run pytest tests/test_client.py::test_name -v
FULL:    uv run pytest -m "not slow"
```

**Step 2. The agent writes one failing test.**

The test covers one behaviour. The name describes the behaviour.

**Step 3. The agent runs the test and shows the failure.**

```
FAILED tests/test_client.py::test_retries_three_times
AttributeError: 'HttpClient' object has no attribute 'retry'
```

The failure must match the prediction of the agent. An import error or a spelling error is not
a valid RED.

**Step 4. The agent writes the minimum implementation.**

**Step 5. The agent runs the test and shows that it passes.**

**Step 6. The agent runs the full suite and shows the result.**

If the agent gives you a summary without the output of the test runner, ask for the output. A
summary is a self-report. The output is evidence.

## Example: A New Feature

Your instruction:

```
Use the test-driven-development skill. Add a rate limiter to the API client.
It must permit 10 requests each second.
```

The agent makes several small cycles. It does not write all the tests first. Each cycle covers
one behaviour:

```
Cycle 1: permits a request when the count is below the limit
Cycle 2: rejects a request when the count reaches the limit
Cycle 3: resets the count after one second
Cycle 4: raises RateLimitError with the wait time
```

Each cycle is RED, then VERIFY RED, then GREEN, then VERIFY GREEN, then REFACTOR. This method
is a vertical slice. The implementation of each cycle teaches the agent about the interface for
the next cycle.

## Example: A Bug Fix

Your instruction:

```
Use the test-driven-development skill. Bug: completeTask does not set completedAt.
```

The agent must write a reproduction test first:

```
1. Write a test that asserts completedAt is a date after completeTask runs.
2. Run it. The test fails. This proves that the defect exists and that the agent
   understands it.
3. Fix the code.
4. Run the test. It passes. This proves that the fix works.
5. Run the full suite. This proves that there are no regressions.
```

The reproduction test stays in the suite. It prevents the return of this defect.

If the agent cannot write a failing test, then the agent does not understand the defect. Tell
it to use the `systematic-debugging` skill first.

## Delegation to a Subagent

A subagent does not obey the gates unless you put the gates in the brief.

```python
delegate_task(
    goal="Implement the rate limiter with strict TDD",
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

Run the test suite yourself before you accept the statement "all tests pass". A summary from a
subagent is a self-report.

## Check That the Tests Are Real

Passing tests prove that the code runs. They do not prove that the tests can find a defect.

Ask the agent to run the manual mutation check:

```
Break one line of the code that you changed. Run the tests. Show me which test fails.
Then undo the change.
```

If no test fails, then that code path has no test. The coverage number does not matter.

For an important suite, use a mutation tool. Ask first, because these tools are slow:

| Language | Tool | Command |
|---|---|---|
| Python | mutmut | `mutmut run --paths-to-mutate src/` |
| JavaScript and TypeScript | Stryker | `npx stryker run` |
| Java | PIT | `mvn org.pitest:pitest-maven:mutationCoverage` |
| Go | go-mutesting | `go-mutesting ./...` |
| Rust | cargo-mutants | `cargo mutants` |

## Signs of a Problem

Stop the agent and correct it when you see one of these signs.

| Sign | Cause | Action |
|---|---|---|
| The agent wrote the implementation first | It did not load the skill, or it ignored the Iron Law | Tell it to delete the code and start from the test |
| A new test passed on its first run | The assertion proves nothing, or the behaviour already exists | Tell it to write the test again |
| The agent used `npm test` in a Python repository | It skipped Step 0 | Tell it to find the real command |
| A skip or an xfail appeared in the diff | Reward hacking | Tell it to undo the change and fix the code |
| The code contains a check of an environment variable such as `NODE_ENV` | Reward hacking | Tell it to undo the change |
| The agent says "all tests pass" without output | A self-report, not evidence | Ask for the output of the runner |
| The agent deleted a failing test and called it flaky | An unproven claim | Tell it to run the test ten times on unchanged code |

## When Not to Use This Skill

Do not use it for configuration files, documentation, static content, or changes to format
only. These changes have no behaviour to test.

For an experiment that answers "is this possible?", use the `spike` skill. Delete the
experiment. Then build the real feature with TDD.
