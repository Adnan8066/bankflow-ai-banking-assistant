#!/usr/bin/env python3
"""Build the beginner edition of the BankFlow guide.

Same complete program as the reference guide, but written as numbered lessons that
start with installing VS Code on a brand new laptop. Every lesson ends with a check
so the reader always knows whether the previous step worked before moving on.

Usage: python build_beginner_docx.py [page-map.json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_bankflow_docx as base  # noqa: E402  (helper functions are shared)

from docx import Document  # noqa: E402
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

ROOT = base.ROOT
OUTPUT = ROOT / "BankFlow-Beginner-Step-by-Step-Guide-with-Full-Code.docx"


def add_goal(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run("Goal: ")
    run.bold = True
    paragraph.add_run(text)


def add_check(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run("Check: ")
    run.bold = True
    paragraph.add_run(text)


def add_note(doc, label: str, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run(f"{label}: ")
    run.bold = True
    paragraph.add_run(text)


def add_code_file(doc, rel_path: str, where: str, note: str = "") -> None:
    """Beginner framing: tell the reader where the file goes, then print it in full."""
    doc.add_heading(rel_path, level=3)
    frame = doc.add_paragraph(style="FileNote")
    frame.add_run(where)
    if note:
        doc.add_paragraph(style="FileNote").add_run(note)
    base.add_code(doc, (ROOT / rel_path).read_text(encoding="utf-8"))


def add_command_block(doc, title: str, command: str, expected: str = "") -> None:
    doc.add_paragraph(title).paragraph_format.space_after = Pt(2)
    base.add_code(doc, command)
    if expected:
        doc.add_paragraph("You should see something like this:").paragraph_format.space_after = Pt(2)
        base.add_code(doc, expected)


def build(page_map: dict) -> None:
    doc = Document()
    base.configure_styles(doc)
    doc.styles["Normal"].font.size = Pt(11)
    doc.styles["Normal"].paragraph_format.space_after = Pt(7)
    base.page_setup(doc)

    # ------------------------------------------------------------------- cover
    doc.add_paragraph("BankFlow Beginner Guide Build the Website Step by Step", style="Title")
    doc.add_paragraph(
        "This guide is written for someone who has never built a website before. It starts with an "
        "empty laptop, walks you through installing the tools, and then builds the complete BankFlow "
        "banking application one small lesson at a time. Every lesson tells you what to do, what you "
        "should see, and what to do when something goes wrong."
    )
    doc.add_paragraph(
        "The whole program is inside this document. You do not need to invent any code: each lesson "
        "shows a file and its complete contents, and you copy that file into the folder named above "
        "it. Nothing is left out and nothing is shortened."
    )
    doc.add_paragraph(
        "BankFlow is a practice project that uses pretend money. It has no connection to any real "
        "bank, so you can click anything you like without risk."
    )

    doc.add_heading("How to use this guide", level=1)
    doc.add_paragraph(
        "Read one lesson at a time and finish its check before starting the next one. The lessons are "
        "in order on purpose: the backend lessons must come before the website lessons, because the "
        "website talks to the backend you build first."
    )
    base.add_numbers(
        doc,
        [
            "Do the work on your own laptop rather than reading like a book. Typing and clicking is how the ideas stick.",
            "When a lesson shows code, copy the whole block, including every bracket and comma, and change nothing unless the lesson says to.",
            "Run the check command after each lesson. If the check does not look right, fix it now with the troubleshooting lesson rather than continuing.",
            "Keep two terminals open in the later lessons: one for the backend and one for the website. Both must stay running at the same time.",
            "If you take a break, come back to Lesson 28 to stop and restart everything cleanly.",
        ],
    )

    doc.add_heading("Contents", level=1)
    contents = [
        ("Part 1 Lesson 1. Install Visual Studio Code", "lesson1"),
        ("Part 1 Lesson 2. Install Python", "lesson2"),
        ("Part 1 Lesson 3. Install Node.js", "lesson3"),
        ("Part 1 Lesson 4. Add the helpful VS Code extensions", "lesson4"),
        ("Part 1 Lesson 5. Learn the five VS Code actions you need", "lesson5"),
        ("Part 1 Lesson 6. Create your project folder", "lesson6"),
        ("Part 2 Lesson 7. Set up the backend virtual environment", "lesson7"),
        ("Part 2 Lesson 8. Create the backend configuration files", "lesson8"),
        ("Part 2 Lesson 9. Create the users app for logging in", "lesson9"),
        ("Part 2 Lesson 10. Create the banking models and business logic", "lesson10"),
        ("Part 2 Lesson 11. Create the banking API and the bank employee API", "lesson11"),
        ("Part 2 Lesson 12. Create the demo data command", "lesson12"),
        ("Part 2 Lesson 13. Create the AI assistant app", "lesson13"),
        ("Part 2 Lesson 14. Create the database and load the demo data", "lesson14"),
        ("Part 2 Lesson 15. Run the backend tests", "lesson15"),
        ("Part 2 Lesson 16. Start the backend and see your API working", "lesson16"),
        ("Part 3 Lesson 17. Create the React website project", "lesson17"),
        ("Part 3 Lesson 18. Create the website settings and theme", "lesson18"),
        ("Part 3 Lesson 19. Create the login state and API connection", "lesson19"),
        ("Part 3 Lesson 20. Create the shared components", "lesson20"),
        ("Part 3 Lesson 21. Create the customer pages", "lesson21"),
        ("Part 3 Lesson 22. Create the bank employee pages", "lesson22"),
        ("Part 3 Lesson 23. Start the website and click through it", "lesson23"),
        ("Part 4 Lesson 24. Guided tour of every screen", "lesson24"),
        ("Part 4 Lesson 25. Change something and watch it update", "lesson25"),
        ("Part 4 Lesson 26. How a click becomes a database record", "lesson26"),
        ("Part 4 Lesson 27. Errors you will meet and how to fix them", "lesson27"),
        ("Part 4 Lesson 28. Stop, start and restart everything", "lesson28"),
        ("Part 4 Lesson 29. What to learn next", "lesson29"),
        ("Appendix A. Plain English word list", "appendixa"),
        ("Appendix B. Every file and what it does", "appendixb"),
        ("Appendix C. Logins and the demo script", "appendixc"),
        ("Appendix D. The API in one table", "appendixd"),
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

    base.page_break(doc)

    # -------------------------------------------------------------- part 1
    doc.add_heading("Part 1. Set up the laptop", level=1)
    doc.add_paragraph(
        "Four programs go onto the laptop before any code is written. Two of them run the backend "
        "and the website, one is the editor where you write and run everything, and one adds helpful "
        "features to that editor. Install them in the order below."
    )

    doc.add_heading("Lesson 1. Install Visual Studio Code", level=1)
    add_goal(doc, "Get a code editor on the laptop so you can create files and run commands in one place.")
    doc.add_paragraph(
        "Visual Studio Code, usually called VS Code, is a free editor from Microsoft. Throughout this "
        "guide it does two jobs: it is the place you write files, and it contains the terminal, which "
        "is the place you type commands."
    )
    base.add_numbers(
        doc,
        [
            "Open a browser and go to code.visualstudio.com.",
            "Click the big Download button for Windows. The site detects your system automatically.",
            "When the download finishes, open the file. It is called something like VSCodeUserSetup-x64.exe.",
            "On the licence screen select I accept the agreement, then click Next.",
            "Keep the default install location and click Next.",
            "On the Select Additional Tasks screen, tick Add to PATH, then tick Open with Code action for both file and directory, then click Next and Install.",
            "When it finishes, leave the Run Visual Studio Code box ticked and click Finish. VS Code opens.",
        ],
    )
    add_note(
        doc,
        "Why the extra ticks matter",
        "Tick Add to PATH so you can start VS Code from a terminal later, and tick the Open with Code "
        "actions so you can right click any folder and open it in VS Code with one click.",
    )
    add_check(
        doc,
        "VS Code is open and you can see the Welcome tab. Close the Welcome tab with the small x on "
        "its tab; the window stays open and empty, which is exactly right for now.",
    )

    doc.add_heading("Lesson 2. Install Python", level=1)
    add_goal(doc, "Install Python, which runs the backend of the application.")
    doc.add_paragraph(
        "Python is the language the server side of BankFlow is written in. One checkbox on the "
        "installer decides whether the command python works everywhere, so read step four closely."
    )
    base.add_numbers(
        doc,
        [
            "Go to python.org/downloads in your browser.",
            "Click the yellow Download Python button for Windows.",
            "Open the downloaded file once it is in your Downloads folder.",
            "On the very first screen, tick the box at the bottom that says Add python.exe to PATH, then click Install Now.",
            "Wait for the progress bar to finish, then click Close.",
        ],
    )
    add_note(
        doc,
        "If you forget the checkbox",
        "Run the installer again, choose Modify, and make sure Add python.exe to PATH is ticked. "
        "Without it you will see the message that python is not recognised in Lesson 5.",
    )
    doc.add_paragraph(
        "Now prove it works. Open a terminal by clicking the Start button, typing cmd, and pressing "
        "Enter. A black window appears. Type this and press Enter."
    )
    base.add_code(doc, "python --version")
    add_check(
        doc,
        "The terminal prints Python followed by a version number, for example Python 3.14.5. If it "
        "instead says python is not recognized, see Lesson 27.",
    )

    doc.add_heading("Lesson 3. Install Node.js", level=1)
    add_goal(doc, "Install Node.js so the website can be created and run.")
    doc.add_paragraph(
        "Node.js runs the tool that builds the React website. Installing Node.js also installs npm, "
        "which is the program that downloads ready made code libraries for the website."
    )
    base.add_numbers(
        doc,
        [
            "Go to nodejs.org in your browser.",
            "Click the button labelled LTS, which stands for long term support. Choose that one, not the Current one.",
            "Open the downloaded file and click Next through the installer.",
            "Accept the licence, keep the default folder, and keep every checkbox as it is.",
            "On the Tools for Native Modules screen you can leave the checkbox empty, then click Next.",
            "Click Install, wait for it to finish, then click Finish.",
        ],
    )
    doc.add_paragraph(
        "Prove it works in the same terminal window you used for Python."
    )
    base.add_code(doc, "node --version\nnpm --version")
    add_check(
        doc,
        "You see two version numbers, for example v24.19.0 and 12.0.2. Two numbers mean both Node.js "
        "and npm are ready.",
    )

    doc.add_heading("Lesson 4. Add the helpful VS Code extensions", level=1)
    add_goal(doc, "Make VS Code understand Python and React, and format your files neatly.")
    doc.add_paragraph(
        "An extension is a small add on for VS Code. The two below are optional in the sense that the "
        "project runs without them, but they colour your code, warn you about mistakes and keep files "
        "tidy, which makes learning much easier."
    )
    base.add_numbers(
        doc,
        [
            "In VS Code, look at the tall icon bar on the far left and click the icon that looks like four squares, or press Ctrl+Shift+X. The Extensions panel opens.",
            "In the search box type Python, and in the results find the one published by Microsoft, then click Install.",
            "Search again for ES7 plus React snippets and install the extension with the most downloads.",
            "Search once more for Prettier Code formatter and install the one by Prettier. It keeps indentation consistent.",
        ],
    )
    add_check(
        doc,
        "The Extensions panel shows the three items with an Installed label and no Install button. "
        "You can close the panel by clicking the squares icon again.",
    )

    doc.add_heading("Lesson 5. Learn the five VS Code actions you need", level=1)
    add_goal(doc, "Learn only the parts of the editor this guide uses, so the screen feels familiar.")
    doc.add_paragraph(
        "VS Code has hundreds of features and you need five of them. Practise them in this lesson "
        "before you create anything."
    )
    base.add_table(
        doc,
        ["What you want to do", "How to do it", "What appears"],
        [
            ["Open a folder in the editor", "Menu File, then Open Folder, then choose the folder",
             "The folder name appears at the top of the left sidebar"],
            ["Create a new file", "Right click in the sidebar, choose New File, type the full name, press Enter",
             "An empty tab opens with the file name on it"],
            ["Save the file", "Press Ctrl+S, or menu File then Save",
             "The dot on the file tab disappears once the file is saved"],
            ["Open the terminal inside VS Code", "Menu Terminal, then New Terminal, or press Ctrl and the backtick key",
             "A panel opens at the bottom with a command prompt"],
            ["Run a command", "Click inside the terminal panel, type the command, press Enter",
             "The terminal prints the result of the command"],
        ],
        [4.6, 6.4, 6.2],
    )
    add_note(
        doc,
        "The most useful habit in this guide",
        "Always run commands in the VS Code terminal that is open in your project folder. The "
        "terminal starts in whatever folder you opened, so you do not have to type long paths.",
    )
    add_check(
        doc,
        "You can open a folder, create a file, save it, open the terminal and run a command without "
        "looking anything up.",
    )

    doc.add_heading("Lesson 6. Create your project folder", level=1)
    add_goal(doc, "Create one folder that will hold the whole project, and open it in VS Code.")
    doc.add_paragraph(
        "Everything you build lives inside a single folder called banking_app, which contains two "
        "sub folders: backend for the server and frontend for the website. Keeping them together "
        "makes it easy to copy the project to another computer later."
    )
    base.add_numbers(
        doc,
        [
            "Open File Explorer and go to the drive where you keep your work, for example drive D or your Documents folder.",
            "Right click in an empty space, choose New then Folder, and name it banking_app.",
            "Open banking_app and create two more folders inside it, one named backend and one named frontend.",
            "Close File Explorer. In VS Code choose File, then Open Folder, select banking_app and click Select Folder.",
            "VS Code may ask whether you trust the authors of the files. Choose Yes, I trust the authors, because these are your own folders.",
        ],
    )
    doc.add_paragraph("Your sidebar should now show the two empty folders like this.")
    base.add_code(
        doc,
        "BANKING_APP\n"
        "    backend\n"
        "    frontend",
    )
    add_check(
        doc,
        "The sidebar shows banking_app with backend and frontend inside it. Part 1 is complete; the "
        "laptop has every tool installed and a home for the project.",
    )

    # -------------------------------------------------------------- part 2
    base.page_break(doc)
    doc.add_heading("Part 2. Build the backend", level=1)
    doc.add_paragraph(
        "The backend is the part that stores the pretend bank data and answers questions from the "
        "website. You build it first because the website needs something to talk to. Every command "
        "in this part is typed in the VS Code terminal, and the terminal must be inside the backend "
        "folder when you run it."
    )

    doc.add_heading("Lesson 7. Set up the backend virtual environment", level=1)
    add_goal(doc, "Create a private box for the backend libraries and install Django inside it.")
    doc.add_paragraph(
        "A virtual environment is a private box of libraries that belongs to this one project. It "
        "stops BankFlow's libraries from interfering with any other Python work on the laptop. You "
        "create it once and then switch it on whenever you work on the project."
    )
    doc.add_paragraph(
        "First move the terminal into the backend folder. In the VS Code terminal type these two "
        "lines, pressing Enter after each one."
    )
    base.add_code(
        doc,
        "cd backend\n"
        "python -m venv venv",
    )
    add_check(
        doc,
        "A new folder named venv appears inside backend in the sidebar. The command finishes with no "
        "error message.",
    )
    doc.add_paragraph(
        "Now switch the environment on and install the libraries. The activation command differs "
        "between Windows and macOS, so use the line that matches your laptop."
    )
    base.add_code(
        doc,
        "# Windows\n"
        "venv\\Scripts\\activate\n"
        "\n"
        "# macOS or Linux\n"
        "source venv/bin/activate",
    )
    add_check(
        doc,
        "The start of the terminal line now shows (venv) in brackets. That tells you the private box "
        "is switched on. Every backend command in this guide assumes you see it.",
    )
    doc.add_paragraph("With (venv) showing, install the backend libraries.")
    base.add_code(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
    )
    add_check(
        doc,
        "The last line says Successfully installed followed by the library names. The list includes "
        "Django, djangorestframework, djangorestframework-simplejwt, django-cors-headers, "
        "python-dotenv and psycopg. If pip is not recognised, see Lesson 27.",
    )
    add_note(
        doc,
        "Remember to switch on the box every time",
        "When you open a new terminal for backend work, run venv\\Scripts\\activate first on Windows. "
        "If you forget, commands fail with No module named django.",
    )

    doc.add_heading("Lesson 8. Create the backend configuration files", level=1)
    add_goal(doc, "Create the files that tell Django how the project is set up.")
    doc.add_paragraph(
        "These eight files are the settings and entry points of the backend. Create each one by "
        "right clicking inside the correct folder, choosing New File, and typing the name exactly as "
        "the heading above the code shows. Then paste the whole block and save with Ctrl+S."
    )
    doc.add_paragraph(
        "The settings file is the most important one. It lists which parts of the project are turned "
        "on, where the database lives, how long a login lasts, and which website address is allowed "
        "to call the API. Read the comments in it as you paste; they explain each choice in one line."
    )
    add_code_file(doc, "backend/requirements.txt", "Create this file directly inside backend. It lists the exact library versions from Lesson 7.")
    add_code_file(doc, "backend/.env.example", "Create this file directly inside backend. It is the template for the secrets file.")
    add_code_file(doc, "backend/.gitignore", "Create this file directly inside backend. It keeps private files out of version control.")
    add_code_file(doc, "backend/manage.py", "Create this file directly inside backend. It is the command you type to run backend tasks.")
    add_code_file(doc, "backend/config/__init__.py", "Right click backend, choose New Folder, name it config, then create this empty file inside it.")
    add_code_file(doc, "backend/config/settings.py", "Inside the config folder. This is the main settings file described above.")
    add_code_file(doc, "backend/config/urls.py", "Inside the config folder. It maps each web address to the code that answers it.")
    add_code_file(doc, "backend/config/wsgi.py", "Inside the config folder. It lets a production server start the project.")
    add_code_file(doc, "backend/config/asgi.py", "Inside the config folder. The equivalent entry point for asynchronous servers.")
    doc.add_paragraph(
        "Finally, make your own private copy of the environment file. In the terminal run:"
    )
    base.add_code(doc, "copy .env.example .env      # cp .env.example .env on macOS or Linux")
    add_check(
        doc,
        "The sidebar shows manage.py, requirements.txt, the .env files and a config folder that "
        "contains four files. Now test the settings by asking Django to check itself.",
    )
    base.add_code(doc, "python manage.py check")
    add_check(
        doc,
        "The terminal prints System check identified no issues with a count in brackets. That one "
        "line means every settings file is correct.",
    )

    doc.add_heading("Lesson 9. Create the users app for logging in", level=1)
    add_goal(doc, "Create the part of the backend that handles accounts, logins and customer details.")
    doc.add_paragraph(
        "In Django, an app is a folder that groups related features. The users app owns three ideas: "
        "a user who logs in with an email address instead of a username, a role that says whether the "
        "person is a customer or a bank employee, and a profile that stores the extra details the "
        "bank employee screens display."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named users.",
            "Inside that folder create another folder named urls.",
            "Create every file below using the same New File method, then paste the code and save.",
            "When the files exist, run makemigrations users so Django prepares the database tables for this app.",
        ],
    )
    add_code_file(doc, "backend/users/__init__.py", "An empty file that marks the folder as a Python package.")
    add_code_file(doc, "backend/users/apps.py", "Describes the app and switches on the profile signal.")
    add_code_file(doc, "backend/users/models.py", "The user, the role choices and the customer profile.")
    add_code_file(doc, "backend/users/signals.py", "Creates a profile automatically for every new user.")
    add_code_file(doc, "backend/users/permissions.py", "The check that only bank employees can open employee pages.")
    add_code_file(doc, "backend/users/serializers.py", "Turns user details into JSON and validates registration.")
    add_code_file(doc, "backend/users/views.py", "The code that answers register and profile requests.")
    add_code_file(doc, "backend/users/urls/__init__.py", "Marks the urls folder as a package.")
    add_code_file(doc, "backend/users/urls/auth_urls.py", "The register, login and refresh web addresses.")
    add_code_file(doc, "backend/users/urls/profile_urls.py", "The profile web address.")
    add_code_file(doc, "backend/users/admin.py", "Makes users editable in the built in Django admin site.")
    add_code_file(doc, "backend/users/tests.py", "Automatic tests for registration, login and profile updates.")
    add_check(
        doc,
        "You now have a users folder with twelve files. Nothing needs to run yet; the checks happen "
        "in Lesson 14 once the whole backend exists.",
    )

    doc.add_heading("Lesson 10. Create the banking models and business logic", level=1)
    add_goal(doc, "Create the four banking tables and the file that does all the money arithmetic.")
    doc.add_paragraph(
        "A model is a description of a table in the database. BankFlow has four: accounts, "
        "transactions, loans and notifications. PostgreSQL or SQLite creates the real tables from "
        "these descriptions, so you never write database code by hand."
    )
    doc.add_paragraph(
        "The services file is where the thinking lives. It holds the EMI formula, the monthly totals, "
        "the spending categories, the six month trend and the list of pretend transactions used by "
        "the seed command in Lesson 12. The dashboard, the charts and the AI assistant all call this "
        "one file, which is why the numbers on every screen always agree."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named banking.",
            "Inside banking, create a folder named management, and inside that create a folder named commands.",
            "Inside banking, create a folder named urls.",
            "Create the files below in their shown locations, then run makemigrations banking.",
        ],
    )
    add_code_file(doc, "backend/banking/__init__.py", "Marks the banking folder as a package.")
    add_code_file(doc, "backend/banking/apps.py", "Describes the banking app.")
    add_code_file(doc, "backend/banking/models.py", "The four tables: account, transaction, loan, notification.")
    add_code_file(doc, "backend/banking/services.py", "EMI maths, totals, categories, trends and the demo transaction list.")
    add_code_file(doc, "backend/banking/serializers.py", "Prepares banking data as JSON for the website.")
    add_code_file(doc, "backend/banking/views.py", "The customer web addresses such as dashboard and transactions.")
    add_code_file(doc, "backend/banking/admin_views.py", "The bank employee web addresses that see every customer.")
    add_code_file(doc, "backend/banking/urls/__init__.py", "Marks the urls folder as a package.")
    add_code_file(doc, "backend/banking/urls/customer_urls.py", "Customer web addresses.")
    add_code_file(doc, "backend/banking/urls/admin_urls.py", "Bank employee web addresses.")
    add_code_file(doc, "backend/banking/admin.py", "Shows the banking tables in the Django admin site.")
    add_code_file(doc, "backend/banking/tests.py", "Automatic tests for the banking endpoints.")
    add_check(
        doc,
        "The banking folder contains the files above and two sub folders. The services file is long, "
        "so paste it in one go rather than retyping it.",
    )

    doc.add_heading("Lesson 11. Create the banking API and the bank employee API", level=1)
    add_goal(doc, "Confirm how the web addresses in the banking app are wired to the code.")
    doc.add_paragraph(
        "You already pasted these files in Lesson 10, so this lesson is about understanding them "
        "rather than creating anything new. Read the two url files now: they are the map that turns a "
        "web address such as /api/transactions/ into the exact function that answers it."
    )
    base.add_table(
        doc,
        ["Address the website calls", "Which file answers it", "What comes back"],
        [
            ["/api/dashboard/", "banking/views.py", "Balances, income, expenses and chart data"],
            ["/api/transactions/", "banking/views.py", "A page of transactions after filtering"],
            ["/api/loans/", "banking/views.py", "The customer's loans, or a new application"],
            ["/api/emi/", "banking/views.py", "The EMI calculation for the numbers you typed"],
            ["/api/admin/analytics/", "banking/admin_views.py", "Totals for the whole pretend bank"],
            ["/api/admin/loans/<id>/", "banking/admin_views.py", "The loan after approving or rejecting it"],
        ],
        [5.4, 5.4, 6.4],
    )
    add_check(
        doc,
        "You can point at any address in the table and say which file answers it. That is the single "
        "most useful skill for reading any backend.",
    )

    doc.add_heading("Lesson 12. Create the demo data command", level=1)
    add_goal(doc, "Create the command that fills the pretend bank with three customers and their history.")
    doc.add_paragraph(
        "Typing test data by hand is slow, so Django lets you write a command you can run any time. "
        "This command creates the three customers, their accounts, twenty-eight transactions spread "
        "over three months, six loan applications, the notification list and one saved AI "
        "conversation."
    )
    doc.add_paragraph(
        "It is written so the demo numbers always match the script you will demonstrate: the balance "
        "is 85,450 rupees, monthly income is 45,000, monthly spending is 18,450, and the largest "
        "category is Shopping at 7,200. Running the command again with the flush option returns the "
        "project to exactly this state."
    )
    add_code_file(doc, "backend/banking/management/__init__.py", "An empty file inside the management folder.")
    add_code_file(doc, "backend/banking/management/commands/__init__.py", "An empty file inside the commands folder.")
    add_code_file(
        doc,
        "backend/banking/management/commands/seed_demo.py",
        "Inside the commands folder. This is the file you run to create all the pretend data.",
    )
    add_check(
        doc,
        "The path backend/banking/management/commands/seed_demo.py exists. The folder names matter: "
        "Django only finds commands placed exactly here.",
    )

    doc.add_heading("Lesson 13. Create the AI assistant app", level=1)
    add_goal(doc, "Create the chat feature and the service that answers banking questions.")
    doc.add_paragraph(
        "The AI assistant is the part of BankFlow that answers questions such as what is my balance. "
        "It works in three moves: it works out what you are asking, it looks up your own pretend "
        "data, and it writes a sentence from that data."
    )
    doc.add_paragraph(
        "The design decision that matters is that the wording and the numbers are separate. The "
        "numbers always come from the database, so the assistant can never invent a balance. If you "
        "later add an external AI key, the model only rephrases the same numbers; if you do not, the "
        "rule based answers you are about to paste handle everything offline."
    )
    base.add_numbers(
        doc,
        [
            "Inside backend, create a folder named assistant.",
            "Create the six files below, then run makemigrations assistant.",
        ],
    )
    add_code_file(doc, "backend/assistant/__init__.py", "Marks the assistant folder as a package.")
    add_code_file(doc, "backend/assistant/apps.py", "Describes the assistant app.")
    add_code_file(doc, "backend/assistant/models.py", "The chat message table that stores history.")
    add_code_file(
        doc,
        "backend/assistant/ai_service.py",
        "The heart of the feature: intents, data lookups, the rule based answers and the optional model call.",
    )
    add_code_file(doc, "backend/assistant/serializers.py", "Validates the question and formats saved messages.")
    add_code_file(doc, "backend/assistant/views.py", "The chat, history, suggestion and monitoring endpoints.")
    add_code_file(doc, "backend/assistant/urls.py", "The assistant web addresses.")
    add_code_file(doc, "backend/assistant/admin.py", "Shows saved conversations in the Django admin site.")
    add_code_file(doc, "backend/assistant/tests.py", "Automatic tests for every kind of question.")
    add_check(
        doc,
        "You now have three apps: users, banking and assistant. If any file is in the wrong folder, "
        "Django will report it in the next lesson.",
    )

    doc.add_heading("Lesson 14. Create the database and load the demo data", level=1)
    add_goal(doc, "Turn the models into real database tables and fill them with pretend bank data.")
    doc.add_paragraph(
        "Three commands finish the backend. The first prepares the instructions that build the "
        "tables, the second builds them, and the third fills them with the three fictional customers."
    )
    base.add_code(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
    )
    doc.add_paragraph("The seed command ends by printing the logins you will use for the rest of the guide.")
    base.add_code(
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
    add_check(
        doc,
        "You see those logins, and a file named db.sqlite3 appears inside backend. That file is your "
        "pretend bank. Write the logins down or leave this page open.",
    )

    doc.add_heading("Lesson 15. Run the backend tests", level=1)
    add_goal(doc, "Prove the backend behaves correctly with twenty-five automatic tests.")
    doc.add_paragraph(
        "Tests are small programs that check your work for you. BankFlow ships with twenty-five of "
        "them: they create their own temporary data, try the endpoints, and compare the answers with "
        "what should happen. Running them takes about half a minute and is the fastest way to know "
        "the backend is healthy."
    )
    base.add_code(doc, "python manage.py test")
    doc.add_paragraph("A healthy run ends like this.")
    base.add_code(
        doc,
        "Found 25 test(s).\n"
        "System check identified no issues (0 silenced).\n"
        ".........................\n"
        "----------------------------------------------------------------------\n"
        "Ran 25 tests in 31.331s\n"
        "\n"
        "OK",
    )
    add_note(
        doc,
        "If you see failures",
        "The most common cause is a file that was pasted with a missing line. Open the file named in "
        "the error message, compare it with the code in this guide, and run the tests again.",
    )
    add_check(
        doc,
        "The word OK appears at the end. This is a big moment: your backend is complete and correct, "
        "and you have not written a line of code yourself.",
    )

    doc.add_heading("Lesson 16. Start the backend and see your API working", level=1)
    add_goal(doc, "Run the backend server and watch it answer a real request.")
    doc.add_paragraph(
        "The API is now complete. Start the server and leave this terminal running for the rest of "
        "the guide."
    )
    base.add_code(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "The terminal stops returning to the prompt and shows a line about watching for file changes. "
        "That means the server is running. Open your browser and visit these two addresses to see it "
        "answer."
    )
    base.add_code(
        doc,
        "http://127.0.0.1:8000/api/dashboard/\n"
        "http://127.0.0.1:8000/admin/",
    )
    add_note(
        doc,
        "Why the first address shows a login error",
        "The dashboard endpoint only answers someone who is logged in, and a browser tab is not "
        "logged in yet. That is the correct behaviour, and it proves the security is working. You "
        "will see the real data in the website in Lesson 23 and you can log into the admin address "
        "with admin@bankflow.com and Admin@12345.",
    )
    doc.add_paragraph(
        "To stop the server later, click in the terminal and press Ctrl+C. To run it again, type the "
        "same command. For now, keep it running."
    )
    add_check(
        doc,
        "The browser shows the Django admin login page at the second address, and you can log in with "
        "the admin account and see the three customers under Users.",
    )

    # -------------------------------------------------------------- part 3
    base.page_break(doc)
    doc.add_heading("Part 3. Build the website", level=1)
    doc.add_paragraph(
        "The website is the part your customer sees. It is built with React, which means the page "
        "runs in the browser and asks the backend for data when it needs it. Open a second terminal "
        "in VS Code for this part: click the plus sign at the top right of the terminal panel. Keep "
        "the backend terminal from Lesson 16 running in the first tab."
    )

    doc.add_heading("Lesson 17. Create the React website project", level=1)
    add_goal(doc, "Create the website project and download the ready made building blocks.")
    doc.add_paragraph(
        "The command below creates a React project with Vite inside your frontend folder. Vite is the "
        "tool that runs the website while you work and packages it at the end."
    )
    base.add_code(
        doc,
        "cd ..\n"
        "cd frontend\n"
        "npm create vite@latest . -- --template react\n"
        "npm install",
    )
    add_note(
        doc,
        "If the terminal asks about the current directory",
        "Answer yes to continue in the current folder. If it asks for a package name, press Enter to "
        "accept the default.",
    )
    doc.add_paragraph(
        "Now install the libraries BankFlow uses. Material UI provides the buttons, cards and tables; "
        "Recharts draws the charts; Axios talks to the backend; and React Router switches between "
        "pages."
    )
    base.add_code(
        doc,
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
    )
    add_check(
        doc,
        "The terminal reports added packages with no error, and the sidebar now shows a frontend "
        "folder containing src, public and package.json. If npm is not recognised, see Lesson 27.",
    )

    doc.add_heading("Lesson 18. Create the website settings and theme", level=1)
    add_goal(doc, "Replace the starter files with the BankFlow settings, theme and page routes.")
    doc.add_paragraph(
        "Vite created a starter project with a demonstration page. You replace those files with the "
        "ones below. Two of them are worth a second look: the theme file holds every colour and "
        "font, so the whole website can be restyled from one place, and App.jsx lists every page and "
        "which web address shows it."
    )
    doc.add_paragraph(
        "When a lesson names a file that already exists, open it in the sidebar and replace all of "
        "its contents with the block shown, then save."
    )
    add_code_file(doc, "frontend/package.json", "Open the existing package.json and replace everything with this version.")
    add_code_file(doc, "frontend/vite.config.js", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/index.html", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/.env.example", "Create this new file in the frontend folder.")
    add_code_file(doc, "frontend/.gitignore", "Replace the existing file in the frontend folder.")
    add_code_file(doc, "frontend/public/bankflow.svg", "Replace the icon in the public folder.")
    add_code_file(doc, "frontend/src/index.css", "Replace the existing file in the src folder.")
    add_code_file(doc, "frontend/src/theme.js", "Create this new file in the src folder. It holds every colour and text style.")
    add_code_file(doc, "frontend/src/main.jsx", "Replace the existing file in the src folder.")
    add_code_file(doc, "frontend/src/App.jsx", "Replace the existing file in the src folder. It lists every page and address.")
    doc.add_paragraph("Copy the environment file so the website knows where the backend is.")
    base.add_code(doc, "copy .env.example .env      # cp .env.example .env on macOS or Linux")
    add_note(
        doc,
        "Delete the starter files you no longer need",
        "The React starter includes src/App.css and a folder called src/assets with a logo. You can "
        "delete both: right click them in the sidebar and choose Delete. BankFlow does not use them.",
    )
    add_check(
        doc,
        "The src folder contains main.jsx, App.jsx, theme.js and index.css, and the frontend folder "
        "contains index.html, vite.config.js, package.json, .env and the public folder.",
    )

    doc.add_heading("Lesson 19. Create the login state and API connection", level=1)
    add_goal(doc, "Create the single place that talks to the backend and remembers who is logged in.")
    doc.add_paragraph(
        "Every request in the website goes through one file, api.js. It attaches the login token to "
        "each request, renews the token automatically when it expires, and turns any failure into a "
        "sentence the screen can show. The auth context beside it remembers which user is logged in, "
        "so any page can ask who you are and whether you are a bank employee."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, make sure these folders exist: services, context and utils. Create each one with a right click and New Folder.",
            "Create the files below in their shown folders, pasting the code and saving each one.",
        ],
    )
    add_code_file(doc, "frontend/src/services/api.js", "Inside src/services. The single connection to the backend.")
    add_code_file(doc, "frontend/src/services/authService.js", "Inside src/services. Register, login and profile calls.")
    add_code_file(doc, "frontend/src/services/bankingService.js", "Inside src/services. Dashboard, transactions, loans and notifications.")
    add_code_file(doc, "frontend/src/services/aiService.js", "Inside src/services. Assistant chat and history calls.")
    add_code_file(doc, "frontend/src/services/adminService.js", "Inside src/services. Bank employee data calls.")
    add_code_file(doc, "frontend/src/context/AuthContext.jsx", "Inside src/context. Remembers the logged in user.")
    add_code_file(doc, "frontend/src/utils/formatCurrency.js", "Inside src/utils. Formats rupees and dates the same way everywhere.")
    add_code_file(doc, "frontend/src/utils/calculations.js", "Inside src/utils. Calculates EMI instantly as you move a slider.")
    add_check(
        doc,
        "src now contains the three new folders. Nothing to run yet; the next lesson adds the visible "
        "parts of the pages.",
    )

    doc.add_heading("Lesson 20. Create the shared components", level=1)
    add_goal(doc, "Create the reusable pieces that appear on many pages.")
    doc.add_paragraph(
        "A component is a piece of a page you write once and reuse. The sidebar, the top bar, the "
        "statistic cards, the transaction table and the chat bubble are all components, which is why "
        "every page looks consistent and why changing one file updates the whole website."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, create a folder named components.",
            "Create the nine files below inside it, pasting and saving each one.",
        ],
    )
    add_code_file(doc, "frontend/src/components/AppLayout.jsx", "The frame around every private page: sidebar, top bar and content area.")
    add_code_file(doc, "frontend/src/components/Navbar.jsx", "The top bar with the page title, notifications and your profile menu.")
    add_code_file(doc, "frontend/src/components/Sidebar.jsx", "The navigation list, which collapses on small screens.")
    add_code_file(doc, "frontend/src/components/DashboardCard.jsx", "One statistic card, used four times on the dashboard.")
    add_code_file(doc, "frontend/src/components/TransactionTable.jsx", "The transaction table, used by customers and employees.")
    add_code_file(doc, "frontend/src/components/LoanCard.jsx", "One loan summary card with a repayment progress bar.")
    add_code_file(doc, "frontend/src/components/ChatMessage.jsx", "One chat bubble, used for your question and the assistant's reply.")
    add_code_file(doc, "frontend/src/components/ProtectedRoute.jsx", "Sends visitors to the login page when a page needs a login.")
    add_code_file(doc, "frontend/src/components/Common.jsx", "Small helpers used everywhere: loader, error message, empty state, status label.")
    add_check(
        doc,
        "The components folder holds nine files. If any file name has a capital letter missing, the "
        "next lesson will fail to find it, so check the names now.",
    )

    doc.add_heading("Lesson 21. Create the customer pages", level=1)
    add_goal(doc, "Create the fourteen pages your customer can visit.")
    doc.add_paragraph(
        "These pages turn API data into screens. The table shows what each page is for and which "
        "backend address it calls, which is the pattern to notice: a page fetches data in the "
        "background, stores it in state, and renders it."
    )
    base.add_table(
        doc,
        ["Page file", "What the customer sees", "Backend address it calls"],
        [
            ["Landing.jsx", "The public introduction page with the hero and features", "none"],
            ["Login.jsx", "The login form with the demo accounts", "/api/auth/login/"],
            ["Register.jsx", "The registration form", "/api/auth/register/"],
            ["Dashboard.jsx", "Balance, income, expenses, loans and four charts", "/api/dashboard/"],
            ["Account.jsx", "Account number with the middle hidden, type and status", "/api/account/"],
            ["Transactions.jsx", "The searchable, filterable transaction list", "/api/transactions/"],
            ["TransactionDetails.jsx", "One transaction in full", "/api/transactions/<id>/"],
            ["Loans.jsx", "Loans and the application form with a live EMI preview", "/api/loans/"],
            ["LoanDetails.jsx", "One loan with its repayment schedule", "/api/loans/<id>/"],
            ["EMICalculator.jsx", "Slider based EMI calculator", "/api/emi/"],
            ["AIAssistant.jsx", "The chat screen with history", "/api/assistant/chat/"],
            ["Notifications.jsx", "Alerts, read and unread", "/api/notifications/"],
            ["Profile.jsx", "Your details, editable", "/api/profile/"],
            ["NotFound.jsx", "A friendly message for unknown addresses", "none"],
        ],
        [4.0, 7.4, 5.8],
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src, create a folder named pages.",
            "Create the fourteen files below inside it.",
        ],
    )
    add_code_file(doc, "frontend/src/pages/Landing.jsx", "The first page a visitor sees.")
    add_code_file(doc, "frontend/src/pages/Login.jsx", "Logging in and remembering the token.")
    add_code_file(doc, "frontend/src/pages/Register.jsx", "Creating a new pretend customer.")
    add_code_file(doc, "frontend/src/pages/Dashboard.jsx", "The main screen after logging in.")
    add_code_file(doc, "frontend/src/pages/Account.jsx", "The account details page.")
    add_code_file(doc, "frontend/src/pages/Transactions.jsx", "The transaction list with filters.")
    add_code_file(doc, "frontend/src/pages/TransactionDetails.jsx", "A single transaction.")
    add_code_file(doc, "frontend/src/pages/Loans.jsx", "Loans and the application form.")
    add_code_file(doc, "frontend/src/pages/LoanDetails.jsx", "A single loan and its schedule.")
    add_code_file(doc, "frontend/src/pages/EMICalculator.jsx", "The EMI calculator.")
    add_code_file(doc, "frontend/src/pages/AIAssistant.jsx", "The chat assistant.")
    add_code_file(doc, "frontend/src/pages/Notifications.jsx", "The alerts page.")
    add_code_file(doc, "frontend/src/pages/Profile.jsx", "The profile page.")
    add_code_file(doc, "frontend/src/pages/NotFound.jsx", "The page for unknown addresses.")
    add_check(
        doc,
        "The pages folder holds fourteen files. Landing.jsx, Dashboard.jsx and AIAssistant.jsx are "
        "the longest; paste them in one go and save.",
    )

    doc.add_heading("Lesson 22. Create the bank employee pages", level=1)
    add_goal(doc, "Create the six pages that only the bank employee account can open.")
    doc.add_paragraph(
        "These pages read the employee endpoints, which return data for every customer. The route "
        "guard from Lesson 20 sends ordinary customers back to their own dashboard if they try to "
        "open an employee address, and the backend refuses the request as well, so the protection "
        "exists in both places."
    )
    base.add_numbers(
        doc,
        [
            "Inside frontend/src/pages, create a folder named admin.",
            "Create the six files below inside that folder.",
        ],
    )
    add_code_file(doc, "frontend/src/pages/admin/AdminDashboard.jsx", "Six totals, portfolio charts and the top customers table.")
    add_code_file(doc, "frontend/src/pages/admin/CustomerManagement.jsx", "The customer table and the customer detail dialog.")
    add_code_file(doc, "frontend/src/pages/admin/TransactionManagement.jsx", "Every customer's transactions with filters.")
    add_code_file(doc, "frontend/src/pages/admin/LoanManagement.jsx", "Approve, activate or reject a loan application.")
    add_code_file(doc, "frontend/src/pages/admin/AdminAnalytics.jsx", "The charts that summarise the whole pretend bank.")
    add_code_file(doc, "frontend/src/pages/admin/AIMonitor.jsx", "What customers asked the assistant and how it answered.")
    add_check(
        doc,
        "All twenty pages now exist, fourteen in pages and six in pages/admin. Part 3 is nearly done.",
    )

    doc.add_heading("Lesson 23. Start the website and click through it", level=1)
    add_goal(doc, "Run the website and confirm it really works.")
    doc.add_paragraph(
        "In your second terminal, which should be inside the frontend folder, start the website."
    )
    base.add_code(doc, "npm run dev")
    doc.add_paragraph(
        "The terminal prints a Local address. Open it in your browser; it is usually "
        "http://localhost:5173. Keep both terminals running: one serves the backend, one serves the "
        "website."
    )
    base.add_numbers(
        doc,
        [
            "The landing page appears with the headline Your Smarter Digital Banking Experience.",
            "Click Login, then click the demo customer line to fill the form, and press Login.",
            "The dashboard appears with a balance of 85,450 rupees, income of 45,000 and spending of 18,450.",
            "Open the AI Assistant from the sidebar and ask: What is my balance?",
            "The assistant answers with the same 85,450 figure, because it reads the same database.",
        ],
    )
    add_check(
        doc,
        "The dashboard shows four cards and four charts, and the assistant answers your question. "
        "Congratulations: you have built and run a complete full stack application.",
    )
    add_note(
        doc,
        "If the page loads but every request fails",
        "Make sure the backend terminal from Lesson 16 is still running. The website cannot show data "
        "without it.",
    )

    # -------------------------------------------------------------- part 4
    base.page_break(doc)
    doc.add_heading("Part 4. Learn by doing", level=1)
    doc.add_paragraph(
        "The application now works. This part turns it into a learning tool: you will walk every "
        "screen, change things and watch the result, and trace what happens between a click and a "
        "database record."
    )

    doc.add_heading("Lesson 24. Guided tour of every screen", level=1)
    add_goal(doc, "See every feature the project contains, in the order you would demonstrate it.")
    base.add_table(
        doc,
        ["Screen", "What to do there", "What it teaches"],
        [
            ["Landing page", "Scroll through the hero, features, assistant preview and security sections",
             "How a public page is composed from components"],
            ["Login", "Click the demo customer line to autofill, then log in",
             "Tokens, form validation and redirects by role"],
            ["Dashboard", "Read the four cards, then switch the chart tabs",
             "Turning one API response into cards and charts"],
            ["Account", "Look at the hidden middle of the account number",
             "Never showing the full number, even in a demo"],
            ["Transactions", "Search for Swiggy, then filter to Shopping",
             "Filtering, paging and totals on the server"],
            ["Transaction details", "Open any row",
             "Passing an id in the address and loading one record"],
            ["Loans", "Open the application form and watch the EMI change as you type",
             "Calculating on the spot and saving a new record"],
            ["Loan details", "Read the repayment schedule table",
             "Turning a loan into an instalment plan"],
            ["EMI calculator", "Move the sliders",
             "Maths in the browser, verified by the backend"],
            ["AI assistant", "Ask three questions, then open the history panel",
             "Intents, saved conversations and grounded answers"],
            ["Notifications", "Mark one as read, then mark all as read",
             "Updating a single record from the interface"],
            ["Profile", "Change your phone number and save",
             "Editing your own data with permission checks"],
            ["Admin dashboard", "Log in as admin@bankflow.com and open it",
             "Role based access and portfolio level totals"],
            ["Loan management", "Approve the pending loan",
             "An action that changes data and notifies the customer"],
            ["AI monitoring", "Read the questions saved from your own chat",
             "How a feature can be observed by an operator"],
        ],
        [3.6, 7.4, 6.2],
    )
    add_check(
        doc,
        "You have visited every screen once. You now know the whole application, not just the parts "
        "this guide made you paste.",
    )

    doc.add_heading("Lesson 25. Change something and watch it update", level=1)
    add_goal(doc, "Make four small changes so you feel how the pieces connect.")
    doc.add_paragraph(
        "Change one thing at a time, save the file, and look at the browser. The website reloads by "
        "itself when you save a frontend file, and the backend reloads when you save a backend file."
    )
    doc.add_paragraph("Exercise 1. Change the brand colour. Open frontend/src/theme.js.")
    base.add_code(
        doc,
        "// find this line inside palette.primary\n"
        "main: \"#1b3a8f\",\n"
        "\n"
        "// replace the colour with another one, for example\n"
        "main: \"#0f766e\",",
    )
    add_check(doc, "Save the file and watch the buttons, sidebar highlights and chart accents turn teal within a second.")

    doc.add_paragraph(
        "Exercise 2. Change the demo balance. Open "
        "backend/banking/management/commands/seed_demo.py and find the line shown below near the "
        "beginning of the transaction section."
    )
    base.add_code(doc, "target_balance = 85450.0      # change to 100000.0 and save")
    doc.add_paragraph(
        "Now rebuild the demo data in the backend terminal and refresh the dashboard."
    )
    base.add_code(doc, "python manage.py seed_demo --flush")
    add_check(
        doc,
        "The dashboard balance changes to 100,000 rupees, and the assistant answers with the same "
        "new figure. That is the single source of truth working: one number, many screens.",
    )

    doc.add_paragraph(
        "Exercise 3. Teach the assistant a new word. Open backend/assistant/ai_service.py and find "
        "the account_balance entry in INTENT_KEYWORDS."
    )
    base.add_code(
        doc,
        "\"account_balance\": [\"balance\", \"how much money\", \"account balance\", \"available amount\"],\n"
        "\n"
        "// add one more phrase inside the list, for example\n"
        "\"account_balance\": [\"balance\", \"how much money\", \"account balance\", \"available amount\", \"kitna paisa\"],",
    )
    add_check(
        doc,
        "Save, then ask the assistant kitna paisa in the chat. It now understands the phrase and "
        "answers with your balance.",
    )

    doc.add_paragraph(
        "Exercise 4. Change a welcome message. Open frontend/src/pages/Dashboard.jsx and find the "
        "PageHeader title line near the top of the returned page."
    )
    base.add_code(doc, "title={`${greeting()}, ${firstName}`}", )
    doc.add_paragraph(
        "Change it to a message of your own, for example title={`Welcome back, ${firstName}`}, save, "
        "and look at the dashboard heading."
    )
    add_check(
        doc,
        "All four changes worked. You have now edited the theme, the data, the AI behaviour and a "
        "page, which are the four places most changes in a project like this happen.",
    )

    doc.add_heading("Lesson 26. How a click becomes a database record", level=1)
    add_goal(doc, "Follow one request from the button you click to the data that comes back.")
    doc.add_paragraph(
        "Understanding this chain is the difference between copying code and being able to build your "
        "own features. Follow the numbers in the diagram below, then read the walkthrough."
    )
    base.add_code(
        doc,
        "1  You click View Transactions in the browser\n"
        "2  React Router shows the pages/Transactions.jsx component for the address /transactions\n"
        "3  The component runs its useEffect and calls bankingService.getTransactions(filters)\n"
        "4  services/api.js attaches your login token and sends the request to the backend\n"
        "5  Django matches /api/transactions/ in banking/urls/customer_urls.py\n"
        "6  TransactionListView in banking/views.py reads the filters, builds a database query\n"
        "7  Django's ORM turns the query into SQL and SQLite returns the matching rows\n"
        "8  TransactionSerializer turns each row into JSON\n"
        "9  The JSON travels back and React stores it in state with setData\n"
        "10 The table on screen re-renders with your rows",
    )
    base.add_numbers(
        doc,
        [
            "Front end means the code running in the browser: React, the pages, the components and the charts.",
            "Back end means the code running in Python: the views, the serializers, the models and the database.",
            "The API is the agreement between them: fixed web addresses that accept and return JSON.",
            "A model describes a table; a serializer shapes it; a view decides who may see it. Almost every feature you build later follows the same three steps.",
            "To add a new screen, you add a view, a web address, a service call and a page. Nothing else changes.",
        ],
    )
    add_check(
        doc,
        "You can explain to somebody else what happens between clicking a filter and seeing fewer "
        "rows.",
    )

    doc.add_heading("Lesson 27. Errors you will meet and how to fix them", level=1)
    add_goal(doc, "Recognise the most common beginner errors and repair them quickly.")
    doc.add_paragraph(
        "Every developer meets these messages. They are not a sign that you are doing something "
        "wrong; they are the tools telling you exactly what to fix."
    )
    base.add_table(
        doc,
        ["Message you see", "What it means", "How to fix it"],
        [
            ["python is not recognized", "Python is not on the system path", "Reinstall Python and tick Add python.exe to PATH"],
            ["pip is not recognized", "The virtual environment is not switched on", "Run venv\\Scripts\\activate, then try again"],
            ["npm is not recognized", "Node.js is not installed or needs a new terminal", "Reinstall Node.js LTS and open a fresh terminal"],
            ["running scripts is disabled on this system", "Windows blocks the activation script", "Run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser, answer Yes, then activate again"],
            ["No module named django", "The environment is off or packages are missing", "Activate venv, then pip install -r requirements.txt"],
            ["manage.py not found", "The terminal is in the wrong folder", "Run cd backend and try again"],
            ["No such table: banking_transaction", "The database tables were never created", "Run python manage.py migrate, then seed_demo --flush"],
            ["Port 8000 is already in use", "The backend is already running elsewhere", "Use the running one, or runserver 127.0.0.1:8001 and update frontend/.env"],
            ["EADDRINUSE port 5173", "The website is already running in another terminal", "Use the existing window, or stop it with Ctrl+C first"],
            ["Cannot find module or Failed to resolve import", "A file name or folder does not match", "Check the capitals and the folder path against this guide"],
            ["Red banner saying the API cannot be reached", "The backend terminal is not running", "Start the backend with runserver and refresh the page"],
            ["CORS policy error in the browser", "The website address is not allowed by the backend", "Check CORS_ALLOWED_ORIGINS in backend/.env includes http://localhost:5173"],
            ["401 Unauthorized on every request", "The login token has expired", "Log out and log in again"],
            ["The page is blank with an error in the terminal", "A syntax error in the last file you edited", "Read the file name and line number in the message and compare that file with this guide"],
            ["npm install stops with a blocked scripts warning", "The package manager blocked esbuild", "Run npm install-scripts approve esbuild, then npm install"],
        ],
        [5.0, 5.2, 7.0],
    )
    add_note(
        doc,
        "The habit that fixes most problems",
        "Read the first line of the error message, then look at the file name it mentions. Nine times "
        "out of ten the answer is a missing line, a wrong folder or a server that is not running.",
    )
    add_check(doc, "You know where to look when something breaks instead of starting again from scratch.")

    doc.add_heading("Lesson 28. Stop, start and restart everything", level=1)
    add_goal(doc, "Keep the project easy to pick up after a break.")
    doc.add_paragraph("Use these commands whenever you return to the project on a new day.")
    base.add_code(
        doc,
        "# stop anything running: click in the terminal and press\n"
        "Ctrl + C\n"
        "\n"
        "# start the backend (terminal 1)\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000\n"
        "\n"
        "# start the website (terminal 2)\n"
        "cd banking_app/frontend\n"
        "npm run dev\n"
        "\n"
        "# if the demo data ever looks wrong\n"
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py seed_demo --flush",
    )
    base.add_table(
        doc,
        ["Address", "What it shows", "Who can open it"],
        [
            ["http://localhost:5173", "The website", "Everyone"],
            ["http://127.0.0.1:8000/api/", "The API", "Logged in accounts only"],
            ["http://127.0.0.1:8000/admin/", "Django admin for the pretend data", "The admin account"],
        ],
        [5.4, 6.6, 5.2],
    )
    add_check(
        doc,
        "You can start, stop and reset the project without re-reading the whole guide.",
    )

    doc.add_heading("Lesson 29. What to learn next", level=1)
    add_goal(doc, "Turn this project into a learning path.")
    base.add_numbers(
        doc,
        [
            "Change one screen at a time. Pick the notifications page, add a filter for the notification type, and follow the chain from view to serializer to service to page.",
            "Add a new field. Add a nickname to the customer profile in backend/users/models.py, run makemigrations and migrate, expose it in the serializer, then show it on the profile page.",
            "Add a new endpoint. Build /api/spending-by-month/ that returns one number per month, then draw it as a new chart on the dashboard.",
            "Improve the assistant. Add intents for questions such as which month did I spend the most, and reuse the helpers in services.py instead of writing new maths.",
            "Learn Git. Put the project in a repository so you can see your own history and try changes safely.",
            "Learn testing. Add a test for every new feature you build, following the style of the existing tests.",
            "Learn deployment. Put the backend on a host such as Render or Railway and the website on a static host such as Netlify or Vercel, then update VITE_API_BASE_URL.",
            "Read the code you already have. Every file in this guide is written to be read, and the comments explain the decisions rather than repeating the code.",
        ],
    )
    add_check(
        doc,
        "You have a project you understand, a habit of checking your work, and a list of next steps. "
        "That is what finishing a first full stack project looks like.",
    )

    # ------------------------------------------------------------- appendices
    base.page_break(doc)
    doc.add_heading("Appendix A. Plain English word list", level=1)
    doc.add_paragraph(
        "Every word below appears in this guide. Keep this page nearby when a term feels unfamiliar."
    )
    base.add_table(
        doc,
        ["Word", "What it means in plain English"],
        [
            ["Terminal", "The text window where you type commands. In VS Code it opens at the bottom of the screen."],
            ["Command", "One line of instruction typed in the terminal and run with Enter."],
            ["Folder and path", "A folder stores files; a path is the address of a file, such as backend/config/settings.py."],
            ["VS Code", "The free editor from Microsoft where you create files and run commands."],
            ["Extension", "An add on for VS Code that adds features such as Python support."],
            ["Virtual environment", "A private box of Python libraries belonging to one project."],
            ["Package or library", "Ready made code written by somebody else that your project uses."],
            ["pip", "The Python tool that downloads packages."],
            ["npm", "The Node.js tool that downloads packages for the website."],
            ["Node.js", "The program that runs the website building tools."],
            ["Django", "The Python framework that provides the backend structure."],
            ["React", "The JavaScript library that builds the screens in the browser."],
            ["Vite", "The tool that runs the website while you work and builds the final version."],
            ["Component", "A reusable piece of a screen, such as a button or a card."],
            ["Prop", "A value you pass into a component so it can display something."],
            ["State", "Data a screen keeps in memory while it is open, such as the list of transactions."],
            ["Hook", "A React function that lets a component remember things or run code at the right moment."],
            ["API", "The set of web addresses your backend answers, and the JSON it exchanges."],
            ["Endpoint", "One of those web addresses, for example /api/dashboard/."],
            ["Request and response", "The message the website sends and the message the backend sends back."],
            ["JSON", "A simple text format for structured data, which both sides understand."],
            ["JWT or token", "A signed pass that proves you are logged in; the website sends it with each request."],
            ["Model", "A description of a database table, written in Python."],
            ["Migration", "A file that tells the database how to create or change tables."],
            ["ORM", "The part of Django that lets you work with database rows using Python instead of SQL."],
            ["Serializer", "The code that turns database rows into JSON and checks incoming data."],
            ["View", "The function that decides what to answer for one web address."],
            ["CORS", "The browser rule that decides which website addresses may call the backend."],
            ["Seed data", "Pretend rows created by a command so the app has something to show."],
            ["Build", "Packaging the website into final files for hosting."],
            ["localhost and port", "Your own computer, and the numbered channel such as 8000 or 5173 that a program listens on."],
        ],
        [4.0, 13.2],
    )

    doc.add_heading("Appendix B. Every file and what it does", level=1)
    doc.add_paragraph(
        "The manifest lists all ninety-two files in the project with their purpose and length, "
        "including the generated ones explained in the note below the table."
    )
    manifest = []
    for rel_path, purpose in base.MANIFEST:
        path = ROOT / rel_path
        lines = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
        manifest.append([rel_path, purpose, str(lines)])
    base.add_table(
        doc,
        ["Path", "What it does", "Lines"],
        manifest,
        [6.4, 9.0, 1.8],
        font_size=Pt(8.5),
        header_size=Pt(8.5),
    )
    doc.add_paragraph(
        "Generated files that you never paste by hand: db.sqlite3 is the database created by "
        "migrate, the migrations folders are created by makemigrations, node_modules and "
        "package-lock.json are created by npm install, and dist is created by npm run build. The two "
        "environment files are copies of the .env.example files."
    )

    doc.add_heading("Appendix C. Logins and the demo script", level=1)
    base.add_table(
        doc,
        ["Role", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345", "Balance 85,450, income 45,000, spending 18,450, two loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "A second customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "A third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "The employee area and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Use this sequence when you show the project to somebody else.")
    base.add_numbers(
        doc,
        [
            "Landing page: the hero, the six features and the assistant preview.",
            "Log in as the demo customer and land on the dashboard.",
            "Read the four cards, then switch the chart tabs.",
            "Open the account page and point out the hidden account number.",
            "Filter the transactions, then open one transaction in full.",
            "Open the loans page and submit an application with the live EMI preview.",
            "Open the EMI calculator and move the sliders.",
            "Ask the assistant five questions, then open the history panel.",
            "Mark a notification as read.",
            "Log in as the bank employee, approve the pending loan, then open analytics and AI monitoring.",
        ],
    )

    doc.add_heading("Appendix D. The API in one table", level=1)
    doc.add_paragraph(
        "Every address below returns JSON. All of them need a login token except register, login and "
        "refresh, and the employee addresses also require the bank employee role."
    )
    base.add_table(
        doc,
        ["Method", "Address", "What it does"],
        [
            ["POST", "/api/auth/register/", "Create a new pretend customer"],
            ["POST", "/api/auth/login/", "Log in and receive your tokens"],
            ["POST", "/api/auth/refresh/", "Renew an expired token"],
            ["GET, PUT", "/api/profile/", "Read or update your details"],
            ["GET", "/api/dashboard/", "Everything the dashboard shows"],
            ["GET", "/api/account/", "Your masked account details"],
            ["GET", "/api/transactions/", "Your transactions with filters and paging"],
            ["GET", "/api/transactions/<id>/", "One transaction"],
            ["GET, POST", "/api/loans/", "Your loans, or a new application"],
            ["GET", "/api/loans/<id>/", "One loan"],
            ["POST", "/api/emi/", "Calculate an EMI"],
            ["GET", "/api/notifications/", "Your notifications"],
            ["PUT", "/api/notifications/<id>/", "Mark one as read"],
            ["POST", "/api/notifications/read-all/", "Mark all as read"],
            ["POST", "/api/assistant/chat/", "Ask the assistant a question"],
            ["GET, DELETE", "/api/assistant/history/", "Read or clear your chat history"],
            ["GET", "/api/admin/analytics/", "Employee totals and charts"],
            ["GET", "/api/admin/customers/", "Employee customer table"],
            ["GET", "/api/admin/transactions/", "Employee transaction table"],
            ["GET", "/api/admin/loans/", "Employee loan table"],
            ["PATCH", "/api/admin/loans/<id>/", "Approve, activate or reject a loan"],
            ["GET", "/api/assistant/monitor/", "Assistant monitoring for employees"],
        ],
        [2.4, 6.4, 8.4],
    )

    doc.save(OUTPUT)
    print(f"wrote {OUTPUT}")


def main() -> None:
    page_map = {}
    if len(sys.argv) > 1:
        page_map = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    build(page_map)


if __name__ == "__main__":
    main()
