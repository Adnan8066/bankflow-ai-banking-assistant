#!/usr/bin/env python3
"""Programmatic layout QA for the rendered BankFlow guide PDF.

Checks performed:
  1. page count and per-page word counts (blank page detection)
  2. text that runs past the printable area (clipping risk)
  3. missing glyph markers and characters outside the expected set
  4. every source file starts and ends inside the rendered document
  5. contents page numbers match the actual heading pages

Usage: python qa_docx_pdf.py rendered.pdf page_map.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pdfplumber

# The project root: override with BANKFLOW_ROOT, otherwise use the parent of tools/.
ROOT = Path(os.environ.get("BANKFLOW_ROOT") or Path(__file__).resolve().parents[1])
RIGHT_MARGIN_PT = 53.9 * 0.6  # tolerated right edge (points, generous)
BOTTOM_TOLERANCE_PT = 8


def norm(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


def main() -> None:
    pdf_path = Path(sys.argv[1])
    page_map = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8-sig"))

    over_right = []
    over_bottom = []
    blank_pages = []
    bad_chars = {}
    page_texts = []
    rupee_fonts = {}

    with pdfplumber.open(pdf_path) as pdf:
        page_width, page_height = pdf.pages[0].width, pdf.pages[0].height
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(text)
            if len(norm(text)) < 20:
                blank_pages.append(index)
            for char in page.chars:
                if not char.get("text"):
                    continue
                if char["x1"] > page_width - RIGHT_MARGIN_PT + 40:
                    over_right.append((index, round(char["x1"], 1), char["text"]))
                if char["bottom"] > page_height - BOTTOM_TOLERANCE_PT:
                    over_bottom.append((index, round(char["bottom"], 1), char["text"]))
                if char["text"] == "\u20b9":
                    rupee_fonts[char["fontname"]] = rupee_fonts.get(char["fontname"], 0) + 1
                if char["text"] in {"\ufffd", "\u25a1", "\u25af"}:
                    bad_chars[char["text"]] = bad_chars.get(char["text"], 0) + 1

    full_text = norm("\n".join(page_texts))

    manifest = [
        "backend/requirements.txt", "backend/.env.example", "backend/.gitignore", "backend/manage.py",
        "backend/config/settings.py", "backend/config/urls.py", "backend/config/wsgi.py",
        "backend/config/asgi.py", "backend/users/models.py", "backend/users/signals.py",
        "backend/users/permissions.py", "backend/users/serializers.py", "backend/users/views.py",
        "backend/users/urls/auth_urls.py", "backend/users/urls/profile_urls.py",
        "backend/users/admin.py", "backend/users/tests.py", "backend/banking/models.py",
        "backend/banking/services.py", "backend/banking/serializers.py", "backend/banking/views.py",
        "backend/banking/admin_views.py", "backend/banking/urls/customer_urls.py",
        "backend/banking/urls/admin_urls.py", "backend/banking/admin.py",
        "backend/banking/management/commands/seed_demo.py", "backend/banking/tests.py",
        "backend/assistant/models.py", "backend/assistant/ai_service.py",
        "backend/assistant/serializers.py", "backend/assistant/views.py",
        "backend/assistant/urls.py", "backend/assistant/admin.py", "backend/assistant/tests.py",
        "frontend/package.json", "frontend/vite.config.js", "frontend/index.html",
        "frontend/.env.example", "frontend/.gitignore", "frontend/public/bankflow.svg",
        "frontend/src/index.css",
        "frontend/src/theme.js", "frontend/src/main.jsx", "frontend/src/App.jsx",
        "frontend/src/services/api.js", "frontend/src/services/authService.js",
        "frontend/src/services/bankingService.js", "frontend/src/services/aiService.js",
        "frontend/src/services/adminService.js", "frontend/src/context/AuthContext.jsx",
        "frontend/src/utils/formatCurrency.js", "frontend/src/utils/calculations.js",
        "frontend/src/components/AppLayout.jsx", "frontend/src/components/Navbar.jsx",
        "frontend/src/components/Sidebar.jsx", "frontend/src/components/DashboardCard.jsx",
        "frontend/src/components/TransactionTable.jsx", "frontend/src/components/LoanCard.jsx",
        "frontend/src/components/ChatMessage.jsx", "frontend/src/components/ProtectedRoute.jsx",
        "frontend/src/components/Common.jsx", "frontend/src/pages/Landing.jsx",
        "frontend/src/pages/Login.jsx", "frontend/src/pages/Register.jsx",
        "frontend/src/pages/Dashboard.jsx", "frontend/src/pages/Account.jsx",
        "frontend/src/pages/Transactions.jsx", "frontend/src/pages/TransactionDetails.jsx",
        "frontend/src/pages/Loans.jsx", "frontend/src/pages/LoanDetails.jsx",
        "frontend/src/pages/EMICalculator.jsx", "frontend/src/pages/AIAssistant.jsx",
        "frontend/src/pages/Notifications.jsx", "frontend/src/pages/Profile.jsx",
        "frontend/src/pages/NotFound.jsx", "frontend/src/pages/admin/AdminDashboard.jsx",
        "frontend/src/pages/admin/CustomerManagement.jsx",
        "frontend/src/pages/admin/TransactionManagement.jsx",
        "frontend/src/pages/admin/LoanManagement.jsx",
        "frontend/src/pages/admin/AdminAnalytics.jsx", "frontend/src/pages/admin/AIMonitor.jsx",
    ]

    missing_files = []
    for rel in manifest:
        path = ROOT / rel
        if not path.exists():
            missing_files.append(f"{rel} (missing on disk)")
            continue
        if norm(rel) not in full_text:
            missing_files.append(f"{rel} (file heading not found in PDF)")
            continue
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        first, last = norm(lines[0]), norm(lines[-1])
        if first and first not in full_text:
            missing_files.append(f"{rel} (first line not rendered)")
        if last and last not in full_text:
            missing_files.append(f"{rel} (last line not rendered)")

    contents_ok = []
    for key, page in page_map.items():
        if key == "contents":
            continue
        needle = None
        if key.startswith("step"):
            needle = f"Step {key[4:]}."
        elif key.startswith("lesson"):
            needle = f"Lesson {key[6:]}."
        elif key.startswith("appendix"):
            needle = f"Appendix {key[-1].upper()}."
        if needle:
            index = page - 1
            hit = index < len(page_texts) and needle in page_texts[index]
            contents_ok.append((key, page, hit))

    print(f"pages: {len(page_texts)}")
    print(f"blank pages: {blank_pages or 'none'}")
    print(f"chars past right edge: {len(over_right)}")
    if over_right[:5]:
        print("  samples:", over_right[:5])
    print(f"chars past bottom edge: {len(over_bottom)}")
    if over_bottom[:5]:
        print("  samples:", over_bottom[:5])
    print(f"missing glyph markers: {bad_chars or 'none'}")
    print(f"rupee glyph fonts: {rupee_fonts}")
    print(f"file check failures: {missing_files or 'none'}")
    print(f"contents page mismatches: {[c for c in contents_ok if not c[2]] or 'none'}")


if __name__ == "__main__":
    main()
