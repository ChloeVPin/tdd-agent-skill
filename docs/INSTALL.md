# Installation

This skill is one directory that contains Markdown files. It has no dependencies. It runs no
scripts.

There are two ways to install it. The skills CLI is the fast way. The manual copy gives you
control of the destination.

## Method 1: the skills CLI

```bash
npx skills add ChloeVPin/tdd-agent-skill
```

The CLI finds the agents that you have installed. Then it puts the skill in the correct
directory for each one. The CLI needs Node.js 22.20 or newer.

Install for one agent only:

```bash
npx skills add ChloeVPin/tdd-agent-skill -a claude-code
```

Install without a prompt, for a script or for CI:

```bash
npx skills add ChloeVPin/tdd-agent-skill -a claude-code -g -y
```

The flag `-g` installs the skill for your user account. The flag `-y` accepts the prompts.

List the skills in this repository before you install:

```bash
npx skills add ChloeVPin/tdd-agent-skill --list
```

### Read the skill first

A skill tells an agent what to do on your computer. Read it before you install it. This rule
applies to this skill and to every other skill.

```bash
npx skills use ChloeVPin/tdd-agent-skill --skill test-driven-development
```

## Method 2: the manual copy

Use this method if you do not have Node.js, or if your agent is not in the list of the CLI.

Get the repository:

```bash
git clone https://github.com/ChloeVPin/tdd-agent-skill.git
cd tdd-agent-skill
```

The directory that you copy is always the same:

```
skills/test-driven-development/
├── SKILL.md
├── assets/
│   └── logo.png
└── references/
    └── evidence.md
```

Copy the full directory. Do not copy `SKILL.md` alone. The skill refers to
`references/evidence.md`, and that link fails if the reference file is absent.

## Claude Code

The CLI installs the skill with this command:

```bash
npx skills add ChloeVPin/tdd-agent-skill -a claude-code
```

To copy the skill manually, use your personal skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/test-driven-development ~/.claude/skills/
```

To install the skill for one project only, use the project directory:

```bash
mkdir -p .claude/skills
cp -R skills/test-driven-development .claude/skills/
```

Verify the installation. Start Claude Code and run:

```
/skills
```

The list must contain `test-driven-development`.

## Hermes Agent

Copy the skill into the skills tree. The category directory is optional but it keeps the tree
organised:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R skills/test-driven-development ~/.hermes/skills/software-development/
```

Verify the installation:

```bash
hermes skills list | grep test-driven-development
```

The skill replaces the default `test-driven-development` skill if that skill is present. To
keep both skills, change the `name` field in the frontmatter before you copy the directory.

## VS Code

Copy the skill into the skills directory of the workspace:

```bash
mkdir -p .github/skills
cp -R skills/test-driven-development .github/skills/
```

VS Code finds the skill when the agent starts. To verify, ask the agent to list its skills.

## OpenAI Codex

Copy the skill into the Codex configuration directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/test-driven-development ~/.codex/skills/
```

## Any Other Agent

Find the skills directory of your tool. Copy `skills/test-driven-development/` into it. The
`SKILL.md` format is the same in all tools that support Agent Skills.

If your tool does not support Agent Skills, you can use the file as a system prompt. Read the
contents of `SKILL.md` and give it to the agent as instructions. The frontmatter block at the
top is metadata. You can remove it in this mode.

## Verify That the Skill Works

An installed skill is not always an active skill. Use this test.

Give your agent this instruction in a repository that has tests:

```
Add a function that validates an email address. Use the test-driven-development skill.
```

The agent behaves correctly if it does all of these actions:

1. It looks for the test command of the repository before it writes code. It examines the
   manifest file or the CI configuration.
2. It writes one test before it writes the implementation.
3. It runs the test and reports the failure output.
4. It writes the implementation after the failure, not before it.
5. It runs the test again and reports that the test passes.
6. It runs the full suite.

The skill is not active if the agent writes the implementation first. Check that the file is in
the correct directory. Check that the frontmatter is valid.

## Check the Frontmatter

The frontmatter must parse as YAML. Use this command to check it:

```bash
python3 -c "
import yaml
text = open('skills/test-driven-development/SKILL.md').read()
data = yaml.safe_load(text.split('---')[1])
print('name:', data['name'])
print('description length:', len(data['description']))
assert len(data['name']) <= 64
assert len(data['description']) <= 1024
print('frontmatter is valid')
"
```

The `name` field has a limit of 64 characters. The `description` field has a limit of 1024
characters. The `name` field can contain only lowercase letters, numbers, and hyphens.

## Remove the Skill

Delete the directory:

```bash
rm -rf ~/.claude/skills/test-driven-development
```

Use the equivalent path for your agent.
