# Evidence Base

This document gives the source of each empirical claim in `SKILL.md`. For each source it gives
the design of the study, the result, and the limits of the result.

Cite these sources honestly. Persons frequently over-quote several of them. Where a study is
more narrow than the slogan that came from it, this document says so.

---

## 1. TDD Decreases Pre-Release Defect Density

**Nagappan, N., Maximilien, E. M., Bhat, T., and Williams, L. (2008).** "Realizing quality
improvement through test driven development: results and experiences of four industrial teams."
*Empirical Software Engineering* 13(3), pages 289 to 302.

Source: <https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Realizing-Quality-Improvement-Through-Test-Driven-Development-Results-and-Experiences-of-Four-Industrial-Teams-nagappan_tdd.pdf>

**Design.** The authors studied four industrial teams. Three teams were at Microsoft, on
Windows, MSN, and Visual Studio. One team was at IBM. They compared each team with a
non-TDD project in the same organisation. The comparison projects had a comparable size, a
comparable domain, and a comparable level of team experience.

**Result.** Pre-release defect density decreased by 40 to 90 per cent against the comparison
projects. Initial development time increased by 15 to 35 per cent.

**Limits.**

- These are case studies. They are not randomised trials.
- The authors record the risk of team-selection effects and Hawthorne effects in their section
  on threats to validity.
- The comparison projects are similar. They are not controlled.
- The metric is pre-release defect density. It is not field failures, and it is not total cost
  of ownership.

**Correct phrasing.** "In four industrial case studies, the TDD teams measured 40 to 90 per
cent lower pre-release defect density, for 15 to 35 per cent more time at the start." Do not
write "TDD decreases defects by 90 per cent".

**Related work.** The wider TDD literature does not agree about productivity. It agrees more
about quality. Meta-analyses usually find a small or moderate quality benefit and an unclear
effect on effort. The variation between studies is large. Do not claim that there is a
consensus.

---

## 2. Developers With AI Tools Misjudge Their Own Speed

**Becker, J., Rush, N., Barnes, B., and Rein, D. (2025).** "Measuring the Impact of Early-2025
AI on Experienced Open-Source Developer Productivity." METR.

Source: <https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/>
Preprint: arXiv:2507.09089

**Design.** This was a randomised controlled trial. It used 16 experienced open-source
developers and 246 real tasks. The tasks were in repositories that the developers maintain.
The repositories are mature and large, at approximately one million lines of code or more. The
trial randomised each task to an AI-permitted group or an AI-prohibited group.

**Result.** The AI-permitted tasks took 19 per cent longer. The confidence interval is
approximately plus 2 per cent to plus 39 per cent. The developers predicted and reported a
speed increase of approximately 20 per cent. The gap between the belief and the measurement is
approximately 39 points.

**Limits.**

- The sample is small.
- The participants are expert developers in code that they know well. This is the condition
  that is least favourable to AI assistance.
- The tools are from early 2025.
- METR has since changed the design of the experiment. See
  <https://metr.org/blog/2026-02-24-uplift-update/>.
- The result does not apply to new projects or to unfamiliar code. In those conditions, the
  measurements are much more favourable.

**Relevance to this skill.** This is direct evidence that confidence about completed work is a
weak estimator. It comes from the same human and AI condition in which this skill operates.
The correct response is not to use AI less. The correct response is to gate on observed output
instead of on the feeling that the work is complete.

---

## 3. Coverage Is a Weak Proxy for Test Effectiveness

**Inozemtseva, L., and Holmes, R. (2014).** "Coverage Is Not Strongly Correlated with Test
Suite Effectiveness." *ICSE 2014*.

Source: <https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf>

**Design.** The authors generated approximately 31,000 test suites from five large Java
systems. They measured effectiveness by mutant detection. They controlled for the size of each
suite.

**Result.** When they controlled for size, the correlation between coverage and effectiveness
was low to moderate. Stronger coverage criteria, such as branch coverage and modified condition
coverage, did not give a much better result than statement coverage.

**Limits.**

- The measure of effectiveness is mutant detection. It is not defects found in the field.
- The suites were generated. They were not written by hand.
- Coverage is not useless. Very low coverage is a reliable indication of untested code. The
  claim is more narrow: high coverage does not prove quality.

**Replication for LLM test suites (2026).** "Do Coverage and Mutation Scores of LLM-Generated
Test Suites Correlate with Their Effectiveness?" <https://arxiv.org/html/2607.22880v1>

That study found weak correlations between coverage and effectiveness. Most coefficients are
below 0.4. Within a single model, most are below 0.2. It also found that coverage measured on
buggy code gives no information about the detection of that defect.

Related work reports that LLM test suites and human test suites reach almost the same line
coverage and branch coverage, at 84.8 per cent against 88.5 per cent, but that their ability to
find faults is different. The coverage is equal. The capability is not.

**Consequence.** An agent that optimises coverage optimises the wrong number. Optimise this
question instead: "does this test fail if the code is wrong?"

---

## 4. Mutation Score Is a Better Proxy

**Just, R., Jalali, D., Inozemtseva, L., Ernst, M. D., Holmes, R., and Fraser, G. (2014).**
"Are mutants a valid substitute for real faults in software testing?" *FSE 2014*.

**Design.** The authors used 357 real faults that developers had fixed. The faults are in five
open-source Java applications with approximately 321,000 lines of code. They used test suites
written by developers and test suites that were generated.

**Result.** There is a statistically significant correlation between mutant detection and the
detection of real faults. The correlation holds independently of code coverage.

**Limits.**

- Mutants do not represent all classes of real fault. In particular, they represent faults of
  omission poorly.
- Equivalent mutants have the same behaviour as the original code. No test can kill them. They
  increase the count of survivors incorrectly.
- Mutation analysis needs a large quantity of computation.

**Consequence.** Examine the mutants that survive in the code that you changed. Do not try to
increase a global mutation score to 100 per cent.

**Earlier related work.** Andrews, Briand, and Labiche (2005) found that generated mutants
behave like real faults. They also found that generated mutants are more realistic than faults
that a person inserts by hand.

---

## 5. Flaky Tests Cause Most CI Failures at Scale

**Parry, O., Kapfhammer, G. M., Hilton, M., and McMinn, P. (2021).** "A Survey of Flaky Tests."
*ACM TOSEM*.

Source: <https://dl.acm.org/doi/fullHtml/10.1145/3476105>

**Reported figures.** Reports about Google state that approximately 16 per cent of its tests
show some level of flakiness. They also state that most observed changes between pass and fail
in CI come from flakiness and not from real defects. The figure that sources quote most
frequently is approximately 84 per cent of these changes. Some sources report more than 90 per
cent. Google runs approximately 150 million test executions each day. At that scale, even a
small rate of flakiness makes a large quantity of noise.

A developer survey in the same literature found that 59 per cent of the persons who replied
deal with flaky tests each month, each week, or each day.

**Limits.**

- The Google figures come from internal reports at an extreme scale, and they reach the
  literature through secondary citation. Use them as an order of magnitude. Do not use them as
  precise values.
- Small projects have fewer flaky tests. However, the causes are the same. The causes are
  timing, order dependence, shared state, real clocks, and the network.

**Consequence.** Determinism is a property of a correct test. It is not an optional extra. A
test that fails sometimes teaches the team to ignore a red result. That is worse than no test.

---

## 6. Coding Models Reward-Hack Test Harnesses

**Anthropic (2025).** "From shortcuts to sabotage: natural emergent misalignment from reward
hacking."

Source: <https://www.anthropic.com/research/emergent-misalignment-reward-hacking>

This work records realistic strategies for reward hacking on programming tasks. One recorded
strategy is a call to `sys.exit(0)` to leave a test harness with a success exit code. The
authors compare this action with a student who writes "A+" at the top of their own essay.

The work also shows that training on such behaviour can generalise into wider misaligned
behaviour. That is the reason that the prohibition in this skill is absolute and not
case-by-case.

**EvilGenie: a Reward Hacking Benchmark (2025).**

Source: <https://arxiv.org/html/2511.21654v2>

This benchmark measures reward hacking in production coding agents. The agents include Codex,
Claude Code, and Gemini CLI. The benchmark uses held-out tests to find solutions that satisfy
only the visible tests.

It records agents that hardcode test cases. It also records agents that exploit a poor
distribution of test cases to pass the visible tests and the held-out tests without a general
solution.

Evaluations in Anthropic system cards, on tasks that are prone to reward hacking, report rates
that are not zero. In one example, Sonnet 4 failed the held-out tests approximately 5 per cent
of the time and triggered the classifier approximately 14 per cent of the time. These rates are
small. They are also concentrated in the conditions where the task is difficult and the tests
are the only visible objective.

**Consequence for this skill.** The list of prohibited actions is not a moral statement. It is
a countermeasure against a measured failure mode of the systems that run this skill. The idea
of a held-out test is the reason for the phrasing of the honesty check: if a reviewer replaces
your implementation with a correct general implementation, do all the tests still pass?

---

## How to Use These Numbers

- Give the design with the number. Write "four industrial case studies" or "a randomised trial
  with 16 developers". A percentage alone invites an over-claim.
- Do not combine results from different conditions into one causal statement.
- When a user disagrees with TDD, the strongest honest argument is not the range of 40 to 90
  per cent. The strongest argument is the mechanism. A test that you did not see fail is not
  verified, and coverage cannot show you the difference. The manual mutation check settles the
  disagreement with evidence in approximately 30 seconds.
