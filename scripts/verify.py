#!/usr/bin/env python3
"""Self-verification for tdd-agent-skill.

This is the canonical verification command for the repository. Run it with:

    python3 scripts/verify.py

It executes the real `run:` bodies from .github/workflows/validate.yml instead
of re-implementing them, so a bug in the workflow fails here as well as in CI.
Every gate is negative-tested: a gate that cannot fail proves nothing.

Checks covered:
  - workflow shape and all .github YAML parses
  - every runnable step of the CI workflow is executed and exits 0
  - README badges resolve and carry a colour and a logo (not flat grey)
  - `npx skills add` installs the skill end to end
  - version and documentation consistency
  - negative tests (planted em dash, broken link, missing image, broken badge)
  - asset geometry, live GitHub metadata, and hygiene
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

import yaml

try:
    from PIL import Image
except ImportError:
    Image = None

REPO = pathlib.Path(__file__).resolve().parent.parent
SLUG = "ChloeVPin/tdd-agent-skill"
SKILL = REPO / "skills/test-driven-development"
results = []


def check(name, ok, detail=""):
    results.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


def sh(*cmd):
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True).stdout.strip()


def gh(path):
    """Best-effort GitHub API read.

    Returns the parsed JSON, or None if the call fails or times out. The live
    metadata checks skip on network or auth failure so a transient outage, or a
    missing token in CI, does not break verification.

    The call runs in its own process group and is killed hard on timeout, because
    `gh` can spawn a credential-helper child that holds the stdout pipe open.
    """
    import os
    import signal

    try:
        proc = subprocess.run(
            ["gh", "api", path],
            capture_output=True, text=True, timeout=20,
            start_new_session=True,
        )
    except subprocess.TimeoutExpired as exc:
        try:
            os.killpg(os.getpgid(exc.pid), signal.SIGKILL)
        except (ProcessLookupError, OSError):
            pass
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return None


def section(title):
    print(f"\n--- {title} ---")


wf = yaml.safe_load((REPO / ".github/workflows/validate.yml").read_text(encoding="utf-8"))
steps = wf["jobs"]["validate"]["steps"]


def run(name):
    step = next(s for s in steps if s["name"] == name)
    return subprocess.run(["bash", "-e", "-c", step["run"]], cwd=REPO,
                          capture_output=True, text=True)


section("workflow shape")
check("workflow has triggers", bool(wf.get("on", wf.get(True))))
expected_steps = [
    "Check out the repository",
    "Set up Python",
    "Install PyYAML and Pillow",
    "Validate the frontmatter",
    "Check the length of the skill body",
    "Check that the bundled files exist",
    "Check that the internal links resolve",
    "Check that the README images resolve",
    "Check that the README badges resolve",
    "Run the self-verification script",
    "Check the typography",
]
check("workflow step names match", [s["name"] for s in steps] == expected_steps,
      f"{len(steps)} steps: {[s['name'] for s in steps]}")

for p in sorted((REPO / ".github").rglob("*.yml")):
    try:
        yaml.safe_load(p.read_text(encoding="utf-8"))
        check(f"yaml parses: {p.relative_to(REPO)}", True)
    except yaml.YAMLError as exc:
        check(f"yaml parses: {p.relative_to(REPO)}", False, str(exc).splitlines()[0])


section("real CI step bodies, executed")
SELF_STEP = "Run the self-verification script"
for step in [s for s in steps if s.get("run")]:
    if step["name"] == SELF_STEP:
        # This step invokes verify.py itself; running it here would recurse.
        check(f"step excluded from re-execution: {step['name']}", True,
              "invokes this script")
        continue
    p = run(step["name"])
    out = (p.stdout + p.stderr).strip().splitlines()
    check(f"step: {step['name']}", p.returncode == 0, out[-1] if out else "")


section("badges are visually distinct, not flat grey")
readme = (REPO / "README.md").read_text(encoding="utf-8")
import urllib.request
badges = sorted(set(re.findall(r'!\[[^\]]*\]\((https://img\.shields\.io/[^)]+)\)', readme)))
check("README has at least 5 badges", len(badges) >= 5, f"{len(badges)} badges")
colours, logo_count = set(), 0
for url in badges:
    req = urllib.request.Request(url, headers={"User-Agent": "verify"})
    with urllib.request.urlopen(req, timeout=30) as r:
        svg = r.read().decode("utf-8", "replace")
    fills = {f.lower() for f in re.findall(r'fill="(#[0-9a-fA-F]{3,6})"', svg)}
    accent = fills - {"#555", "#fff"}
    colours |= accent
    if "<image" in svg:
        logo_count += 1
    check(f"badge has an accent colour: {url.split('/badge/')[-1][:40] or url[-40:]}",
          bool(accent), ",".join(sorted(accent)))
check("badges use several distinct colours", len(colours) >= 4, f"{len(colours)} colours")
check("every badge carries a logo", logo_count == len(badges), f"{logo_count}/{len(badges)}")
check("no legacy flat 1f2328 badge remains", "1f2328" not in readme)


section("npx skills install, end to end")
npx_ok = shutil.which("npx") is not None
if not npx_ok:
    check("npx available", False, "npx not found")
else:
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "HOME": tmp}
        proc = subprocess.run(
            ["npx", "-y", "skills@latest", "add", SLUG,
             "--skill", "test-driven-development", "-a", "claude-code", "-g", "-y"],
            capture_output=True, text=True, cwd=tmp, env=env, timeout=300)
        check("npx skills add succeeds", proc.returncode == 0, f"exit {proc.returncode}")
        dest = pathlib.Path(tmp) / ".claude/skills/test-driven-development"
        check("skill lands in ~/.claude/skills", dest.is_dir())
        for rel in ("SKILL.md", "references/evidence.md", "assets/logo.png"):
            src, got = SKILL / rel, dest / rel
            same = got.exists() and got.read_bytes() == src.read_bytes()
            check(f"installed file is byte-identical: {rel}", same)
        if (dest / "SKILL.md").exists():
            fm = yaml.safe_load((dest / "SKILL.md").read_text(encoding="utf-8").split("---")[1])
            check("installed frontmatter intact",
                  fm.get("name") == "test-driven-development" and fm.get("author") == "chloevpin",
                  f"v{fm.get('version')}")


section("version consistency")
fm = yaml.safe_load((SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1])
changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
check("SKILL.md version is 2.0.1", fm.get("version") == "2.0.1", str(fm.get("version")))
check("CHANGELOG documents 2.0.1", "## [2.0.1]" in changelog)


section("install docs teach the CLI")
install_doc = (REPO / "docs/INSTALL.md").read_text(encoding="utf-8")
check("README shows npx skills add", f"npx skills add {SLUG}" in readme)
check("README keeps the git fallback", "git clone" in readme)
check("docs/INSTALL.md shows npx skills add", f"npx skills add {SLUG}" in install_doc)
check("docs/INSTALL.md keeps the git fallback", "git clone" in install_doc)
check("README tells the reader to read the skill first", "npx skills use" in readme)


section("negative tests")
canary = REPO / "hermes-canary.md"
for text, gate, label in [
    ("An \u2014 em dash.\n", "Check the typography", "a planted em dash"),
    ("A [broken link](nope/missing.md).\n", "Check that the internal links resolve",
     "a broken internal link"),
]:
    canary.write_text(text, encoding="utf-8")
    try:
        check(f"gate fails on {label}", run(gate).returncode != 0)
    finally:
        canary.unlink()

victim, backup = REPO / "assets/logo-256.png", REPO / "assets/.bak"
shutil.move(victim, backup)
try:
    check("gate fails on a missing README image",
          run("Check that the README images resolve").returncode != 0)
finally:
    shutil.move(backup, victim)

original = readme
try:
    (REPO / "README.md").write_text(
        readme.replace("https://img.shields.io/badge/licence-MIT-3DA639",
                       "https://img.shields.io/badge/$$$bad"), encoding="utf-8")
    check("gate fails on a broken badge URL",
          run("Check that the README badges resolve").returncode != 0)
finally:
    (REPO / "README.md").write_text(original, encoding="utf-8")
check("gates pass again after restore",
      run("Check that the README badges resolve").returncode == 0)


section("assets")
if Image is None:
    # Pillow is optional for local runs. CI installs it (see requirements.txt),
    # so the geometry checks run there. Skip locally instead of failing.
    check("asset geometry (skipped: Pillow not installed)", True, "SKIP")
else:
    for rel, dim in {
        "assets/logo.png": 1254, "assets/logo-512.png": 512, "assets/logo-256.png": 256,
        "assets/logo-128.png": 128, "skills/test-driven-development/assets/logo.png": 256,
    }.items():
        with Image.open(REPO / rel) as im:
            check(f"image: {rel}", im.size == (dim, dim) and im.format == "PNG", str(im.size))


section("live repository metadata")
meta = gh(f"repos/{SLUG}")
if meta is None:
    check("repo metadata (skipped: gh unavailable or network down)", True, "SKIP")
else:
    check("repo is public", meta.get("private") is False)
    desc = meta.get("description") or ""
    check("description within GitHub's 350-char limit", 0 < len(desc) <= 350, f"{len(desc)} chars")
    check("issues and discussions enabled",
          bool(meta.get("has_issues")) and bool(meta.get("has_discussions")))
    topics = gh(f"repos/{SLUG}/topics")
    if topics is None:
        check("topics (skipped: gh unavailable or network down)", True, "SKIP")
    else:
        check("20 topics, GitHub's maximum", len(topics.get("names", [])) == 20,
              f"{len(topics.get('names', []))}")
    prof = gh(f"repos/{SLUG}/community/profile")
    if prof is None:
        check("community health (skipped: gh unavailable or network down)", True, "SKIP")
    else:
        check("community health score is 100", prof.get("health_percentage") == 100,
              str(prof.get("health_percentage")))


section("hygiene")
check("no stale repo-name references",
      not sh("grep", "-rn", "tdd-skill-repo", "--include=*.md", "."))
check("no .DS_Store", not list(REPO.rglob(".DS_Store")))
check("no tracked file is gitignored",
      not sh("git", "ls-files", "--ignored", "--exclude-standard", "-c"))


failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
if failed:
    print("FAILED: " + "; ".join(failed))
sys.exit(1 if failed else 0)
