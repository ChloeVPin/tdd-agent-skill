# Contributing

Thank you for your interest in this skill. This document explains how to propose a change.

## The Standard for a Change

This skill makes claims about software engineering. Each claim must have evidence, or it must
be marked clearly as an opinion.

Before you propose a change, answer these three questions.

**1. Which failure does this change prevent?**

Name the specific behaviour that an agent produces today and must not produce after the
change. A change that improves the style but prevents no failure adds tokens and gives no
benefit.

**2. What is the evidence?**

An empirical claim needs a citation. The citation needs a study design and a statement of its
limits. Read `skills/test-driven-development/references/evidence.md` for the format.

A claim from experience is acceptable. Mark it as experience. Do not write it as a
measurement.

**3. What is the cost in tokens?**

The agent loads the whole `SKILL.md` file into its context. Each sentence competes with the
conversation and with the task. The body must stay below 500 lines. If your addition is
detailed, put it in a file in `references/` and link to it.

## Types of Change

### A Correction to a Fact

Open an issue. Give the source that contradicts the current text. This is the most valuable
type of contribution. An incorrect citation damages the trust in all the others.

### A New Section

Open an issue first. Describe the failure that the section prevents. Include an example of the
incorrect behaviour of an agent, with real output if you have it.

### A New Rationalisation

The table answers arguments that stop an agent from using TDD. To add an entry, give the
argument in the form that you saw it, and give the reply.

### A Correction to the Language

The repository uses ASD-STE100 Simplified Technical English. Read `docs/STYLE.md`. Corrections
that improve the conformance are welcome. State which rule the current text breaks.

## Before You Open a Pull Request

Check these items.

- [ ] The frontmatter parses as YAML. The `name` field is 64 characters or fewer. The
      `description` field is 1024 characters or fewer.
- [ ] The body of `SKILL.md` is below 500 lines.
- [ ] There are no em dashes.
- [ ] There are no emoji.
- [ ] The spelling is international English outside code blocks.
- [ ] Each procedural sentence gives one instruction.
- [ ] Each new claim has a citation, or it is marked as experience.
- [ ] A new citation includes the design of the study and its limits.
- [ ] You tested the change with a real agent on a real task.

Run this command to check the frontmatter:

```bash
python3 -c "
import yaml
text = open('skills/test-driven-development/SKILL.md').read()
data = yaml.safe_load(text.split('---')[1])
assert len(data['name']) <= 64, 'name is too long'
assert len(data['description']) <= 1024, 'description is too long'
print('frontmatter is valid')
"
```

Run this command to find em dashes and emoji. It uses a Unicode escape, so the command itself
does not contain the characters that it looks for.

```bash
python3 - <<'PY'
import pathlib, re, sys

banned = {'\u2014': 'em dash', '\u2013': 'en dash'}
emoji = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF]')
found = False

for path in pathlib.Path('.').rglob('*.md'):
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        for character, label in banned.items():
            if character in line:
                print(f'{path}:{number}: found {label}')
                found = True
        if emoji.search(line):
            print(f'{path}:{number}: found emoji')
            found = True

sys.exit(1 if found else 0)
PY
```

## Test Your Change With an Agent

A change to a skill is a change to the behaviour of a program. Test it.

1. Install your version of the skill.
2. Give an agent a real task in a real repository.
3. Record what the agent does.
4. Compare the result with the behaviour before your change.

Put the result in the pull request. Describe the task, the agent, and the difference in
behaviour.

A change that you did not test with an agent is a guess. The skill exists to remove guesses
from software, and the same standard applies to the skill itself.

## What This Repository Will Not Accept

**A framework preference.** The skill does not select a test framework. The repository under
test decides that.

**A coverage target.** Coverage correlates weakly with fault detection. A target produces
tests with weak assertions.

**A rule with no failure behind it.** Each rule costs tokens in every session that loads the
skill.

**An exception to the anti-reward-hacking list.** That list is absolute by design. A rule with
exceptions invites an agent to find the exception.

## Code of Conduct

Be direct about technical problems. Be respectful about people. Give evidence for a
disagreement.
