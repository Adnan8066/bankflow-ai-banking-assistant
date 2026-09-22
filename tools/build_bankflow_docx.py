#!/usr/bin/env python3
"""Build the BankFlow setup guide DOCX: step-by-step instructions + complete source code.

Usage:
    python build_bankflow_docx.py [page-map.json]

The optional page-map.json is produced by measure_pages.py after the first render and
supplies the real page number for every contents entry. When it is missing the contents
page numbers are omitted, so the document still builds cleanly on the first pass.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import (
    WD_ALIGN_PARAGRAPH,
    WD_LINE_SPACING,
    WD_TAB_ALIGNMENT,
    WD_TAB_LEADER,
)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# The project root: override with BANKFLOW_ROOT, otherwise use the parent of tools/.
ROOT = Path(os.environ.get("BANKFLOW_ROOT") or Path(__file__).resolve().parents[1])
OUTPUT = ROOT / "BankFlow-Complete-Setup-Guide-with-Full-Code.docx"

CODE_FONT = "Consolas"
CODE_SIZE = Pt(7.5)
CODE_LINE = Pt(9)
BODY_FONT = "Calibri"
BODY_SIZE = Pt(10.5)

HEADER_FILL = "1B3A8F"
HEADER_TEXT = "FFFFFF"
ROW_TINT = "F4F6FB"
BORDER_GREY = "D9D9D9"


# --------------------------------------------------------------------------- #
# low level docx helpers
# --------------------------------------------------------------------------- #
def black(style, size=None, bold=None):
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.font.name = BODY_FONT
    if size is not None:
        style.font.size = size
    if bold is not None:
        style.font.bold = bold


def strip_paragraph_borders(style):
    ppr = style.element.get_or_add_pPr()
    for border in ppr.findall(qn("w:pBdr")):
        ppr.remove(border)


def configure_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    black(normal, BODY_SIZE)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    title = doc.styles["Title"]
    black(title, Pt(24), bold=True)
    strip_paragraph_borders(title)
    title.paragraph_format.space_after = Pt(10)

    h1 = doc.styles["Heading 1"]
    black(h1, Pt(17), bold=True)
    strip_paragraph_borders(h1)
    h1.paragraph_format.space_before = Pt(20)
    h1.paragraph_format.space_after = Pt(8)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    black(h2, Pt(13.5), bold=True)
    strip_paragraph_borders(h2)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True

    h3 = doc.styles["Heading 3"]
    black(h3, Pt(11), bold=True)
    strip_paragraph_borders(h3)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True

    code = doc.styles.add_style("CodeBlock", 1)  # 1 = paragraph style
    code.base_style = doc.styles["Normal"]
    code.font.name = CODE_FONT
    code.font.size = CODE_SIZE
    code.font.color.rgb = RGBColor(0x11, 0x1A, 0x2E)
    rpr = code.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), CODE_FONT)
    pf = code.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(10)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = CODE_LINE
    pf.left_indent = Cm(0.3)
    pf.keep_together = False

    caption = doc.styles.add_style("FileNote", 1)
    caption.base_style = doc.styles["Normal"]
    caption.font.size = Pt(9.5)
    caption.font.italic = True
    caption.font.color.rgb = RGBColor(0x40, 0x4A, 0x60)
    caption.paragraph_format.space_after = Pt(4)


def page_setup(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.9)
    section.bottom_margin = Cm(1.9)
    section.left_margin = Cm(1.9)
    section.right_margin = Cm(1.9)

    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(4)
    run = paragraph.add_run()
    run.font.size = Pt(8.5)
    run.font.name = BODY_FONT
    run.font.color.rgb = RGBColor(0x5A, 0x64, 0x78)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)


def shade_cell(cell, fill) -> None:
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def set_borders(table, color=BORDER_GREY, size="6") -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)
        borders.append(element)
    tbl_pr.append(borders)


def set_cell_margins(table, top=60, start=90, bottom=60, end=90) -> None:
    tbl_pr = table._tbl.tblPr
    margin = OxmlElement("w:tblCellMar")
    for tag, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        element = OxmlElement(f"w:{tag}")
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")
        margin.append(element)
    tbl_pr.append(margin)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    element = OxmlElement("w:tblHeader")
    element.set(qn("w:val"), "true")
    tr_pr.append(element)


def add_code(doc: Document, text: str) -> None:
    """One paragraph per code block; line breaks keep it compact and page-splittable."""
    lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
    paragraph = doc.add_paragraph(style="CodeBlock")
    run = paragraph.add_run(lines[0])
    for line in lines[1:]:
        run.add_break()
        run.add_text(line)


def add_table(doc, header, rows, widths, font_size=Pt(9), header_size=Pt(9)):
    table = doc.add_table(rows=1, cols=len(header))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    set_borders(table)
    set_cell_margins(table)
    repeat_header(table.rows[0])

    for index, text in enumerate(header):
        cell = table.rows[0].cells[index]
        cell.width = Cm(widths[index])
        shade_cell(cell, HEADER_FILL)
        paragraph = cell.paragraphs[0]
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(text)
        run.bold = True
        run.font.size = header_size
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = BODY_FONT

    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for col_index, text in enumerate(row):
            cell = cells[col_index]
            cell.width = Cm(widths[col_index])
            if row_index % 2 == 1:
                shade_cell(cell, ROW_TINT)
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.line_spacing = 1.05
            run = paragraph.add_run(str(text))
            run.font.size = font_size
            run.font.name = BODY_FONT
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_bullets(doc, items) -> None:
    for item in items:
        paragraph = doc.add_paragraph(item, style="List Bullet")
        paragraph.paragraph_format.space_after = Pt(3)


def add_numbers(doc, items) -> None:
    for item in items:
        paragraph = doc.add_paragraph(item, style="List Number")
        paragraph.paragraph_format.space_after = Pt(3)


def add_file(doc: Document, rel_path: str, note: str = "") -> None:
    path = ROOT / rel_path
    doc.add_heading(rel_path, level=3)
    if note:
        paragraph = doc.add_paragraph(style="FileNote")
        paragraph.add_run(note)
    add_code(doc, path.read_text(encoding="utf-8"))


def page_break(doc) -> None:
    doc.add_page_break()


# --------------------------------------------------------------------------- #
# document content
# --------------------------------------------------------------------------- #
def build(page_map: dict) -> None:
    doc = Document()
    configure_styles(doc)
    page_setup(doc)

    doc.add_paragraph("BankFlow AI Banking Assistant Complete Setup Guide and Source Code", style="Title")
    doc.add_paragraph(
        "BankFlow is a demonstration banking application built with React, Vite and Material UI on "
        "the front end and Django, Django REST Framework and JWT on the back end. This document "
        "contains every step required to create the project on a new computer, followed by the "
        "complete source code of all 96 files in the order you create them."
    )
    doc.add_paragraph(
        "Work through the steps in sequence. Each step explains what you are building and why, "
        "lists the commands to run, and then gives the files for that step with their full code. "
        "After the backend steps you have a working API with three fictional customers and "
        "twenty-eight transactions. After the frontend steps you have a website you can demonstrate "
        "in about ten minutes."
    )
    doc.add_paragraph(
        "Every account, transaction, loan and notification in BankFlow is fictional. The "
        "application never moves real money and must not be used with real banking credentials."
    )

    # ------------------------------------------------------------------ contents
    doc.add_heading("Contents", level=1)
    contents = [
        ("Step 1. Install the required software", "step1"),
        ("Step 2. Create the project folders", "step2"),
        ("Step 3. Create the Django project and virtual environment", "step3"),
        ("Step 4. Backend configuration files", "step4"),
        ("Step 5. Build the users app for authentication and profiles", "step5"),
        ("Step 6. Build the banking app for accounts, transactions and loans", "step6"),
        ("Step 7. Build the assistant app with the AI service", "step7"),
        ("Step 8. Create the database and load the demo data", "step8"),
        ("Step 9. Run the backend test suite", "step9"),
        ("Step 10. Check the API by hand", "step10"),
        ("Step 11. Create the React frontend and install packages", "step11"),
        ("Step 12. Frontend project files", "step12"),
        ("Step 13. API layer, authentication context and helpers", "step13"),
        ("Step 14. Shared components", "step14"),
        ("Step 15. Customer pages", "step15"),
        ("Step 16. Bank employee pages", "step16"),
        ("Step 17. Build the production bundle", "step17"),
        ("Step 18. Run the whole application", "step18"),
        ("Step 19. Demo logins and the ten minute demo script", "step19"),
        ("Step 20. Troubleshooting", "step20"),
        ("Appendix A. API endpoint reference", "appendixa"),
        ("Appendix B. Complete file manifest", "appendixb"),
        ("Appendix C. Database models and relationships", "appendixc"),
        ("Appendix D. Deployment notes and future improvements", "appendixd"),
    ]
    for index, (label, key) in enumerate(contents, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.tab_stops.add_tab_stop(
            Cm(17.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        paragraph.add_run(f"{index}. {label}")
        page = page_map.get(key)
        if page:
            paragraph.add_run(f"\t{page}")

    page_break(doc)

    # ------------------------------------------------------------------- step 1
    doc.add_heading("Step 1. Install the required software", level=1)
    doc.add_paragraph(
        "Install the two runtimes the project depends on and confirm the versions before you "
        "create any files. The versions below are the ones this project was built and tested with. "
        "Any newer minor release works as well."
    )
    add_table(
        doc,
        ["Tool", "Version used here", "How to check", "Why the project needs it"],
        [
            ["Python", "3.14.5 (3.10 or newer)", "python --version",
             "Runs Django, the REST API, the seed command and the test suite"],
            ["Node.js", "24.19.0 (18 or newer)", "node --version",
             "Runs Vite and builds the React front end"],
            ["npm", "12.0.2", "npm --version", "Installs the frontend packages"],
            ["A code editor", "Visual Studio Code", "-",
             "Creates and edits the project files"],
            ["A web browser", "Chrome or Edge", "-",
             "Opens the demo website at http://localhost:5173"],
        ],
        [2.9, 3.6, 3.6, 7.1],
    )
    doc.add_paragraph(
        "Open a terminal in the folder where you want the project to live and check both runtimes."
    )
    add_code(
        doc,
        "python --version\n"
        "node --version\n"
        "npm --version",
    )

    # ------------------------------------------------------------------- step 2
    doc.add_heading("Step 2. Create the project folders", level=1)
    doc.add_paragraph(
        "BankFlow keeps the API and the website in two sibling folders so each one can be started "
        "and deployed on its own. Create the structure now; every later step adds files inside it."
    )
    add_code(
        doc,
        "mkdir banking_app\n"
        "cd banking_app\n"
        "mkdir backend\n"
        "mkdir frontend",
    )
    doc.add_paragraph(
        "After all the steps in this document the folder looks like the tree below. Files marked "
        "generated are produced by commands rather than typed by hand."
    )
    add_code(
        doc,
        "banking_app/\n"
        "  README.md\n"
        "  backend/\n"
        "    manage.py\n"
        "    requirements.txt\n"
        "    .env  .env.example\n"
        "    db.sqlite3                 (generated)\n"
        "    config/                    settings.py, urls.py, wsgi.py, asgi.py\n"
        "    users/                     models, serializers, views, urls, admin, tests\n"
        "    banking/                   models, services, serializers, views, admin_views, urls,\n"
        "                               management/commands/seed_demo.py, tests\n"
        "    assistant/                 models, ai_service, serializers, views, urls, tests\n"
        "  frontend/\n"
        "    index.html  package.json  vite.config.js  .env\n"
        "    public/bankflow.svg\n"
        "    src/\n"
        "      main.jsx  App.jsx  theme.js  index.css\n"
        "      components/  context/  services/  utils/  pages/  pages/admin/",
    )

    # ------------------------------------------------------------------- step 3
    doc.add_heading("Step 3. Create the Django project and virtual environment", level=1)
    doc.add_paragraph(
        "A virtual environment keeps the backend packages separate from every other Python "
        "project on the machine. Create it inside the backend folder, activate it, and install the "
        "five packages the API needs."
    )
    add_code(
        doc,
        "cd banking_app/backend\n"
        "python -m venv venv\n"
        "\n"
        "# Windows\n"
        "venv\\Scripts\\activate\n"
        "\n"
        "# macOS or Linux\n"
        "source venv/bin/activate",
    )
    doc.add_paragraph(
        "With the environment active, install the dependencies. The same packages are listed in "
        "requirements.txt in Step 4, so you can either run this command once or create the file "
        "first and run pip install -r requirements.txt."
    )
    add_code(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 \\\n"
        "            django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
    )
    doc.add_paragraph(
        "psycopg is only needed if you later switch the database to PostgreSQL. Installing it now "
        "keeps the switch to a single environment variable."
    )

    # ------------------------------------------------------------------- step 4
    doc.add_heading("Step 4. Backend configuration files", level=1)
    doc.add_paragraph(
        "The configuration package holds the project settings, the root URL map and the server "
        "entry points. Create the files below exactly as shown; the comments explain each "
        "decision, including how to switch from SQLite to PostgreSQL and how the JWT lifetimes "
        "are set."
    )
    add_file(doc, "backend/requirements.txt", "Pinned backend dependencies.")
    add_file(
        doc,
        "backend/.env.example",
        "Template for the environment file. Copy it to .env and change the values.",
    )
    add_file(doc, "backend/manage.py", "Django command line entry point.")
    add_file(doc, "backend/.gitignore", "Keeps the virtual environment, secrets and database out of git.")
    add_file(doc, "backend/config/__init__.py", "Marks the configuration folder as a Python package.")
    add_file(
        doc,
        "backend/config/settings.py",
        "Project settings: apps, middleware, database switch, JWT, CORS and the AI provider.",
    )
    add_file(
        doc,
        "backend/config/urls.py",
        "Root URL map that wires each app's urls module to its API prefix.",
    )
    add_file(doc, "backend/config/wsgi.py", "WSGI entry point used by production servers.")
    add_file(doc, "backend/config/asgi.py", "ASGI entry point for asynchronous servers.")
    doc.add_paragraph(
        "Copy the environment template so Django can read the secret key, the database choice and "
        "the optional AI settings."
    )
    add_code(doc, "copy .env.example .env        # cp .env.example .env on macOS or Linux")

    # ------------------------------------------------------------------- step 5
    doc.add_heading("Step 5. Build the users app for authentication and profiles", level=1)
    doc.add_paragraph(
        "The users app replaces the default Django user with one that logs in by email and carries "
        "a role field, so the same API can serve customers and bank employees. A profile model "
        "stores the contact and employment details the bank employee area displays."
    )
    doc.add_heading("Models, permissions and signals", level=2)
    doc.add_paragraph(
        "User is an AbstractUser with no username field, an email that must be unique, and a role "
        "that is either CUSTOMER or ADMIN. CustomerProfile is a one-to-one extension created "
        "automatically by a signal, so every user always has a complete profile object."
    )
    add_file(doc, "backend/users/__init__.py")
    add_file(doc, "backend/users/apps.py", "Registers the signal module when the app becomes ready.")
    add_file(doc, "backend/users/models.py", "User manager, User model and CustomerProfile.")
    add_file(doc, "backend/users/signals.py", "Creates a profile for every new user.")
    add_file(doc, "backend/users/permissions.py", "IsBankStaff guard for the employee endpoints.")
    doc.add_heading("Serializers, views and URLs", level=2)
    doc.add_paragraph(
        "The serializers validate registration, keep passwords hashed and restrict profile "
        "updates to the fields a customer is allowed to change. The views expose registration, "
        "profile read and profile update."
    )
    add_file(doc, "backend/users/serializers.py", "Registration, profile read and profile update.")
    add_file(doc, "backend/users/views.py", "Register and profile endpoints.")
    add_file(doc, "backend/users/urls/__init__.py")
    add_file(
        doc,
        "backend/users/urls/auth_urls.py",
        "Registration, login and refresh routes; login and refresh come from SimpleJWT.",
    )
    add_file(doc, "backend/users/urls/profile_urls.py", "The /api/profile/ route.")
    add_file(doc, "backend/users/admin.py", "Django admin registration for users and profiles.")
    add_file(
        doc,
        "backend/users/tests.py",
        "Tests for registration, duplicate email rejection, login and profile updates.",
    )

    # ------------------------------------------------------------------- step 6
    doc.add_heading("Step 6. Build the banking app for accounts, transactions and loans", level=1)
    doc.add_paragraph(
        "This is the core app. It holds the four banking models, the business logic that every "
        "screen and the AI assistant share, the customer API and the bank employee API."
    )
    doc.add_heading("Models and business logic", level=2)
    doc.add_paragraph(
        "Account holds the masked demo account, Transaction records every movement with a running "
        "balance, Loan stores the application, EMI, tenure and outstanding amount, and "
        "Notification carries the simulated alerts. services.py keeps all the arithmetic in one "
        "place: the EMI formula, month boundaries, period totals, category breakdowns, the six "
        "month trend, the ledger rebuild used by the seed command, and the demo transaction list."
    )
    add_file(doc, "backend/banking/__init__.py")
    add_file(doc, "backend/banking/apps.py")
    add_file(doc, "backend/banking/models.py", "Account, Transaction, Loan and Notification.")
    add_file(
        doc,
        "backend/banking/services.py",
        "Shared business logic: EMI, dashboard totals, category analysis, trends, seed ledger.",
    )
    doc.add_heading("Serializers and customer API", level=2)
    doc.add_paragraph(
        "The serializers turn the models into the JSON the React pages expect, including display "
        "labels and computed fields such as the masked account number and the loan progress. The "
        "views expose the dashboard, account, transaction, loan, EMI and notification endpoints."
    )
    add_file(doc, "backend/banking/serializers.py")
    add_file(doc, "backend/banking/views.py", "Customer endpoints, all JWT protected.")
    add_file(doc, "backend/banking/urls/__init__.py")
    add_file(doc, "backend/banking/urls/customer_urls.py")
    doc.add_heading("Bank employee API", level=2)
    doc.add_paragraph(
        "The employee endpoints reuse the same models but skip the per-customer filter, and every "
        "view requires the ADMIN role. The analytics view aggregates the whole portfolio; the loan "
        "endpoint approves, activates or rejects an application and writes a notification for the "
        "customer."
    )
    add_file(doc, "backend/banking/admin_views.py", "Admin dashboard, customer, loan and user APIs.")
    add_file(doc, "backend/banking/urls/admin_urls.py")
    add_file(doc, "backend/banking/admin.py", "Django admin registrations for the banking models.")
    doc.add_heading("Management command and tests", level=2)
    doc.add_paragraph(
        "The seed command creates the three fictional customers, their accounts, twenty-eight "
        "transactions across three months, six loan applications, the notification list and a "
        "saved AI conversation. It is written so the demo numbers always match the script: the "
        "balance is Rs 85,450, monthly income is Rs 45,000, monthly expenses are Rs 18,450 and the "
        "largest category is Shopping at Rs 7,200."
    )
    add_file(doc, "backend/banking/management/__init__.py")
    add_file(doc, "backend/banking/management/commands/__init__.py")
    add_file(
        doc,
        "backend/banking/management/commands/seed_demo.py",
        "Creates every piece of fictional demo data. Run it with python manage.py seed_demo --flush.",
    )
    add_file(
        doc,
        "backend/banking/tests.py",
        "Tests for the dashboard totals, filters, loan application, EMI endpoint and admin access.",
    )

    # ------------------------------------------------------------------- step 7
    doc.add_heading("Step 7. Build the assistant app with the AI service", level=1)
    doc.add_paragraph(
        "The assistant app stores conversations and holds the AI service. The service is split so "
        "the language model is optional: intent detection and data retrieval always run locally, "
        "and the rule based answers produce the response whenever no external key is configured."
    )
    doc.add_heading("Conversation model and AI service", level=2)
    doc.add_paragraph(
        "ChatMessage stores one question and one answer with its intent type and the provider that "
        "produced it, which is what the employee monitoring screen reads. ai_service.py exposes "
        "answer(), which detects the intent, builds a grounded snapshot of the customer data, asks "
        "the model if one is configured, and otherwise answers from the rule based engine. It also "
        "holds the banking knowledge base used for questions such as what is KYC or what is a "
        "credit score."
    )
    add_file(doc, "backend/assistant/__init__.py")
    add_file(doc, "backend/assistant/apps.py")
    add_file(doc, "backend/assistant/models.py", "ChatMessage model used for history and monitoring.")
    add_file(
        doc,
        "backend/assistant/ai_service.py",
        "Intent detection, data grounding, rule based fallback answers and the optional LLM call.",
    )
    doc.add_heading("Assistant API", level=2)
    doc.add_paragraph(
        "The chat view validates the question, calls the service, saves the exchange and returns "
        "the answer with its type and data. The history view returns the saved conversation and "
        "the suggestion list; the monitor view is restricted to bank employees."
    )
    add_file(doc, "backend/assistant/serializers.py")
    add_file(doc, "backend/assistant/views.py")
    add_file(doc, "backend/assistant/urls.py")
    add_file(doc, "backend/assistant/admin.py")
    add_file(
        doc,
        "backend/assistant/tests.py",
        "Tests every assistant intent, the saved history and the employee only monitor endpoint.",
    )

    # ------------------------------------------------------------------- step 8
    doc.add_heading("Step 8. Create the database and load the demo data", level=1)
    doc.add_paragraph(
        "Generate the migrations for the three apps, apply them to create the SQLite database, and "
        "run the seed command. The --flush flag clears any earlier demo data first, so the command "
        "can be repeated at any time to return to a known state."
    )
    add_code(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
    )
    doc.add_paragraph(
        "The seed command prints the demo logins when it finishes. The expected output looks like "
        "this."
    )
    add_code(
        doc,
        "Seeded customer Mohammed Adnan\n"
        "Seeded customer Aisha Khan\n"
        "Seeded customer Rahul Verma\n"
        "\n"
        "Demo data ready.\n"
        "Admin    : admin@bankflow.com / Admin@12345\n"
        "Customer : mohammed@bankflow.com / Demo@12345\n"
        "Customer : aisha@bankflow.com / Demo@12345\n"
        "Customer : rahul@bankflow.com / Demo@12345",
    )
    doc.add_paragraph(
        "The same data is available in the Django admin at http://127.0.0.1:8000/admin/ using the "
        "admin account."
    )

    # ------------------------------------------------------------------- step 9
    doc.add_heading("Step 9. Run the backend test suite", level=1)
    doc.add_paragraph(
        "Django creates a separate test database, seeds nothing, and runs twenty-five tests that "
        "create their own data. The suite covers registration and login, profile updates, dashboard "
        "totals, transaction filters, loan applications, the EMI endpoint, notification state, the "
        "employee permission boundary and every assistant intent."
    )
    add_code(doc, "python manage.py test")
    doc.add_paragraph("A healthy run ends with this output.")
    add_code(
        doc,
        "Found 25 test(s).\n"
        "System check identified no issues (0 silenced).\n"
        "Creating test database for alias 'default'...\n"
        ".........................\n"
        "----------------------------------------------------------------------\n"
        "Ran 25 tests in 31.331s\n"
        "\n"
        "OK\n"
        "Destroying test database for alias 'default'...",
    )

    # ------------------------------------------------------------------ step 10
    doc.add_heading("Step 10. Check the API by hand", level=1)
    doc.add_paragraph(
        "Start the development server and confirm the endpoints answer before you build the "
        "website on top of them."
    )
    add_code(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "In a second terminal, log in as the demo customer and call the dashboard, the transaction "
        "filter and the assistant. This is PowerShell; the curl equivalents follow."
    )
    add_code(
        doc,
        "$base = 'http://127.0.0.1:8000/api'\n"
        "$login = Invoke-RestMethod -Method Post -Uri \"$base/auth/login/\" -ContentType 'application/json' `\n"
        "  -Body (@{ email = 'mohammed@bankflow.com'; password = 'Demo@12345' } | ConvertTo-Json)\n"
        "$headers = @{ Authorization = \"Bearer $($login.access)\" }\n"
        "\n"
        "Invoke-RestMethod -Uri \"$base/dashboard/\" -Headers $headers\n"
        "Invoke-RestMethod -Uri \"$base/transactions/?category=Shopping&type=DEBIT\" -Headers $headers\n"
        "Invoke-RestMethod -Method Post -Uri \"$base/assistant/chat/\" -Headers $headers `\n"
        "  -ContentType 'application/json' -Body (@{ message = 'What is my balance?' } | ConvertTo-Json)",
    )
    add_code(
        doc,
        "# curl version\n"
        "TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        "  -d '{\"email\":\"mohammed@bankflow.com\",\"password\":\"Demo@12345\"}' | python -c \\\n"
        "  'import sys,json;print(json.load(sys.stdin)[\"access\"])')\n"
        "\n"
        "curl -s http://127.0.0.1:8000/api/dashboard/ -H \"Authorization: Bearer $TOKEN\"\n"
        "curl -s -X POST http://127.0.0.1:8000/api/assistant/chat/ -H \"Authorization: Bearer $TOKEN\" \\\n"
        "  -H 'Content-Type: application/json' -d '{\"message\":\"How much did I spend this month?\"}'",
    )
    doc.add_paragraph("The dashboard response starts with these values.")
    add_code(
        doc,
        '{"balance": 85450.0, "monthly_income": 45000.0, "monthly_expenses": 18450.0,\n'
        ' "monthly_savings": 26550.0, "active_loans": 2, "total_outstanding": 1137500.0,\n'
        ' "top_category": {"category": "Shopping", "amount": 7200.0, "color": "#8b5cf6"}, ...}',
    )
    doc.add_paragraph("The assistant response for the spending question looks like this.")
    add_code(
        doc,
        '{"response": "You spent Rs 18,450 this month. Your income for the month is Rs 45,000, "\n'
        '             "so your net savings are Rs 26,550.",\n'
        ' "type": "expense_summary", "intent": "expense_summary", "provider": "fallback",\n'
        ' "data": {"amount": 18450.0, "income": 45000.0, "savings": 26550.0}}',
    )

    # ------------------------------------------------------------------ step 11
    doc.add_heading("Step 11. Create the React frontend and install packages", level=1)
    doc.add_paragraph(
        "The website is a Vite project using React 18, Material UI for the components, Recharts for "
        "the charts, Axios for API calls and React Router for navigation. Create the project and "
        "install the packages, then replace the generated files with the ones in Step 12."
    )
    add_code(
        doc,
        "cd banking_app\n"
        "npm create vite@latest frontend -- --template react\n"
        "cd frontend\n"
        "\n"
        "npm install\n"
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
    )
    doc.add_paragraph(
        "If your npm policy blocks package install scripts, approve them and re-run the install:"
    )
    add_code(doc, "npm install-scripts approve esbuild\nnpm install")

    # ------------------------------------------------------------------ step 12
    doc.add_heading("Step 12. Frontend project files", level=1)
    doc.add_paragraph(
        "These files define the Vite build, the HTML shell, the theme tokens and the route map. "
        "Replace package.json, index.html and vite.config.js with the versions below, and add the "
        "theme, stylesheet, entry point and route file."
    )
    add_file(doc, "frontend/package.json", "Scripts and dependency list for the front end.")
    add_file(doc, "frontend/vite.config.js", "Vite configuration: React plugin and dev server port.")
    add_file(doc, "frontend/index.html", "HTML shell that mounts the React application.")
    add_file(doc, "frontend/.env.example", "Template for the API base URL.")
    add_file(doc, "frontend/.gitignore", "Keeps node_modules, the build output and secrets out of git.")
    add_file(doc, "frontend/public/bankflow.svg", "Favicon used by the browser tab.")
    add_file(doc, "frontend/src/index.css", "Global styles and the small fade-in animation.")
    add_file(
        doc,
        "frontend/src/theme.js",
        "Material UI theme: navy banking palette, rounded corners, card and button defaults.",
    )
    add_file(doc, "frontend/src/main.jsx", "React entry point with the theme, router and auth provider.")
    add_file(
        doc,
        "frontend/src/App.jsx",
        "Route map: public pages, the protected customer area and the employee area.",
    )
    doc.add_paragraph(
        "Copy the environment template so the front end knows where the API lives."
    )
    add_code(doc, "copy .env.example .env        # cp .env.example .env on macOS or Linux")

    # ------------------------------------------------------------------ step 13
    doc.add_heading("Step 13. API layer, authentication context and helpers", level=1)
    doc.add_paragraph(
        "All network access goes through one Axios instance. It adds the JWT access token to every "
        "request, refreshes the token once when the API answers 401, signs the user out when the "
        "refresh fails, and converts any failure into a sentence the interface can display. The "
        "auth context keeps the signed-in user in React state and rehydrates it from the stored "
        "token when the page reloads."
    )
    add_file(doc, "frontend/src/services/api.js", "Axios instance, token store, refresh logic, error mapping.")
    add_file(doc, "frontend/src/services/authService.js", "Register, login, profile and logout calls.")
    add_file(doc, "frontend/src/services/bankingService.js", "Dashboard, account, transactions, loans, EMI, notifications.")
    add_file(doc, "frontend/src/services/aiService.js", "Chat, history, suggestions and clear history.")
    add_file(doc, "frontend/src/services/adminService.js", "Employee analytics, customers, loans, users and AI monitor.")
    add_file(doc, "frontend/src/context/AuthContext.jsx", "Authentication state, login, logout and role flags.")
    add_file(
        doc,
        "frontend/src/utils/formatCurrency.js",
        "Rupee, date, relative time and greeting formatting plus shared category and loan constants.",
    )
    add_file(
        doc,
        "frontend/src/utils/calculations.js",
        "Client side EMI, amortisation schedule and tenure label for instant feedback.",
    )

    # ------------------------------------------------------------------ step 14
    doc.add_heading("Step 14. Shared components", level=1)
    doc.add_paragraph(
        "The components build the application shell and the repeated pieces used by several pages: "
        "the responsive sidebar and app bar, the four statistic cards, the transaction table that "
        "both the customer and employee pages reuse, the loan card, the chat bubble, the route "
        "guard and a small set of layout helpers."
    )
    add_file(doc, "frontend/src/components/AppLayout.jsx", "Sidebar, app bar and page container.")
    add_file(doc, "frontend/src/components/Navbar.jsx", "App bar with page title, notifications and profile menu.")
    add_file(doc, "frontend/src/components/Sidebar.jsx", "Role aware navigation drawer that collapses on mobile.")
    add_file(doc, "frontend/src/components/DashboardCard.jsx", "Statistic card with icon, value and trend.")
    add_file(doc, "frontend/src/components/TransactionTable.jsx", "Reusable transaction table with loading and empty states.")
    add_file(doc, "frontend/src/components/LoanCard.jsx", "Loan summary card with progress and details link.")
    add_file(doc, "frontend/src/components/ChatMessage.jsx", "User and assistant chat bubbles.")
    add_file(doc, "frontend/src/components/ProtectedRoute.jsx", "Route guard for signed-in and employee only routes.")
    add_file(
        doc,
        "frontend/src/components/Common.jsx",
        "Page header, loader, error alert, empty state, status chip and section card.",
    )

    # ------------------------------------------------------------------ step 15
    doc.add_heading("Step 15. Customer pages", level=1)
    doc.add_paragraph(
        "These fourteen pages make up the customer experience, from the public landing page "
        "through to the AI assistant. The table lists what each page does and which API endpoints "
        "it calls."
    )
    add_table(
        doc,
        ["Page", "Route", "API endpoints used"],
        [
            ["Landing", "/", "none (static marketing page with demo logins)"],
            ["Login", "/login", "POST /api/auth/login/, GET /api/profile/"],
            ["Register", "/register", "POST /api/auth/register/"],
            ["Dashboard", "/dashboard", "GET /api/dashboard/, GET /api/notifications/"],
            ["Account", "/account", "GET /api/account/"],
            ["Transactions", "/transactions", "GET /api/transactions/ with filters and paging"],
            ["Transaction details", "/transactions/:id", "GET /api/transactions/<id>/"],
            ["Loans", "/loans", "GET /api/loans/, POST /api/loans/"],
            ["Loan details", "/loans/:id", "GET /api/loans/<id>/"],
            ["EMI calculator", "/emi-calculator", "POST /api/emi/ (verifies the local maths)"],
            ["AI assistant", "/assistant", "POST /api/assistant/chat/, GET and DELETE /api/assistant/history/"],
            ["Notifications", "/notifications", "GET /api/notifications/, PUT /api/notifications/<id>/"],
            ["Profile", "/profile", "GET /api/profile/, PUT /api/profile/"],
            ["Not found", "any unknown route", "none"],
        ],
        [3.9, 3.9, 9.4],
    )
    add_file(
        doc,
        "frontend/src/pages/Landing.jsx",
        "Public landing page with hero, feature cards, assistant preview, security and demo logins.",
    )
    add_file(doc, "frontend/src/pages/Login.jsx", "JWT login with demo autofill, validation and redirect by role.")
    add_file(doc, "frontend/src/pages/Register.jsx", "Registration form with client side validation.")
    add_file(
        doc,
        "frontend/src/pages/Dashboard.jsx",
        "KPI cards, quick actions, four Recharts charts, recent transactions and notifications.",
    )
    add_file(doc, "frontend/src/pages/Account.jsx", "Masked account card and account information list.")
    add_file(
        doc,
        "frontend/src/pages/Transactions.jsx",
        "Search, category, type and date filters, sorting, pagination and filtered totals.",
    )
    add_file(doc, "frontend/src/pages/TransactionDetails.jsx", "Single transaction view with the resulting balance.")
    add_file(
        doc,
        "frontend/src/pages/Loans.jsx",
        "Status tabs, totals and the demo loan application dialog with a live EMI preview.",
    )
    add_file(
        doc,
        "frontend/src/pages/LoanDetails.jsx",
        "Loan summary, progress bar, application details and the first twelve instalments.",
    )
    add_file(
        doc,
        "frontend/src/pages/EMICalculator.jsx",
        "Sliders and inputs, result cards, principal versus interest chart and server verification.",
    )
    add_file(
        doc,
        "frontend/src/pages/AIAssistant.jsx",
        "Chat interface with history panel, suggestion chips, typing state and error handling.",
    )
    add_file(doc, "frontend/src/pages/Notifications.jsx", "Read and unread tabs with mark read and mark all read.")
    add_file(doc, "frontend/src/pages/Profile.jsx", "Profile card and editable contact details.")
    add_file(doc, "frontend/src/pages/NotFound.jsx", "Friendly 404 page with routes back into the application.")

    # ------------------------------------------------------------------ step 16
    doc.add_heading("Step 16. Bank employee pages", level=1)
    doc.add_paragraph(
        "The employee area is guarded by the ADMIN role. These six pages reuse the components from "
        "Step 14 and read the admin endpoints, which return data for every customer."
    )
    add_table(
        doc,
        ["Page", "Route", "API endpoints used"],
        [
            ["Admin dashboard", "/admin", "GET /api/admin/analytics/"],
            ["Customer management", "/admin/customers", "GET /api/admin/customers/, GET /api/admin/customers/<id>/"],
            ["Transaction management", "/admin/transactions", "GET /api/admin/transactions/ with filters"],
            ["Loan management", "/admin/loans", "GET /api/admin/loans/, PATCH /api/admin/loans/<id>/"],
            ["Analytics", "/admin/analytics", "GET /api/admin/analytics/"],
            ["AI monitoring", "/admin/ai-monitor", "GET /api/assistant/monitor/"],
        ],
        [4.2, 4.2, 8.8],
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AdminDashboard.jsx",
        "Six KPI cards, portfolio charts and the top customers table.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/CustomerManagement.jsx",
        "Searchable customer table and a customer 360 dialog.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/TransactionManagement.jsx",
        "Portfolio wide transaction table with the same filters as the customer page.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/LoanManagement.jsx",
        "Loan table with approve, activate and reject actions that notify the customer.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AdminAnalytics.jsx",
        "Trend, category, transaction count and active loan ratio charts with a summary grid.",
    )
    add_file(
        doc,
        "frontend/src/pages/admin/AIMonitor.jsx",
        "Assistant monitoring: totals, intent breakdown and the full question log.",
    )

    # ------------------------------------------------------------------ step 17
    doc.add_heading("Step 17. Build the production bundle", level=1)
    doc.add_paragraph(
        "Vite compiles the React application into static files in dist/. Run this whenever you want "
        "to confirm the code still builds cleanly."
    )
    add_code(doc, "npm run build\nnpm run preview      # serves the production bundle locally")
    doc.add_paragraph("The build output lists the bundle files and their gzip sizes.")
    add_code(
        doc,
        "vite v5.4.21 building for production...\n"
        "transforming...\n"
        "checkmark 1868 modules transformed.\n"
        "dist/index.html                     0.62 kB gzip:   0.37 kB\n"
        "dist/assets/index-BYgGbjXY.css      0.50 kB gzip:   0.32 kB\n"
        "dist/assets/index-CX94YJLq.js   1,142.96 kB gzip: 331.14 kB\n"
        "checkmark built in 26.53s",
    )

    # ------------------------------------------------------------------ step 18
    doc.add_heading("Step 18. Run the whole application", level=1)
    doc.add_paragraph(
        "Start the API and the website in two terminals. Keep both running while you demonstrate "
        "the application."
    )
    add_code(
        doc,
        "# terminal 1 - backend\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000\n"
        "\n"
        "# terminal 2 - frontend\n"
        "cd banking_app/frontend\n"
        "npm run dev",
    )
    doc.add_paragraph(
        "Open http://localhost:5173 for the website and http://127.0.0.1:8000/api/ for the API. "
        "The Django admin is at http://127.0.0.1:8000/admin/."
    )

    # ------------------------------------------------------------------ step 19
    doc.add_heading("Step 19. Demo logins and the ten minute demo script", level=1)
    add_table(
        doc,
        ["Role", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345",
             "Balance Rs 85,450, income Rs 45,000, expenses Rs 18,450, two active loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "Second customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "Third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "Employee dashboard and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Follow this sequence to demonstrate the project in about ten minutes.")
    add_numbers(
        doc,
        [
            "Open the landing page and point out the hero, the six feature cards, the assistant preview and the security section.",
            "Log in as mohammed@bankflow.com and land on the dashboard.",
            "Read the four statistic cards and the four charts, then use the quick actions.",
            "Open the account page and show the masked account number and the account status.",
            "Open transactions, filter by the Shopping category and by type, then open a transaction detail.",
            "Open loans, switch between the status tabs, and submit a new demo loan application with the live EMI preview.",
            "Open the EMI calculator, move the sliders and show the message that the Django API verified the result.",
            "Open the AI assistant and ask: What is my balance, How much did I spend this month, What was my biggest expense, What loans do I have, and Explain EMI. Show the history panel afterwards.",
            "Open notifications and mark one as read.",
            "Log out, log in as admin@bankflow.com and open the admin dashboard.",
            "Approve the pending loan in loan management and show the notification it creates for the customer.",
            "Open analytics and the AI monitoring page, then close on the architecture: React, Axios and JWT, Django REST Framework, the service layer, the database and the AI service.",
        ],
    )

    # ------------------------------------------------------------------ step 20
    doc.add_heading("Step 20. Troubleshooting", level=1)
    doc.add_paragraph(
        "These are the problems that come up most often when the project is set up on a new "
        "machine, with the cause and the fix."
    )
    add_table(
        doc,
        ["Symptom", "Likely cause", "Fix"],
        [
            ["The website shows a red banner about reaching the API",
             "The Django server is not running or the URL differs",
             "Start runserver on 127.0.0.1:8000 and check VITE_API_BASE_URL in frontend/.env"],
            ["Browser console reports a CORS error",
             "The frontend origin is missing from the allowed list",
             "Add it to CORS_ALLOWED_ORIGINS in backend/.env and restart the server"],
            ["Every request returns 401",
             "The access token expired and the refresh token is gone",
             "Log in again; tokens live in localStorage under bankflow_access and bankflow_refresh"],
            ["Login works but the dashboard is empty",
             "The demo data was never seeded",
             "Run python manage.py seed_demo --flush"],
            ["Command not found: manage.py",
             "The terminal is in the wrong folder",
             "cd into banking_app/backend before running manage.py"],
            ["port already in use",
             "Another process holds 8000 or 5173",
             "runserver 127.0.0.1:8001 and update VITE_API_BASE_URL, or stop the other process"],
            ["PostgreSQL connection refused",
             "DB_ENGINE is postgres but no server is running",
             "Set DB_ENGINE=sqlite in backend/.env, or start PostgreSQL and check the credentials"],
            ["npm install stops on blocked install scripts",
             "The package manager policy blocked esbuild",
             "Run npm install-scripts approve esbuild then npm install"],
            ["The assistant replies with the offline wording",
             "No external AI key is configured",
             "This is expected; set AI_PROVIDER=openai and OPENAI_API_KEY in backend/.env for model answers"],
            ["Charts render but the numbers look wrong",
             "The demo data was edited through the Django admin",
             "Run python manage.py seed_demo --flush to return to the documented values"],
        ],
        [5.2, 5.0, 7.0],
    )

    # -------------------------------------------------------------- appendix A
    page_break(doc)
    doc.add_heading("Appendix A. API endpoint reference", level=1)
    doc.add_paragraph(
        "Every endpoint accepts and returns JSON. Customer endpoints need the header "
        "Authorization: Bearer <access token>. Employee endpoints additionally require the ADMIN "
        "role and answer 403 for customers."
    )
    add_table(
        doc,
        ["Method", "Endpoint", "Purpose"],
        [
            ["POST", "/api/auth/register/", "Register a demo customer and create the demo account"],
            ["POST", "/api/auth/login/", "Return access and refresh tokens"],
            ["POST", "/api/auth/refresh/", "Exchange a refresh token for a new access token"],
            ["GET, PUT", "/api/profile/", "Read or update name, phone, address, occupation and income"],
            ["GET", "/api/dashboard/", "Balance, income, expenses, loans, categories, trend and recent transactions"],
            ["GET", "/api/account/", "Masked account number, type, status, branch and IFSC-like identifier"],
            ["GET", "/api/transactions/", "Paginated list; supports search, category, type, status, date and ordering"],
            ["GET", "/api/transactions/<id>/", "Single transaction with the resulting balance"],
            ["GET, POST", "/api/loans/", "List loans or submit a demo application"],
            ["GET", "/api/loans/<id>/", "Single loan with EMI and outstanding amount"],
            ["POST", "/api/emi/", "Server side EMI, total interest and total repayment"],
            ["GET", "/api/notifications/", "Notifications, optionally only unread"],
            ["PUT", "/api/notifications/<id>/", "Mark a notification read or unread"],
            ["POST", "/api/notifications/read-all/", "Mark every notification as read"],
            ["POST", "/api/assistant/chat/", "Ask the assistant and store the exchange"],
            ["GET, DELETE", "/api/assistant/history/", "Read or clear the saved conversation"],
            ["GET", "/api/assistant/suggestions/", "Suggested question chips"],
            ["GET", "/api/admin/analytics/", "Portfolio totals and every admin chart"],
            ["GET", "/api/admin/analytics/overview/", "The six KPI numbers used on the admin dashboard"],
            ["GET", "/api/admin/customers/", "Customer table, supports search"],
            ["GET", "/api/admin/customers/<id>/", "Customer 360 view with accounts, dashboard and loans"],
            ["GET", "/api/admin/transactions/", "All transactions with filters across every customer"],
            ["GET", "/api/admin/loans/", "All loans with status and type filters"],
            ["PATCH", "/api/admin/loans/<id>/", "Approve, activate or reject a loan and notify the customer"],
            ["GET", "/api/admin/users/", "User management table"],
            ["GET", "/api/assistant/monitor/", "Assistant totals, intent breakdown and the question log"],
        ],
        [2.2, 6.2, 8.8],
    )

    # -------------------------------------------------------------- appendix B
    doc.add_heading("Appendix B. Complete file manifest", level=1)
    doc.add_paragraph(
        "The manifest lists every file in the project with its purpose and length. Generated files "
        "are marked, because they are produced by the commands in Steps 8 and 11 rather than typed."
    )
    manifest = []
    for rel_path, purpose in MANIFEST:
        path = ROOT / rel_path
        lines = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
        manifest.append([rel_path, purpose, str(lines)])
    add_table(
        doc,
        ["Path", "Purpose", "Lines"],
        manifest,
        [6.4, 9.0, 1.8],
        font_size=Pt(8.5),
        header_size=Pt(8.5),
    )

    # -------------------------------------------------------------- appendix C
    doc.add_heading("Appendix C. Database models and relationships", level=1)
    doc.add_paragraph(
        "Seven models carry the whole application. The relationship chain is User to "
        "CustomerProfile to Account to Transaction, with loans, notifications and chat messages "
        "attached to the user."
    )
    add_code(
        doc,
        "User (users)\n"
        "  |-- CustomerProfile   one to one\n"
        "  |-- Account           one to many\n"
        "  |     '-- Transaction one to many\n"
        "  |-- Loan              one to many\n"
        "  |-- Notification      one to many\n"
        "  '-- ChatMessage       one to many",
    )
    add_table(
        doc,
        ["Model", "Key fields", "Relationships"],
        [
            ["User", "email (login), name, role, is_active", "Source of every customer record"],
            ["CustomerProfile", "phone, address, occupation, employment_type, monthly_income",
             "One to one with User"],
            ["Account", "account_number, account_type, balance, status, ifsc_code, branch",
             "Many to one with User, one to many with Transaction"],
            ["Transaction", "transaction_id, date, description, category, transaction_type, amount, status, balance_after",
             "Many to one with Account"],
            ["Loan", "loan_id, loan_type, amount, interest_rate, tenure_months, emi, remaining_amount, status, purpose, monthly_income",
             "Many to one with User"],
            ["Notification", "title, message, notification_type, is_read", "Many to one with User"],
            ["ChatMessage", "message, response, response_type, provider", "Many to one with User"],
        ],
        [3.2, 8.4, 5.6],
    )

    # -------------------------------------------------------------- appendix D
    doc.add_heading("Appendix D. Deployment notes and future improvements", level=1)
    doc.add_paragraph(
        "The development setup in this document is enough to run and demonstrate the project. The "
        "notes below cover what changes when the application is hosted, and which additions are "
        "worth building next."
    )
    add_bullets(
        doc,
        [
            "Set DJANGO_DEBUG=False, use a long random DJANGO_SECRET_KEY, and list only your real host names in DJANGO_ALLOWED_HOSTS.",
            "Run python manage.py collectstatic and serve the static files through a web server or a static host.",
            "Serve the React bundle produced by npm run build from any static host, and point VITE_API_BASE_URL at the deployed API.",
            "Switch to PostgreSQL with DB_ENGINE=postgres and keep the database credentials in environment variables, never in the repository.",
            "Add refresh token rotation and blacklisting, and enable two factor authentication for employee accounts.",
            "Stream assistant answers, add function calling so the model can query the API directly, and keep the rule based engine as the offline fallback.",
            "Add Celery and Redis for scheduled EMI reminders and monthly spending summaries.",
            "Replace notification polling with WebSockets and add statement export to CSV or PDF.",
            "Add Playwright end to end tests and a GitHub Actions workflow that runs the Django tests and the frontend build on every push.",
        ],
    )

    doc.save(OUTPUT)
    print(f"wrote {OUTPUT}")


# --------------------------------------------------------------------------- #
# file manifest used by Appendix B (path, purpose)
# --------------------------------------------------------------------------- #
MANIFEST = [
    ("backend/requirements.txt", "Pinned backend dependencies"),
    ("backend/.env.example", "Environment variable template"),
    ("backend/.gitignore", "Backend ignore rules"),
    ("backend/manage.py", "Django command line entry point"),
    ("backend/config/settings.py", "Project settings and app registration"),
    ("backend/config/urls.py", "Root URL map"),
    ("backend/config/wsgi.py", "WSGI entry point"),
    ("backend/config/asgi.py", "ASGI entry point"),
    ("backend/users/models.py", "User, role field and CustomerProfile"),
    ("backend/users/signals.py", "Auto creates a profile for new users"),
    ("backend/users/permissions.py", "IsBankStaff permission class"),
    ("backend/users/serializers.py", "Register, profile read and update serializers"),
    ("backend/users/views.py", "Register and profile endpoints"),
    ("backend/users/urls/auth_urls.py", "Register, login and refresh routes"),
    ("backend/users/urls/profile_urls.py", "Profile route"),
    ("backend/users/admin.py", "User and profile admin registration"),
    ("backend/users/tests.py", "Authentication and profile tests"),
    ("backend/banking/models.py", "Account, Transaction, Loan and Notification"),
    ("backend/banking/services.py", "EMI, dashboard, analytics and seed helpers"),
    ("backend/banking/serializers.py", "Banking API serializers"),
    ("backend/banking/views.py", "Customer API views"),
    ("backend/banking/admin_views.py", "Employee API views"),
    ("backend/banking/urls/customer_urls.py", "Customer routes"),
    ("backend/banking/urls/admin_urls.py", "Employee routes"),
    ("backend/banking/admin.py", "Banking model admin registration"),
    ("backend/banking/management/commands/seed_demo.py", "Creates all fictional demo data"),
    ("backend/banking/tests.py", "Banking API tests"),
    ("backend/assistant/models.py", "ChatMessage model"),
    ("backend/assistant/ai_service.py", "Intents, data grounding, rules and LLM hook"),
    ("backend/assistant/serializers.py", "Chat request and message serializers"),
    ("backend/assistant/views.py", "Chat, history, suggestions and monitor views"),
    ("backend/assistant/urls.py", "Assistant routes"),
    ("backend/assistant/admin.py", "Chat message admin registration"),
    ("backend/assistant/tests.py", "Assistant intent tests"),
    ("frontend/package.json", "Frontend scripts and dependencies"),
    ("frontend/vite.config.js", "Vite configuration"),
    ("frontend/index.html", "HTML shell"),
    ("frontend/.env.example", "Frontend environment template"),
    ("frontend/.gitignore", "Frontend ignore rules"),
    ("frontend/public/bankflow.svg", "Favicon"),
    ("frontend/src/index.css", "Global styles"),
    ("frontend/src/theme.js", "Material UI theme"),
    ("frontend/src/main.jsx", "React entry point"),
    ("frontend/src/App.jsx", "Route map"),
    ("frontend/src/services/api.js", "Axios instance, tokens and error mapping"),
    ("frontend/src/services/authService.js", "Authentication calls"),
    ("frontend/src/services/bankingService.js", "Banking calls"),
    ("frontend/src/services/aiService.js", "Assistant calls"),
    ("frontend/src/services/adminService.js", "Employee calls"),
    ("frontend/src/context/AuthContext.jsx", "Authentication state"),
    ("frontend/src/utils/formatCurrency.js", "Formatting helpers and constants"),
    ("frontend/src/utils/calculations.js", "EMI and amortisation helpers"),
    ("frontend/src/components/AppLayout.jsx", "Application shell"),
    ("frontend/src/components/Navbar.jsx", "Top app bar"),
    ("frontend/src/components/Sidebar.jsx", "Navigation drawer"),
    ("frontend/src/components/DashboardCard.jsx", "Statistic card"),
    ("frontend/src/components/TransactionTable.jsx", "Reusable transaction table"),
    ("frontend/src/components/LoanCard.jsx", "Loan summary card"),
    ("frontend/src/components/ChatMessage.jsx", "Chat bubble"),
    ("frontend/src/components/ProtectedRoute.jsx", "Route guard"),
    ("frontend/src/components/Common.jsx", "Shared layout primitives"),
    ("frontend/src/pages/Landing.jsx", "Public landing page"),
    ("frontend/src/pages/Login.jsx", "Login page"),
    ("frontend/src/pages/Register.jsx", "Registration page"),
    ("frontend/src/pages/Dashboard.jsx", "Customer dashboard with charts"),
    ("frontend/src/pages/Account.jsx", "Account details page"),
    ("frontend/src/pages/Transactions.jsx", "Transactions list with filters"),
    ("frontend/src/pages/TransactionDetails.jsx", "Transaction detail page"),
    ("frontend/src/pages/Loans.jsx", "Loans page and application dialog"),
    ("frontend/src/pages/LoanDetails.jsx", "Loan detail page"),
    ("frontend/src/pages/EMICalculator.jsx", "EMI calculator page"),
    ("frontend/src/pages/AIAssistant.jsx", "AI chat page"),
    ("frontend/src/pages/Notifications.jsx", "Notifications page"),
    ("frontend/src/pages/Profile.jsx", "Profile page"),
    ("frontend/src/pages/NotFound.jsx", "404 page"),
    ("frontend/src/pages/admin/AdminDashboard.jsx", "Employee dashboard"),
    ("frontend/src/pages/admin/CustomerManagement.jsx", "Customer management"),
    ("frontend/src/pages/admin/TransactionManagement.jsx", "Transaction management"),
    ("frontend/src/pages/admin/LoanManagement.jsx", "Loan management and decisions"),
    ("frontend/src/pages/admin/AdminAnalytics.jsx", "Analytics dashboard"),
    ("frontend/src/pages/admin/AIMonitor.jsx", "Assistant monitoring"),
]


def main() -> None:
    page_map = {}
    if len(sys.argv) > 1:
        # utf-8-sig tolerates the byte order mark that Windows PowerShell writes.
        page_map = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    build(page_map)


if __name__ == "__main__":
    main()
