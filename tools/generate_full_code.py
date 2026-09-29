#!/usr/bin/env python3
"""Regenerate FULL_CODE.md: every source file of the project in one headline-wise document.

Usage: python tools/generate_full_code.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_bankflow_docx as base  # noqa: E402  (reuses the curated file order)

ROOT = base.ROOT
OUTPUT = ROOT / "FULL_CODE.md"

LANGUAGES = {
    ".py": "python",
    ".jsx": "jsx",
    ".js": "javascript",
    ".json": "json",
    ".css": "css",
    ".html": "html",
    ".svg": "xml",
    ".ps1": "powershell",
    ".yml": "yaml",
    ".txt": "text",
    ".md": "markdown",
}

SKIP = {"FULL_CODE.md", "package-lock.json"}


def tracked_files() -> list[str]:
    """Every text file git knows about, so the document can never go stale."""
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def order_key(path: str) -> tuple:
    """Root documents first, then backend, frontend and tools, using the curated order."""
    preferred = base.MANIFEST
    names = [entry[0] for entry in preferred]
    index = names.index(path) if path in names else len(names) + 1
    top_level = 0 if "/" not in path else {"backend": 1, "frontend": 2, "tools": 3}.get(
        path.split("/")[0], 4
    )
    return (top_level, index, path)


def main() -> None:
    files = [
        path
        for path in tracked_files()
        if path not in SKIP and (ROOT / path).exists() and (ROOT / path).suffix in LANGUAGES
    ]
    files.sort(key=order_key)

    lines = [
        "# BANKFLOW - AI BANKING ASSISTANT",
        "",
        "Complete source code of the project, headline-wise, in the order you create the files.",
        f"Generated from {len(files)} tracked files by tools/generate_full_code.py.",
        "",
        "> Demo application only. All banking data is fictional and no real money movement happens.",
        "",
        "---",
        "",
        "## Install and run",
        "",
        "```bash",
        "git clone https://github.com/Adnan8066/bankflow-ai-banking-assistant.git",
        "cd bankflow-ai-banking-assistant",
        "",
        "# backend",
        "cd backend",
        "python -m venv venv",
        "venv\\Scripts\\activate            # source venv/bin/activate on macOS or Linux",
        "pip install -r requirements.txt",
        "copy .env.example .env           # cp on macOS or Linux",
        "python manage.py migrate",
        "python manage.py seed_demo --flush",
        "python manage.py runserver 127.0.0.1:8000",
        "",
        "# frontend, in a second terminal",
        "cd frontend",
        "npm install",
        "copy .env.example .env           # cp on macOS or Linux",
        "npm run dev",
        "```",
        "",
        "---",
        "",
    ]

    current_group = None
    for path in files:
        group = "root" if "/" not in path else path.split("/")[0]
        if group != current_group:
            current_group = group
            title = {
                "root": "Project files",
                "backend": "Backend (Django REST Framework)",
                "frontend": "Frontend (React and Vite)",
                "tools": "Tooling",
            }.get(group, group.title())
            lines += [f"## {title}", ""]

        fence = "````" if path.endswith(".md") else "```"
        language = LANGUAGES.get(Path(path).suffix, "text")
        lines += [f"### {path}", "", f"{fence}{language}"]
        lines.append((ROOT / path).read_text(encoding="utf-8").rstrip("\n"))
        lines += [fence, ""]

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(files)} files")


if __name__ == "__main__":
    main()
