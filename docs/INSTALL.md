# Installation

This skill is one directory that contains Markdown files. It has no dependencies. It runs no
scripts. To install it, copy the directory into the skills directory of your agent.

## Before You Start

Get the repository:

```bash
git clone https://github.com/chloevpin/tdd-skill-repo.git
cd tdd-skill-repo
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

Copy the skill into your personal skills directory:

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
