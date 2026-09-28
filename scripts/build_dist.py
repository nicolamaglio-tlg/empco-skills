#!/usr/bin/env python3
"""Build the downloadable files attached to each GitHub release, into dist/:

  <skill>.zip  one skill per zip, for skill-upload apps (e.g. Claude.ai)
  <skill>.md   the whole skill in one file, for any chat app: attach it, or add it to a project

  python3 scripts/build_dist.py
"""
from __future__ import annotations
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ["empco-screener", "empco-claim-writer"]
ZIP_EXCLUDE = {"tests", "README.md", "__pycache__", ".env"}
REPO_URL = "https://github.com/nicolamaglio-tlg/empco-skills"


def frontmatter(skill_md: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", skill_md, re.S)
    if not m:
        raise SystemExit("SKILL.md has no frontmatter")
    fields = dict(re.findall(r"^(\w+): (.+)$", m.group(1), re.M))
    return fields, skill_md[m.end():]


def validate(skill: str, fields: dict) -> None:
    name, desc = fields.get("name", ""), fields.get("description", "")
    problems = []
    if name != skill:
        problems.append(f"name {name!r} doesn't match folder {skill!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        problems.append("name must be lowercase-hyphenated, max 64 chars")
    if not desc or len(desc) > 1024:
        problems.append(f"description must be 1-1024 chars (is {len(desc)})")
    if problems:
        raise SystemExit(f"{skill}: " + "; ".join(problems))


def skill_files(skill_dir: Path) -> list[Path]:
    return sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and not ZIP_EXCLUDE.intersection(p.relative_to(skill_dir).parts)
    )


def build_zip(skill: str, files: list[Path]) -> Path:
    out = DIST / f"{skill}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, f"{skill}/{p.relative_to(ROOT / skill)}")
    with zipfile.ZipFile(out) as z:
        count = sum(n.endswith("/SKILL.md") or n == "SKILL.md" for n in z.namelist())
    if count != 1:
        raise SystemExit(f"{out.name} contains {count} SKILL.md files, expected exactly 1")
    return out


def build_single_file(skill: str, fields: dict, body: str, files: list[Path]) -> Path:
    skill_dir = ROOT / skill
    parts = [
        f"# {skill} — instructions for an AI assistant",
        "",
        f"> **To the assistant:** these are your instructions for this task — follow them. "
        f"{fields['description']}",
        ">",
        "> This single file contains the whole skill. Where the instructions mention a file such as "
        "`references/…` or `assets/…`, its full text is included below under that file's name. "
        "If you can't run scripts, skip any script step and use the alternative the instructions give.",
        "",
        f"<!-- Built from {REPO_URL} — first-pass screening, not legal advice. -->",
        "",
        body.strip(),
    ]
    for p in files:
        rel = p.relative_to(skill_dir).as_posix()
        if rel == "SKILL.md" or p.suffix != ".md" or rel == "SETUP.md":
            continue
        text = re.sub(r"^<!-- Synced from .*?-->\n\n", "", p.read_text(encoding="utf-8"))
        parts += ["", "---", "", f"## File: `{rel}`", "", text.strip()]
    out = DIST / f"{skill}.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return out


def main() -> int:
    DIST.mkdir(exist_ok=True)
    for skill in SKILLS:
        skill_dir = ROOT / skill
        fields, body = frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        validate(skill, fields)
        files = skill_files(skill_dir)
        for out in (build_zip(skill, files), build_single_file(skill, fields, body, files)):
            print(f"built {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
