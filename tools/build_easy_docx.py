#!/usr/bin/env python3
"""Build the very easy edition of the BankFlow guide.

Written for a first-time learner: short sentences, one action per numbered step,
a plain language reason for every step, and a check after each lesson. The complete
program is included, exactly as in the other editions.

Usage: python build_easy_docx.py [page-map.json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_bankflow_docx as base  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

ROOT = base.ROOT
OUTPUT = ROOT / "BankFlow-Very-Easy-Guide-with-Full-Code.docx"


# --------------------------------------------------------------------------- #
# small helpers that keep every lesson looking the same
# --------------------------------------------------------------------------- #
def one_line(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run("In one line: ")
    run.bold = True
    paragraph.add_run(text)


def needs(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run("What you need: ")
    run.bold = True
    paragraph.add_run(text)


def steps(doc, items) -> None:
    for index, item in enumerate(items, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(4)
        paragraph.paragraph_format.left_indent = Cm(0.6)
        paragraph.paragraph_format.first_line_indent = Cm(-0.6)
        run = paragraph.add_run(f"{index}. ")
        run.bold = True
        paragraph.add_run(item)


def see(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run("You should see: ")
    run.bold = True
    paragraph.add_run(text)


def done(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(10)
    run = paragraph.add_run("Done when: ")
    run.bold = True
    paragraph.add_run(text)


def problems(doc, text: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(10)
    run = paragraph.add_run("If it does not work: ")
    run.bold = True
    paragraph.add_run(text)


def new_words(doc, items) -> None:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.add_run("New words in this lesson:").bold = True
    for word, meaning in items:
        line = doc.add_paragraph(style="List Bullet")
        line.paragraph_format.space_after = Pt(2)
        run = line.add_run(f"{word} - ")
        run.bold = True
        line.add_run(meaning)


def command(doc, text: str, what: str = "") -> None:
    if what:
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.add_run(what).italic = True
    base.add_code(doc, text)


def code_file(doc, rel_path: str, where: str, what: str) -> None:
    doc.add_heading(rel_path, level=3)
    line = doc.add_paragraph(style="FileNote")
    line.add_run("Where it goes: ")
    line.add_run(where)
    line2 = doc.add_paragraph(style="FileNote")
    line2.add_run("What it does: ")
    line2.add_run(what)
    line3 = doc.add_paragraph(style="FileNote")
    line3.add_run(
        "Copy the whole block below without changing anything. In VS Code click at the start of the "
        "first line, drag to the last line, press Ctrl+C, then paste it into your new file with Ctrl+V."
    )
    base.add_code(doc, (ROOT / rel_path).read_text(encoding="utf-8"))


def build(page_map: dict) -> None:
    doc = Document()
    base.configure_styles(doc)
    doc.styles["Normal"].font.size = Pt(12)
    doc.styles["Normal"].paragraph_format.space_after = Pt(8)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.2
    code_style = doc.styles["CodeBlock"]
    code_style.font.size = Pt(8)
    code_style.paragraph_format.line_spacing = Pt(9.6)
    base.page_setup(doc)

    # -------------------------------------------------------------------- cover
    doc.add_paragraph("BankFlow Very Easy Guide Build Your First Website", style="Title")
    doc.add_paragraph(
        "This guide is for someone who has never made a website. It uses short sentences and one "
        "action at a time. If you can click, copy and paste, you can finish it."
    )
    doc.add_paragraph(
        "You will build a pretend bank called BankFlow. It has a login page, a dashboard with "
        "charts, a list of transactions, a loan form, an EMI calculator and a chat assistant that "
        "answers questions about your pretend money."
    )
    doc.add_paragraph(
        "The whole program is inside this book. You never write new code. You copy the code shown "
        "and you run the commands shown. That is how everyone starts."
    )

    doc.add_heading("The whole project in one picture", level=1)
    doc.add_paragraph(
        "Think of a bank branch. Customers stand in the lobby. Behind a counter, staff do the real "
        "work. Behind the staff there is a record room full of files."
    )
    base.add_table(
        doc,
        ["In the bank branch", "In our project", "What it is"],
        [
            ["The lobby customers see", "The website, called the frontend",
             "Pages and buttons that run inside your browser"],
            ["The counter where you ask", "The API",
             "Fixed web addresses that accept questions and give answers"],
            ["The staff behind the counter", "The backend, written in Python with Django",
             "It checks who you are and decides what to send back"],
            ["The record room", "The database, a file called db.sqlite3",
             "It stores the customers, transactions and loans"],
            ["A helpful clerk who reads your file", "The AI assistant",
             "It reads your own pretend data and answers in words"],
        ],
        [4.6, 5.8, 6.8],
    )
    doc.add_paragraph(
        "That is the whole idea. The website cannot see the record room directly. It must ask the "
        "counter, and the staff check that you are allowed to see the answer. Everything else in "
        "this book is detail."
    )

    doc.add_heading("Two ways to build this project", level=1)
    doc.add_paragraph(
        "Read both options and pick one. Both are honest ways to learn, and you can switch later."
    )
    doc.add_paragraph().add_run("Path A, the fast path.").bold = True
    doc.add_paragraph(
        "You already have a ready made folder of the project. Copy it to your laptop, install the "
        "tools in Lessons 1 to 6, then jump to Lesson 16 to start the backend and Lesson 24 to "
        "start the website. Use the rest of the book as a dictionary when you want to understand a "
        "file. This path takes about an hour and is the best choice if your goal is to see it work."
    )
    doc.add_paragraph().add_run("Path B, the learning path.").bold = True
    doc.add_paragraph(
        "You do every lesson in order and create all ninety-two files by copying them from this "
        "book. This takes longer, perhaps two or three evenings, but at the end you will have typed "
        "every part yourself and you will understand how a real project is put together. This is "
        "the path the book is written for."
    )

    doc.add_heading("Seven rules that make this easy", level=1)
    steps(
        doc,
        [
            "Do one lesson, then stop and do its check. Never continue with a red error on your screen.",
            "Copy code exactly, including brackets, commas and empty lines. Small typing differences cause most errors.",
            "Keep your folders matching the headings in this book. A file in the wrong folder is the second most common error.",
            "Use the terminal inside VS Code. It already knows which folder you are working in.",
            "When a command finishes, read its last line. That line tells you if it worked.",
            "Two programs must run at the same time later: the backend and the website. Keep both windows open.",
            "When you feel lost, look at the picture above and ask yourself: am I working on the lobby, the counter, the staff, or the record room?",
        ],
    )

    doc.add_heading("Contents", level=1)
    contents = [
        ("Part 1 Lesson 1. Install Visual Studio Code", "lesson1"),
        ("Part 1 Lesson 2. Install Python", "lesson2"),
        ("Part 1 Lesson 3. Install Node.js", "lesson3"),
        ("Part 1 Lesson 4. Add two VS Code extensions", "lesson4"),
        ("Part 1 Lesson 5. Learn five things in VS Code", "lesson5"),
        ("Part 1 Lesson 6. Make your folders", "lesson6"),
        ("Part 2 Lesson 7. What a backend is and which files it needs", "lesson7"),
        ("Part 2 Lesson 8. Turn on your private Python box", "lesson8"),
        ("Part 2 Lesson 9. Create four simple backend files", "lesson9"),
        ("Part 2 Lesson 10. Create the settings folder", "lesson10"),
        ("Part 2 Lesson 11. Create the users app for logging in", "lesson11"),
        ("Part 2 Lesson 12. Create the banking tables and the maths file", "lesson12"),
        ("Part 2 Lesson 13. Create the banking web addresses", "lesson13"),
        ("Part 2 Lesson 14. Create the pretend data command", "lesson14"),
        ("Part 2 Lesson 15. Create the AI assistant app", "lesson15"),
        ("Part 2 Lesson 16. Build the database and fill it with pretend data", "lesson16"),
        ("Part 2 Lesson 17. Run the tests and start the backend", "lesson17"),
        ("Part 3 Lesson 18. What a website is and how to create the project", "lesson18"),
        ("Part 3 Lesson 19. Create the website settings files", "lesson19"),
        ("Part 3 Lesson 20. Create the files that talk to the backend", "lesson20"),
        ("Part 3 Lesson 21. Create the shared pieces of every page", "lesson21"),
        ("Part 3 Lesson 22. Create the customer pages", "lesson22"),
        ("Part 3 Lesson 23. Create the bank employee pages", "lesson23"),
        ("Part 3 Lesson 24. Start the website and log in", "lesson24"),
        ("Part 4 Lesson 25. A tour of every screen", "lesson25"),
        ("Part 4 Lesson 26. Four easy changes you can make", "lesson26"),
        ("Part 4 Lesson 27. How a click becomes data", "lesson27"),
        ("Part 4 Lesson 28. When something goes wrong", "lesson28"),
        ("Part 4 Lesson 29. Stop, start and start again", "lesson29"),
        ("Part 4 Lesson 30. What to learn next", "lesson30"),
        ("Appendix A. Words explained simply", "appendixa"),
        ("Appendix B. Every file and what it does", "appendixb"),
        ("Appendix C. Logins and the demo script", "appendixc"),
        ("Appendix D. All the commands in one place", "appendixd"),
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

    # ============================================================ part 1
    doc.add_heading("Part 1. Get your laptop ready", level=1)
    doc.add_paragraph(
        "You will install four programs. Two of them make the project run, one is the editor where "
        "you work, and one adds helpful features to that editor. Do them in this order."
    )
    doc.add_paragraph(
        "Each lesson takes ten to fifteen minutes. You only install these once. After today you "
        "will never repeat Part 1 on this laptop."
    )

    doc.add_heading("Lesson 1. Install Visual Studio Code", level=1)
    one_line(doc, "Put the editor on your laptop. This is where you write files and run commands.")
    needs(doc, "An internet connection and about ten minutes.")
    doc.add_paragraph(
        "Visual Studio Code is free. People call it VS Code. It has two parts you will use: a side "
        "list of your files, and a black panel at the bottom called the terminal."
    )
    steps(
        doc,
        [
            "Open your browser and go to code.visualstudio.com.",
            "Click the blue Download button for Windows.",
            "Open the file that was downloaded. Its name starts with VSCodeUserSetup.",
            "Click I accept the agreement, then click Next.",
            "Leave the folder as it is and click Next.",
            "Tick Add to PATH. Tick both boxes that start with Open with Code.",
            "Click Next, then Install, then Finish.",
            "VS Code opens. Close the Welcome tab with its small x.",
        ],
    )
    new_words(
        doc,
        [
            ("Editor", "The program where you write files. VS Code is your editor."),
            ("PATH", "A list that lets you start a program by typing its name in the terminal."),
        ],
    )
    see(doc, "An empty VS Code window with a Welcome tab, and a tall icon bar on the left.")
    done(doc, "VS Code is installed and open.")
    problems(doc, "Install it again and make sure Add to PATH is ticked.")

    doc.add_heading("Lesson 2. Install Python", level=1)
    one_line(doc, "Install the language that runs the backend, the staff behind the counter.")
    needs(doc, "About ten minutes. Read step 4 carefully, it matters.")
    steps(
        doc,
        [
            "Go to python.org/downloads.",
            "Click the yellow Download Python button.",
            "Open the downloaded file.",
            "On the first screen, tick the box at the bottom that says Add python.exe to PATH.",
            "Click Install Now and wait.",
            "Click Close when it finishes.",
            "Press the Windows key, type cmd, and press Enter. A black window opens.",
            "Type python --version and press Enter.",
        ],
    )
    command(doc, "python --version", "Type this in the black window.")
    see(doc, "A line like Python 3.14.5. The number can be newer.")
    done(doc, "Python prints a version number.")
    problems(
        doc,
        "If the window says python is not recognized, run the installer again, choose Modify, tick "
        "Add python.exe to PATH, and open a new black window.",
    )
    new_words(
        doc,
        [
            ("Python", "The language the backend is written in."),
            ("Terminal or command prompt", "The black text window where you type commands."),
        ],
    )

    doc.add_heading("Lesson 3. Install Node.js", level=1)
    one_line(doc, "Install the tool that builds the website in the browser.")
    needs(doc, "About ten minutes.")
    steps(
        doc,
        [
            "Go to nodejs.org.",
            "Click the button marked LTS. Do not pick Current.",
            "Open the downloaded file.",
            "Click Next through every screen. Keep the default folder.",
            "Leave the checkbox on the Tools for Native Modules screen empty.",
            "Click Install, wait, then click Finish.",
            "In the same black window type node --version and press Enter.",
            "Then type npm --version and press Enter.",
        ],
    )
    command(doc, "node --version\nnpm --version")
    see(doc, "Two version numbers, one after the other, such as v24.19.0 and 12.0.2.")
    done(doc, "Both commands print a number.")
    problems(doc, "Install Node.js again, then close the black window and open a new one.")
    new_words(
        doc,
        [
            ("Node.js", "A program that runs the tools which build the website."),
            ("npm", "The tool that downloads ready made code for the website."),
        ],
    )

    doc.add_heading("Lesson 4. Add two VS Code extensions", level=1)
    one_line(doc, "Teach VS Code about Python and about React, so it can highlight your code.")
    needs(doc, "VS Code open. About five minutes.")
    doc.add_paragraph(
        "Extensions are add ons. They colour your code, warn you about mistakes and keep the "
        "spacing tidy. The project works without them, but they make everything easier to read."
    )
    steps(
        doc,
        [
            "In VS Code press Ctrl+Shift+X. The Extensions panel opens on the left.",
            "Type Python in the search box. Find the one made by Microsoft and click Install.",
            "Clear the search box and type ES7 React snippets. Install the one with the most downloads.",
            "Clear the box again and type Prettier. Install the one made by Prettier.",
            "Press Ctrl+Shift+X again to close the panel.",
        ],
    )
    see(doc, "Each installed extension shows the word Installed and no Install button.")
    done(doc, "Three extensions are installed.")
    problems(doc, "Check your internet connection and try again.")

    doc.add_heading("Lesson 5. Learn five things in VS Code", level=1)
    one_line(doc, "Practise the only five actions this whole book needs.")
    needs(doc, "VS Code open. About ten minutes.")
    base.add_table(
        doc,
        ["What you want", "How to do it", "What happens"],
        [
            ["Open a folder", "Click File, then Open Folder, then choose your folder",
             "The folder name appears at the top of the left sidebar"],
            ["Make a new file", "Right click in the sidebar, click New File, type the name, press Enter",
             "A blank tab opens with that file name"],
            ["Save your work", "Press Ctrl+S",
             "The little dot on the file tab disappears"],
            ["Open the terminal", "Click Terminal, then New Terminal",
             "A panel opens at the bottom with a command line"],
            ["Run a command", "Click in the terminal, type the command, press Enter",
             "The terminal prints the result"],
        ],
        [4.2, 6.6, 6.4],
    )
    steps(
        doc,
        [
            "Open the folder you will create in the next lesson, using File then Open Folder.",
            "Right click in the sidebar and make a file called practice.txt.",
            "Type the word hello inside it and press Ctrl+S.",
            "Open the terminal with Terminal then New Terminal.",
            "Type dir and press Enter.",
        ],
    )
    see(doc, "The terminal lists your files, including practice.txt. You can delete that file afterwards.")
    done(doc, "You can open a folder, make a file, save it, open the terminal and run a command.")
    problems(doc, "Make sure you clicked inside the terminal panel before typing.")
    new_words(
        doc,
        [
            ("Sidebar", "The left list of files and folders in VS Code."),
            ("Terminal", "The panel at the bottom where commands are typed."),
        ],
    )

    doc.add_heading("Lesson 6. Make your folders", level=1)
    one_line(doc, "Create one main folder with two folders inside it.")
    needs(doc, "Two minutes.")
    steps(
        doc,
        [
            "Open File Explorer from the taskbar.",
            "Go to the place you keep your work, for example Documents.",
            "Right click an empty space, click New, then Folder, and name it banking_app.",
            "Open banking_app. Inside it make two folders: backend and frontend.",
            "Close File Explorer.",
            "In VS Code click File, then Open Folder, choose banking_app, and click Select Folder.",
            "If VS Code asks whether you trust the folder, click Yes, I trust the authors.",
        ],
    )
    doc.add_paragraph("Your sidebar should look like this.")
    base.add_code(doc, "BANKING_APP\n    backend\n    frontend")
    see(doc, "The sidebar shows banking_app with backend and frontend inside it.")
    done(doc, "Part 1 is finished. Your laptop now has every tool you need.")
    problems(doc, "Use File then Open Folder again and pick banking_app, not backend.")
    new_words(
        doc,
        [
            ("Folder", "A container for files. Ours is called banking_app."),
            ("backend and frontend", "The staff room and the lobby, in folder form."),
        ],
    )

    # ============================================================ part 2
    base.page_break(doc)
    doc.add_heading("Part 2. Build the backend", level=1)
    doc.add_paragraph(
        "The backend is the staff behind the counter. It stores the pretend money data and answers "
        "questions from the website. You build it first, because the website needs something to "
        "talk to."
    )
    doc.add_paragraph(
        "Everything in Part 2 happens in the VS Code terminal, and the terminal must be inside the "
        "backend folder. There are eight lessons. Each one is short."
    )

    doc.add_heading("Lesson 7. What a backend is and which files it needs", level=1)
    one_line(doc, "Understand the shape of the backend before you create it.")
    needs(doc, "Ten minutes of reading. No typing yet.")
    doc.add_paragraph(
        "Django is a ready made backend. It gives you a structure so you do not invent one. Inside "
        "the backend folder you will create three groups of files, called apps, plus one settings "
        "folder."
    )
    base.add_table(
        doc,
        ["Folder", "In plain words", "What it holds"],
        [
            ["config", "The instructions for the whole building",
             "Settings, web addresses and the start up files"],
            ["users", "The staff who check identity",
             "Logging in, roles, and customer details"],
            ["banking", "The staff who handle money records",
             "Accounts, transactions, loans and notifications"],
            ["assistant", "The helpful clerk who answers questions",
             "Saved conversations and the answering logic"],
        ],
        [3.2, 6.6, 7.4],
    )
    doc.add_paragraph(
        "A file named models.py describes a table in the record room. A file named views.py decides "
        "what to answer when somebody asks. A file named serializers.py turns a database row into "
        "text the website can read. Every app has these, which is why the same pattern repeats."
    )
    doc.add_paragraph(
        "Two files do the thinking. services.py holds the money maths, such as EMI and monthly "
        "totals. ai_service.py holds the question answering. Everything else is plumbing."
    )
    done(doc, "You can say what config, users, banking and assistant are for.")
    new_words(
        doc,
        [
            ("Django", "A ready made backend structure written in Python."),
            ("App", "A folder that groups related backend features."),
            ("Model", "A description of one table in the database."),
            ("View", "The code that answers one web address."),
        ],
    )

    doc.add_heading("Lesson 8. Turn on your private Python box", level=1)
    one_line(doc, "Create a private space for the project's Python libraries and install them.")
    needs(doc, "The backend folder open in VS Code. About fifteen minutes.")
    doc.add_paragraph(
        "Your laptop may have other Python projects. A virtual environment is a private box of "
        "libraries used only by BankFlow, so nothing clashes. You create it once."
    )
    doc.add_paragraph("Open the terminal in VS Code and type these two lines, pressing Enter after each.")
    command(doc, "cd backend\npython -m venv venv", "The first line moves you into the backend folder.")
    see(doc, "A new folder named venv appears inside backend in the sidebar.")
    doc.add_paragraph(
        "Now switch the box on. On Windows type the line below. On macOS or Linux type "
        "source venv/bin/activate instead. Type only one of them, never both."
    )
    command(doc, "venv\\Scripts\\activate", "The Windows line. Ignore the (venv) text in the explanation; you type only this line.")
    see(doc, "The start of the terminal line now shows (venv).")
    doc.add_paragraph("With (venv) showing, install the backend libraries. This downloads them from the internet.")
    command(
        doc,
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"",
        "One long line. Copy it whole.",
    )
    see(doc, "The last line starts with Successfully installed.")
    done(doc, "The terminal shows (venv) and the libraries are installed.")
    problems(
        doc,
        "If it says pip is not recognized, the box is off. Run the activate line again. If it says "
        "No module named django later, run activate again in that terminal.",
    )
    new_words(
        doc,
        [
            ("Virtual environment", "A private box of libraries for one project. Ours is called venv."),
            ("pip", "The tool that downloads Python libraries."),
            ("Library", "Ready made code written by other people."),
        ],
    )

    doc.add_heading("Lesson 9. Create four simple backend files", level=1)
    one_line(doc, "Make the small files that sit directly inside the backend folder.")
    needs(doc, "About fifteen minutes.")
    doc.add_paragraph(
        "For every file in this book: right click the folder named in Where it goes, click New File, "
        "type the name exactly, press Enter, paste the code, then press Ctrl+S."
    )
    code_file(doc, "backend/requirements.txt", "inside the backend folder",
              "A shopping list of the libraries, so another computer can install the same ones.")
    code_file(doc, "backend/.env.example", "inside the backend folder",
              "A template for settings and secrets. You copy it to .env in a moment.")
    code_file(doc, "backend/.gitignore", "inside the backend folder",
              "Tells Git to ignore private files. Nothing to run.")
    code_file(doc, "backend/manage.py", "inside the backend folder",
              "The command file. Every backend command starts with python manage.py.")
    doc.add_paragraph("Now make your own copy of the settings file.")
    command(
        doc,
        "copy .env.example .env",
        "Type this in the terminal. On macOS or Linux the same command is: cp .env.example .env",
    )
    see(doc, "The sidebar shows a new file named .env next to .env.example.")
    done(doc, "Four files plus the .env copy exist inside backend.")
    problems(doc, "If a file looks empty, you forgot to paste. Open it again and paste.")
    new_words(
        doc,
        [
            (".env", "A private file with settings and secrets. Never share it."),
            ("manage.py", "The file you run to give the backend instructions."),
        ],
    )

    doc.add_heading("Lesson 10. Create the settings folder", level=1)
    one_line(doc, "Create the config folder that holds the instructions for the whole backend.")
    needs(doc, "About twenty minutes.")
    steps(
        doc,
        [
            "Right click backend in the sidebar, click New Folder, and name it config.",
            "Create the five files below inside the config folder.",
            "After the last file, run the check command at the end of this lesson.",
        ],
    )
    code_file(doc, "backend/config/__init__.py", "inside the config folder",
              "An empty file that tells Python this folder contains code.")
    code_file(doc, "backend/config/settings.py", "inside the config folder",
              "The most important file. It lists what is switched on, where the database lives and "
              "how long a login lasts. This is the best file in the project to read slowly.")
    code_file(doc, "backend/config/urls.py", "inside the config folder",
              "The address book. It sends each web address to the right app.")
    code_file(doc, "backend/config/wsgi.py", "inside the config folder",
              "Used by hosting companies when the site goes online. Nothing to change.")
    code_file(doc, "backend/config/asgi.py", "inside the config folder",
              "A second start up file for newer servers. Nothing to change.")
    command(doc, "python manage.py check", "Ask Django to test your settings.")
    see(doc, "The words System check identified no issues, with a number in brackets.")
    done(doc, "The check passes, which means your settings are correct.")
    problems(
        doc,
        "If it says manage.py not found, your terminal is not in the backend folder. Type cd backend "
        "and try again.",
    )
    new_words(
        doc,
        [
            ("Settings", "The file that controls how the whole backend behaves."),
            ("URL", "A web address, such as /api/dashboard/."),
        ],
    )

    doc.add_heading("Lesson 11. Create the users app for logging in", level=1)
    one_line(doc, "Create the files that handle accounts, logins and customer details.")
    needs(doc, "About forty minutes, because there are twelve files.")
    doc.add_paragraph(
        "In most systems a user logs in with a username. BankFlow is more like a real bank, so "
        "people log in with their email address. Every user also has a role: customer, or bank "
        "employee. That role decides which pages they can open."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named users.",
            "Right click the new users folder and create a folder named urls.",
            "Create the twelve files below, pasting each one and pressing Ctrl+S.",
        ],
    )
    code_file(doc, "backend/users/__init__.py", "inside users", "Marks the folder as code.")
    code_file(doc, "backend/users/apps.py", "inside users", "Tells Django about this app and switches on the profile rule.")
    code_file(doc, "backend/users/models.py", "inside users",
              "The user table, the role choices, and the customer profile table.")
    code_file(doc, "backend/users/signals.py", "inside users",
              "Creates an empty profile automatically whenever a user is created.")
    code_file(doc, "backend/users/permissions.py", "inside users",
              "The rule that only bank employees may open employee pages.")
    code_file(doc, "backend/users/serializers.py", "inside users",
              "Checks the register form and shapes user data as text for the website.")
    code_file(doc, "backend/users/views.py", "inside users", "Answers the register and profile requests.")
    code_file(doc, "backend/users/urls/__init__.py", "inside users/urls", "Marks the folder as code.")
    code_file(doc, "backend/users/urls/auth_urls.py", "inside users/urls",
              "The register, login and refresh addresses.")
    code_file(doc, "backend/users/urls/profile_urls.py", "inside users/urls", "The profile address.")
    code_file(doc, "backend/users/admin.py", "inside users",
              "Lets you see and edit users in the built in admin page.")
    code_file(doc, "backend/users/tests.py", "inside users",
              "Automatic checks for logging in and updating a profile.")
    done(doc, "The users folder holds twelve files, including the small urls folder.")
    problems(doc, "Check the spelling and the capital letters of every file name.")
    new_words(
        doc,
        [
            ("Role", "Whether somebody is a customer or a bank employee."),
            ("Serializer", "The file that turns a database row into text for the website."),
            ("Test", "A small program that checks your work for you."),
        ],
    )

    doc.add_heading("Lesson 12. Create the banking tables and the maths file", level=1)
    one_line(doc, "Create the four money tables and the file that does all the calculations.")
    needs(doc, "About forty minutes. The maths file is long, so copy it in one piece.")
    doc.add_paragraph(
        "A model is a description of a table. Four tables cover this project: accounts, "
        "transactions, loans and notifications. You do not write database code; Django reads these "
        "descriptions and creates the tables for you."
    )
    doc.add_paragraph(
        "The file called services.py is where all the money maths lives. It knows how to work out "
        "an EMI, how much you spent this month, which category is biggest, and what the last six "
        "months look like. The dashboard, the charts and the AI assistant all call this one file, "
        "which is why every screen shows the same numbers."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named banking.",
            "Inside banking, create a folder named urls.",
            "Create the six files below, then continue to the next lesson for the rest of this app.",
        ],
    )
    code_file(doc, "backend/banking/__init__.py", "inside banking", "Marks the folder as code.")
    code_file(doc, "backend/banking/apps.py", "inside banking", "Tells Django about this app.")
    code_file(doc, "backend/banking/models.py", "inside banking",
              "The four tables: account, transaction, loan and notification.")
    code_file(doc, "backend/banking/services.py", "inside banking",
              "All the money maths and the list of pretend transactions. The most interesting file "
              "in the backend.")
    code_file(doc, "backend/banking/serializers.py", "inside banking",
              "Turns banking rows into text the website can display.")
    code_file(doc, "backend/banking/urls/__init__.py", "inside banking/urls", "Marks the folder as code.")
    done(doc, "The banking folder holds these six files, and the maths file is saved without errors.")
    problems(doc, "If the file looks shorter than the book, you missed a section. Paste it again.")
    new_words(
        doc,
        [
            ("Transaction", "One movement of money, either in or out."),
            ("EMI", "The fixed amount you pay every month for a loan."),
        ],
    )

    doc.add_heading("Lesson 13. Create the banking web addresses", level=1)
    one_line(doc, "Create the files that answer the website's questions.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "A view is the code that answers one web address. Some views are for customers and only "
        "show your own data. Others are for bank employees and show everybody's data. The two url "
        "files decide which address reaches which view."
    )
    base.add_table(
        doc,
        ["Address the website asks for", "Which file answers", "What comes back"],
        [
            ["/api/dashboard/", "banking/views.py", "Balance, income, spending and chart numbers"],
            ["/api/transactions/", "banking/views.py", "A page of transactions after filtering"],
            ["/api/loans/", "banking/views.py", "Your loans, or a new application"],
            ["/api/emi/", "banking/views.py", "The EMI for the numbers you typed"],
            ["/api/admin/analytics/", "banking/admin_views.py", "Totals for the whole pretend bank"],
            ["/api/admin/loans/<id>/", "banking/admin_views.py", "The loan after approving or rejecting"],
        ],
        [5.2, 5.0, 7.0],
    )
    code_file(doc, "backend/banking/views.py", "inside banking",
              "Customer addresses such as dashboard, transactions and loans.")
    code_file(doc, "backend/banking/admin_views.py", "inside banking",
              "Bank employee addresses that can see every customer.")
    code_file(doc, "backend/banking/urls/customer_urls.py", "inside banking/urls",
              "The list of customer addresses.")
    code_file(doc, "backend/banking/urls/admin_urls.py", "inside banking/urls",
              "The list of employee addresses.")
    code_file(doc, "backend/banking/admin.py", "inside banking",
              "Shows the four tables in the built in admin page.")
    code_file(doc, "backend/banking/tests.py", "inside banking",
              "Automatic checks for the banking addresses.")
    done(doc, "You can point at any address in the table above and say which file answers it.")
    problems(doc, "Make sure the two url files are inside the urls folder, not loose in banking.")
    new_words(
        doc,
        [
            ("Endpoint", "One web address your backend answers, such as /api/dashboard/."),
            ("JSON", "The simple text format both sides use to exchange data."),
        ],
    )

    doc.add_heading("Lesson 14. Create the pretend data command", level=1)
    one_line(doc, "Create the command that fills the record room with three pretend customers.")
    needs(doc, "About thirty minutes.")
    doc.add_paragraph(
        "Typing test data by hand would take hours. Instead you write a command once and run it "
        "whenever you want. It creates the three customers, their accounts, twenty-eight "
        "transactions across three months, six loans, some notifications and one saved chat."
    )
    doc.add_paragraph(
        "The numbers are chosen to match the demo you will show: balance 85,450 rupees, monthly "
        "income 45,000, monthly spending 18,450, and the biggest category Shopping at 7,200."
    )
    steps(
        doc,
        [
            "Right click banking and create a folder named management.",
            "Inside management, create a folder named commands.",
            "Create the three files below. The two __init__.py files are empty, but they must exist.",
        ],
    )
    code_file(doc, "backend/banking/management/__init__.py", "inside banking/management", "Marks the folder as code.")
    code_file(doc, "backend/banking/management/commands/__init__.py", "inside banking/management/commands", "Marks the folder as code.")
    code_file(doc, "backend/banking/management/commands/seed_demo.py", "inside banking/management/commands",
              "The command that creates all the pretend data. You run it in Lesson 16.")
    done(doc, "The path banking/management/commands/seed_demo.py exists exactly as written.")
    problems(
        doc,
        "Django only finds commands in that exact folder. If the name is different, the command "
        "will not appear later.",
    )
    new_words(
        doc,
        [
            ("Command", "A task you run by typing, such as seed_demo."),
            ("Seed data", "Pretend rows created so the app has something to show."),
        ],
    )

    doc.add_heading("Lesson 15. Create the AI assistant app", level=1)
    one_line(doc, "Create the chat feature that answers banking questions in sentences.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "The assistant works in three moves. First it works out what you asked. Then it looks up "
        "your own pretend data. Then it writes a sentence from that data."
    )
    doc.add_paragraph(
        "The important idea is that the numbers always come from the database. The assistant is "
        "never allowed to invent a balance. If you later add a paid AI key, the robot only rephrases "
        "the same numbers. If you do not add one, the built in answers handle everything."
    )
    steps(
        doc,
        [
            "Right click backend and create a folder named assistant.",
            "Create the nine files below, pasting each one.",
        ],
    )
    code_file(doc, "backend/assistant/__init__.py", "inside assistant", "Marks the folder as code.")
    code_file(doc, "backend/assistant/apps.py", "inside assistant", "Tells Django about this app.")
    code_file(doc, "backend/assistant/models.py", "inside assistant",
              "The chat table that stores every question and answer.")
    code_file(doc, "backend/assistant/ai_service.py", "inside assistant",
              "The heart of the feature: it recognises the question, reads your data and writes the "
              "answer. Read this file after the project works.")
    code_file(doc, "backend/assistant/serializers.py", "inside assistant",
              "Checks that the question is sensible and formats saved chats.")
    code_file(doc, "backend/assistant/views.py", "inside assistant",
              "The chat, history and monitoring addresses.")
    code_file(doc, "backend/assistant/urls.py", "inside assistant", "The assistant address list.")
    code_file(doc, "backend/assistant/admin.py", "inside assistant",
              "Shows saved chats in the built in admin page.")
    code_file(doc, "backend/assistant/tests.py", "inside assistant",
              "Automatic checks for every kind of question.")
    done(doc, "All three apps exist: users, banking and assistant. The backend is complete.")
    problems(doc, "If Django complains about a missing file later, it names the app in the message.")
    new_words(
        doc,
        [
            ("Intent", "What the assistant thinks you are asking about."),
            ("Fallback", "The built in answers used when no paid AI service is connected."),
        ],
    )

    doc.add_heading("Lesson 16. Build the database and fill it with pretend data", level=1)
    one_line(doc, "Turn your file descriptions into real tables, then fill them.")
    needs(doc, "About ten minutes.")
    doc.add_paragraph(
        "Three commands finish the backend. The first prepares the table instructions. The second "
        "creates the tables. The third fills them with the three pretend customers."
    )
    command(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush",
        "Run these three lines one at a time, waiting for each to finish.",
    )
    doc.add_paragraph("The last command prints the logins you will use for the rest of the book.")
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
    see(doc, "Those three logins, and a new file named db.sqlite3 inside backend.")
    done(doc, "The pretend bank exists. db.sqlite3 is your record room.")
    problems(
        doc,
        "If it says No such table, you skipped the migrate command. Run it again, then run seed_demo.",
    )
    new_words(
        doc,
        [
            ("Migration", "An instruction that creates or changes database tables."),
            ("db.sqlite3", "The database file. It is your pretend bank's record room."),
        ],
    )

    doc.add_heading("Lesson 17. Run the tests and start the backend", level=1)
    one_line(doc, "Check the backend with twenty-five automatic tests, then switch it on.")
    needs(doc, "About ten minutes.")
    doc.add_paragraph(
        "Tests are small programs that check your work. BankFlow has twenty-five of them. They "
        "create their own temporary data, try every important address, and compare the answers with "
        "what should happen. This is the fastest way to know your backend is healthy."
    )
    command(doc, "python manage.py test")
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
    see(doc, "The word OK at the end.")
    done(doc, "All twenty-five tests pass. Your backend is correct.")
    problems(
        doc,
        "The message names the file with the problem. Open that file, compare it with the code in "
        "this book, save it, and run the tests again.",
    )
    doc.add_paragraph("Now start the backend and leave it running.")
    command(doc, "python manage.py runserver 127.0.0.1:8000")
    doc.add_paragraph(
        "The terminal stops returning to the prompt and shows a line about watching for file "
        "changes. That means the server is on. Leave this terminal running and do not close it."
    )
    steps(
        doc,
        [
            "Open your browser and go to http://127.0.0.1:8000/admin/",
            "Log in with admin@bankflow.com and the password Admin@12345.",
            "Click Users on the left. You will see the three pretend customers.",
        ],
    )
    see(doc, "A page listing Mohammed Adnan, Aisha Khan and Rahul Verma.")
    done(doc, "Your backend is running and holds real data. Part 2 is finished.")
    problems(
        doc,
        "If the browser cannot open the page, the server is not running. Run the start command "
        "again. To stop the server later, click in the terminal and press Ctrl+C.",
    )
    new_words(
        doc,
        [
            ("Port", "The numbered channel a program listens on, here 8000."),
            ("localhost or 127.0.0.1", "Your own computer."),
        ],
    )

    # ============================================================ part 3
    base.page_break(doc)
    doc.add_heading("Part 3. Build the website", level=1)
    doc.add_paragraph(
        "The website is the lobby. It runs inside the browser and asks the backend for data when it "
        "needs it. You already have the staff working; now you build the room customers walk into."
    )
    doc.add_paragraph(
        "Open a second terminal for this part: in VS Code click the plus sign at the top right of "
        "the terminal panel. Keep the backend running in the first tab."
    )

    doc.add_heading("Lesson 18. What a website is and how to create the project", level=1)
    one_line(doc, "Understand the frontend, then create the project and download its libraries.")
    needs(doc, "About twenty minutes.")
    doc.add_paragraph(
        "A website is made of pages. Each page is built from pieces called components, such as a "
        "button, a card or a table. When you click something, the page asks the backend for data "
        "and then redraws itself. That is all that is happening on every screen you will build."
    )
    doc.add_paragraph(
        "React is the tool that builds these pages. Vite is the tool that runs the website while you "
        "work and packs it up at the end. You will create the project with two commands."
    )
    steps(
        doc,
        [
            "In your second terminal, move into the frontend folder.",
            "Create the React project inside it.",
            "Install the starter libraries.",
            "Install the four extra libraries BankFlow uses.",
        ],
    )
    command(
        doc,
        "cd ..\ncd frontend\nnpm create vite@latest . -- --template react\nnpm install",
        "Wait for each command to finish before typing the next.",
    )
    doc.add_paragraph(
        "If the terminal asks whether to continue in the current folder, answer yes. If it asks for "
        "a package name, just press Enter."
    )
    command(
        doc,
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons",
        "These add the buttons, cards, charts and the connection to your backend.",
    )
    see(doc, "Messages about added packages, with no red errors.")
    done(doc, "The frontend folder contains src, public and package.json.")
    problems(
        doc,
        "If npm is not recognized, install Node.js again from Lesson 3 and open a fresh terminal.",
    )
    new_words(
        doc,
        [
            ("React", "The tool that builds the pages you see in the browser."),
            ("Component", "A reusable piece of a page, such as a card."),
            ("npm", "The tool that downloads website libraries."),
        ],
    )

    doc.add_heading("Lesson 19. Create the website settings files", level=1)
    one_line(doc, "Replace the starter files with the BankFlow versions.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "The starter project comes with a demonstration page. You replace those files with ours. "
        "When a file already exists, open it and replace everything inside it, then press Ctrl+S."
    )
    doc.add_paragraph(
        "Two of these files are worth knowing. theme.js holds every colour and font, so you can "
        "restyle the whole website from one file. App.jsx lists every page and the address that "
        "shows it."
    )
    code_file(doc, "frontend/package.json", "frontend folder, replacing the existing file",
              "The list of libraries and the commands you can run.")
    code_file(doc, "frontend/vite.config.js", "frontend folder, replacing the existing file",
              "Tells Vite which port to use and how to build the site.")
    code_file(doc, "frontend/index.html", "frontend folder, replacing the existing file",
              "The outer page that loads everything else.")
    code_file(doc, "frontend/.env.example", "frontend folder, a new file",
              "A template that says where your backend is.")
    code_file(doc, "frontend/.gitignore", "frontend folder, replacing the existing file",
              "Tells Git to ignore downloaded files.")
    code_file(doc, "frontend/public/bankflow.svg", "public folder, replacing the existing icon",
              "The small picture shown on the browser tab.")
    code_file(doc, "frontend/src/index.css", "src folder, replacing the existing file",
              "A few global styles.")
    code_file(doc, "frontend/src/theme.js", "src folder, a new file",
              "Every colour, font and rounded corner in the website.")
    code_file(doc, "frontend/src/main.jsx", "src folder, replacing the existing file",
              "Starts the website and switches on the theme and login state.")
    code_file(doc, "frontend/src/App.jsx", "src folder, replacing the existing file",
              "The list of pages and their addresses.")
    command(doc, "copy .env.example .env", "In the terminal, inside the frontend folder.")
    doc.add_paragraph(
        "The starter project also contains src/App.css and a folder called src/assets with a logo. "
        "Right click each of them in the sidebar and click Delete. BankFlow does not use them."
    )
    see(doc, "The src folder holds main.jsx, App.jsx, theme.js and index.css.")
    done(doc, "Every settings file is saved, and the starter leftovers are deleted.")
    problems(doc, "If a page shows an import error later, the file name is probably misspelled.")
    new_words(
        doc,
        [
            ("Theme", "The file that decides colours, fonts and spacing."),
            ("Route", "A web address inside the website, such as /dashboard."),
        ],
    )

    doc.add_heading("Lesson 20. Create the files that talk to the backend", level=1)
    one_line(doc, "Create one connection file, five call files, the login memory and two helpers.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "When the website needs data, it calls one file called api.js. That file adds your login "
        "pass to the request, renews the pass automatically when it expires, and turns any error "
        "into a sentence the page can show. Because every request goes through it, you only write "
        "this logic once."
    )
    doc.add_paragraph(
        "Beside it, AuthContext.jsx remembers who is logged in, so any page can ask who you are and "
        "whether you are a bank employee."
    )
    steps(
        doc,
        [
            "Inside frontend/src, create three folders: services, context and utils.",
            "Create the eight files below in their folders.",
        ],
    )
    code_file(doc, "frontend/src/services/api.js", "src/services",
              "The single connection to the backend, with the login pass attached to every request.")
    code_file(doc, "frontend/src/services/authService.js", "src/services",
              "Register, log in and read your profile.")
    code_file(doc, "frontend/src/services/bankingService.js", "src/services",
              "Dashboard, transactions, loans, EMI and notifications.")
    code_file(doc, "frontend/src/services/aiService.js", "src/services",
              "Chat with the assistant and read saved history.")
    code_file(doc, "frontend/src/services/adminService.js", "src/services",
              "The bank employee calls.")
    code_file(doc, "frontend/src/context/AuthContext.jsx", "src/context",
              "Remembers who is logged in while the website is open.")
    code_file(doc, "frontend/src/utils/formatCurrency.js", "src/utils",
              "Writes rupees and dates the same way everywhere.")
    code_file(doc, "frontend/src/utils/calculations.js", "src/utils",
              "Works out an EMI instantly as you move a slider.")
    done(doc, "The three folders exist with their eight files saved.")
    problems(doc, "Folder names must be lowercase: services, context, utils.")
    new_words(
        doc,
        [
            ("Axios", "The small library that sends requests to your backend."),
            ("Token", "The signed pass that proves you are logged in."),
            ("State", "Data a page keeps in memory while it is open."),
        ],
    )

    doc.add_heading("Lesson 21. Create the shared pieces of every page", level=1)
    one_line(doc, "Create the nine components that appear on many pages.")
    needs(doc, "About forty minutes.")
    doc.add_paragraph(
        "A component is a piece of a page you write once and reuse. The sidebar, the top bar, the "
        "statistic cards, the transaction table and the chat bubble are all components. That is why "
        "every page has the same look, and why changing one file updates the whole website."
    )
    steps(
        doc,
        [
            "Inside frontend/src, create a folder named components.",
            "Create the nine files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/components/AppLayout.jsx", "src/components",
              "The frame around every private page: sidebar, top bar and content.")
    code_file(doc, "frontend/src/components/Navbar.jsx", "src/components",
              "The top bar with the page title, notifications and your name.")
    code_file(doc, "frontend/src/components/Sidebar.jsx", "src/components",
              "The list of pages on the left. It folds away on small screens.")
    code_file(doc, "frontend/src/components/DashboardCard.jsx", "src/components",
              "One statistic card, used four times on the dashboard.")
    code_file(doc, "frontend/src/components/TransactionTable.jsx", "src/components",
              "The transaction table, used by both customer and employee pages.")
    code_file(doc, "frontend/src/components/LoanCard.jsx", "src/components",
              "One loan summary with a repayment bar.")
    code_file(doc, "frontend/src/components/ChatMessage.jsx", "src/components",
              "One chat bubble, used for your question and the assistant's answer.")
    code_file(doc, "frontend/src/components/ProtectedRoute.jsx", "src/components",
              "Sends you to the login page when a page needs a login.")
    code_file(doc, "frontend/src/components/Common.jsx", "src/components",
              "Small helpers used everywhere: loading spinner, error message, empty state, status label.")
    done(doc, "The components folder holds nine files.")
    problems(doc, "Capital letters matter. AppLayout.jsx is not the same as applayout.jsx.")
    new_words(
        doc,
        [
            ("Prop", "A value you pass into a component so it can display something."),
            ("Layout", "The outer frame that stays the same while pages change inside it."),
        ],
    )

    doc.add_heading("Lesson 22. Create the customer pages", level=1)
    one_line(doc, "Create the fourteen pages a customer can visit.")
    needs(doc, "About two hours. This is the biggest lesson, so take it slowly.")
    doc.add_paragraph(
        "Each page follows the same pattern: it asks the backend for data, keeps the answer in "
        "memory, and draws it on screen. The table shows which address each page calls."
    )
    base.add_table(
        doc,
        ["Page file", "What the customer sees", "It calls this address"],
        [
            ["Landing.jsx", "The public introduction with the big headline", "nothing"],
            ["Login.jsx", "The login form with the demo accounts", "/api/auth/login/"],
            ["Register.jsx", "The sign up form", "/api/auth/register/"],
            ["Dashboard.jsx", "Balance, income, spending, loans and four charts", "/api/dashboard/"],
            ["Account.jsx", "Your account details, with the middle hidden", "/api/account/"],
            ["Transactions.jsx", "The list with search and filters", "/api/transactions/"],
            ["TransactionDetails.jsx", "One transaction in full", "/api/transactions/<id>/"],
            ["Loans.jsx", "Loans and the application form", "/api/loans/"],
            ["LoanDetails.jsx", "One loan and its repayment plan", "/api/loans/<id>/"],
            ["EMICalculator.jsx", "The EMI calculator with sliders", "/api/emi/"],
            ["AIAssistant.jsx", "The chat screen", "/api/assistant/chat/"],
            ["Notifications.jsx", "Your alerts", "/api/notifications/"],
            ["Profile.jsx", "Your details, which you can edit", "/api/profile/"],
            ["NotFound.jsx", "A friendly message for unknown addresses", "nothing"],
        ],
        [3.8, 7.4, 6.0],
    )
    steps(
        doc,
        [
            "Inside frontend/src, create a folder named pages.",
            "Create the fourteen files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/pages/Landing.jsx", "src/pages", "The first page a visitor sees.")
    code_file(doc, "frontend/src/pages/Login.jsx", "src/pages", "Logging in and remembering the pass.")
    code_file(doc, "frontend/src/pages/Register.jsx", "src/pages", "Creating a new pretend customer.")
    code_file(doc, "frontend/src/pages/Dashboard.jsx", "src/pages", "The main screen after logging in.")
    code_file(doc, "frontend/src/pages/Account.jsx", "src/pages", "Account details.")
    code_file(doc, "frontend/src/pages/Transactions.jsx", "src/pages", "The transaction list with filters.")
    code_file(doc, "frontend/src/pages/TransactionDetails.jsx", "src/pages", "A single transaction.")
    code_file(doc, "frontend/src/pages/Loans.jsx", "src/pages", "Loans and the application form.")
    code_file(doc, "frontend/src/pages/LoanDetails.jsx", "src/pages", "A single loan and its schedule.")
    code_file(doc, "frontend/src/pages/EMICalculator.jsx", "src/pages", "The EMI calculator.")
    code_file(doc, "frontend/src/pages/AIAssistant.jsx", "src/pages", "The chat assistant.")
    code_file(doc, "frontend/src/pages/Notifications.jsx", "src/pages", "The alerts page.")
    code_file(doc, "frontend/src/pages/Profile.jsx", "src/pages", "The profile page.")
    code_file(doc, "frontend/src/pages/NotFound.jsx", "src/pages", "The page for addresses that do not exist.")
    done(doc, "The pages folder holds fourteen files.")
    problems(doc, "Landing, Dashboard and AIAssistant are long. Copy them in one piece and save.")
    new_words(
        doc,
        [
            ("Page", "A screen the user can open, such as the dashboard."),
            ("Chart", "A picture of numbers, drawn by the Recharts library."),
        ],
    )

    doc.add_heading("Lesson 23. Create the bank employee pages", level=1)
    one_line(doc, "Create the six pages only a bank employee can open.")
    needs(doc, "About forty five minutes.")
    doc.add_paragraph(
        "These pages read the employee addresses, which return data for every customer. The route "
        "guard sends ordinary customers back to their own dashboard, and the backend refuses the "
        "request too, so the door is locked in two places."
    )
    steps(
        doc,
        [
            "Inside frontend/src/pages, create a folder named admin.",
            "Create the six files below inside it.",
        ],
    )
    code_file(doc, "frontend/src/pages/admin/AdminDashboard.jsx", "src/pages/admin",
              "Six totals, portfolio charts and the top customers table.")
    code_file(doc, "frontend/src/pages/admin/CustomerManagement.jsx", "src/pages/admin",
              "The customer table and the detail window.")
    code_file(doc, "frontend/src/pages/admin/TransactionManagement.jsx", "src/pages/admin",
              "Every customer's transactions with filters.")
    code_file(doc, "frontend/src/pages/admin/LoanManagement.jsx", "src/pages/admin",
              "Approve, activate or reject a loan application.")
    code_file(doc, "frontend/src/pages/admin/AdminAnalytics.jsx", "src/pages/admin",
              "The charts that summarise the whole pretend bank.")
    code_file(doc, "frontend/src/pages/admin/AIMonitor.jsx", "src/pages/admin",
              "What customers asked the assistant and how it answered.")
    done(doc, "All twenty pages exist: fourteen in pages, six in pages/admin.")
    problems(doc, "The admin folder must be inside the pages folder, not beside it.")
    new_words(
        doc,
        [
            ("Access", "Who is allowed to open a page."),
            ("Monitoring", "A page that lets staff watch how a feature is being used."),
        ],
    )

    doc.add_heading("Lesson 24. Start the website and log in", level=1)
    one_line(doc, "Run the website and click through it for the first time.")
    needs(doc, "Both the backend and the frontend. About ten minutes.")
    doc.add_paragraph(
        "Your backend should still be running in the first terminal tab. In the second tab, make "
        "sure you are inside the frontend folder, then start the website."
    )
    command(doc, "npm run dev")
    doc.add_paragraph(
        "The terminal prints a Local address, usually http://localhost:5173. Open that address in "
        "your browser. Keep both terminals running."
    )
    steps(
        doc,
        [
            "The landing page appears with the headline Your Smarter Digital Banking Experience.",
            "Click Login.",
            "Click the line with mohammed@bankflow.com to fill the form, then click Login.",
            "The dashboard appears with a balance of 85,450 rupees.",
            "Click AI Assistant in the left list and ask: What is my balance?",
            "The assistant answers with the same 85,450 rupees, because it reads the same database.",
        ],
    )
    see(doc, "Four statistic cards, four charts, and an assistant that answers your question.")
    done(doc, "The website and the backend are talking to each other. You built both of them.")
    problems(
        doc,
        "If the page loads but every message says the API cannot be reached, the backend terminal "
        "has stopped. Go to that tab and run the start command again.",
    )
    new_words(
        doc,
        [
            ("local address", "The address of the website running on your own computer."),
            ("Refresh", "Pressing F5 to load the page again."),
        ],
    )

    # ============================================================ part 4
    base.page_break(doc)
    doc.add_heading("Part 4. Practise and understand", level=1)
    doc.add_paragraph(
        "The hard work is done. This part turns the finished project into your own learning ground. "
        "You will walk every screen, change things on purpose, and trace how a click becomes data."
    )

    doc.add_heading("Lesson 25. A tour of every screen", level=1)
    one_line(doc, "See every feature in the order you would show it to somebody.")
    needs(doc, "Twenty minutes of clicking.")
    base.add_table(
        doc,
        ["Screen", "What to do", "What it teaches"],
        [
            ["Landing page", "Scroll down slowly", "How a public page is built from sections"],
            ["Login", "Click the demo line, then log in", "How a login is checked and remembered"],
            ["Dashboard", "Read the four cards, then switch chart tabs", "Turning one answer into cards and charts"],
            ["Account", "Look at the hidden middle of the number", "Never showing a full account number"],
            ["Transactions", "Search Swiggy, then filter Shopping", "Filtering and paging on the backend"],
            ["Transaction details", "Open any row", "How one record is loaded by its number"],
            ["Loans", "Open the form and watch the EMI change", "Instant maths and saving a new record"],
            ["Loan details", "Read the instalment table", "Turning a loan into a monthly plan"],
            ["EMI calculator", "Move the sliders", "Browser maths checked by the backend"],
            ["AI assistant", "Ask three questions, open history", "How questions are understood and saved"],
            ["Notifications", "Mark one read, then mark all read", "Changing one row from the screen"],
            ["Profile", "Change your phone and save", "Editing your own data safely"],
            ["Admin dashboard", "Log in as admin@bankflow.com", "Different pages for different roles"],
            ["Loan management", "Approve the pending loan", "An action that changes data and notifies somebody"],
            ["AI monitoring", "Read the questions from your own chat", "How staff can watch a feature"],
        ],
        [3.6, 7.2, 6.4],
    )
    done(doc, "You have visited every screen once.")

    doc.add_heading("Lesson 26. Four easy changes you can make", level=1)
    one_line(doc, "Change one small thing at a time and watch the result.")
    needs(doc, "Thirty minutes. Change only one thing before looking at the result.")
    doc.add_paragraph(
        "Change 1. The colour of the whole website. Open frontend/src/theme.js and find the line "
        "that sets the main colour. Change the colour code and save."
    )
    base.add_code(doc, "main: \"#1b3a8f\",        // change this to main: \"#0f766e\", and save")
    see(doc, "Every button and highlight turns teal within a second, without restarting anything.")
    doc.add_paragraph(
        "Change 2. The demo balance. Open backend/banking/management/commands/seed_demo.py and "
        "find this line."
    )
    base.add_code(doc, "target_balance = 85450.0      # change this number and save")
    doc.add_paragraph("Then run the seed command again in the backend terminal and refresh the dashboard.")
    base.add_code(doc, "python manage.py seed_demo --flush")
    see(doc, "The dashboard balance becomes 100,000 rupees, and the assistant gives the same new number.")
    doc.add_paragraph(
        "Change 3. Teach the assistant a new phrase. Open backend/assistant/ai_service.py, find "
        "account_balance in the INTENT_KEYWORDS list, and add a phrase of your own to that list."
    )
    see(doc, "After saving, you can ask the assistant using your new phrase and it answers with your balance.")
    doc.add_paragraph(
        "Change 4. The dashboard greeting. Open frontend/src/pages/Dashboard.jsx, find the PageHeader "
        "title near the top, and change the wording."
    )
    base.add_code(doc, "title={`${greeting()}, ${firstName}`}      // change the words inside the braces")
    see(doc, "The dashboard heading shows your own wording after you save.")
    done(doc, "You have edited the theme, the data, the assistant and a page. Those are the four places "
              "most changes happen in a project like this.")
    problems(doc, "If something breaks, press Ctrl+Z in that file to undo, then save again.")

    doc.add_heading("Lesson 27. How a click becomes data", level=1)
    one_line(doc, "Follow one click from the button to the record and back.")
    needs(doc, "Ten minutes of reading.")
    doc.add_paragraph(
        "This is the most useful thing in the whole book. Read the ten steps below slowly. Once you "
        "can follow this path, you can build any feature."
    )
    base.add_code(
        doc,
        "1  You click View Transactions in the browser\n"
        "2  The website shows the Transactions page for the address /transactions\n"
        "3  That page asks the bank service for a list of transactions\n"
        "4  The connection file adds your login pass and sends the request\n"
        "5  Django matches the address /api/transactions/ to a view\n"
        "6  The view reads your filters and asks the database for matching rows\n"
        "7  The database returns the rows of your pretend account\n"
        "8  The serializer turns each row into simple text\n"
        "9  The text travels back and the page stores it in memory\n"
        "10 The table on your screen redraws with those rows",
    )
    doc.add_paragraph("Four sentences to remember:")
    steps(
        doc,
        [
            "The lobby is the website: pages, buttons and charts in your browser.",
            "The counter is the API: fixed addresses that accept questions and return answers.",
            "The staff are the backend: they check who you are and decide what to send.",
            "The record room is the database: it stores every customer, transaction and loan.",
        ],
    )
    done(doc, "You can explain this path to somebody else without reading it again.")

    doc.add_heading("Lesson 28. When something goes wrong", level=1)
    one_line(doc, "Fix the twenty messages beginners see most often.")
    needs(doc, "Keep this lesson open while you work.")
    base.add_table(
        doc,
        ["What you see", "What it means", "What to do"],
        [
            ["python is not recognized", "Python is not on the PATH", "Reinstall Python and tick Add python.exe to PATH"],
            ["pip is not recognized", "Your private box is switched off", "Run venv\\Scripts\\activate, then try again"],
            ["npm is not recognized", "Node.js is missing, or the terminal is old", "Reinstall Node.js LTS, then open a new terminal"],
            ["running scripts is disabled", "Windows blocks the activate line", "Run Set-ExecutionPolicy RemoteSigned -Scope CurrentUser, answer Yes, then activate again"],
            ["No module named django", "The box is off or libraries are missing", "Activate venv, then pip install -r requirements.txt"],
            ["manage.py not found", "The terminal is in the wrong folder", "Type cd backend and try again"],
            ["No such table", "The tables were never created", "Run python manage.py migrate, then seed_demo --flush"],
            ["Port 8000 is already in use", "The backend is already running", "Use the running one, or start it on 8001 and change the website setting"],
            ["EADDRINUSE port 5173", "The website is already running", "Use the window that is already open, or press Ctrl+C first"],
            ["Cannot find module", "A file name or folder is wrong", "Compare the capitals and the folder with this book"],
            ["The API cannot be reached", "The backend terminal stopped", "Start the backend again and refresh the page"],
            ["CORS policy error", "The backend does not allow your website address", "Check CORS_ALLOWED_ORIGINS in backend/.env includes http://localhost:5173"],
            ["401 Unauthorized", "Your login pass expired", "Log out and log in again"],
            ["Blank page with an error in the terminal", "The last file you edited has a mistake", "Open that file, compare it with this book, press Ctrl+Z to undo if unsure"],
            ["npm install stops with a blocked scripts warning", "The package manager blocked esbuild", "Run npm install-scripts approve esbuild, then npm install again"],
            ["The rupee sign looks strange", "Your code font is different", "Ignore it; the website itself is not affected"],
        ],
        [4.8, 5.2, 7.2],
    )
    doc.add_paragraph(
        "One habit solves most of these: read the first line of the message, look at the file name it "
        "mentions, and ask whether the terminal is in the right folder and whether the backend is "
        "still running."
    )
    done(doc, "You know where to look instead of starting over.")

    doc.add_heading("Lesson 29. Stop, start and start again", level=1)
    one_line(doc, "Keep the project easy to open on any day.")
    needs(doc, "Five minutes.")
    doc.add_paragraph(
        "To stop anything that is running, click inside that terminal and press the Ctrl and C keys "
        "together. Then start each side again with its own commands."
    )
    doc.add_paragraph().add_run("Start the backend in the first terminal:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000",
    )
    doc.add_paragraph().add_run("Start the website in the second terminal:").bold = True
    command(doc, "cd banking_app/frontend\nnpm run dev")
    doc.add_paragraph().add_run("If the pretend data ever looks wrong, reset it:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py seed_demo --flush",
    )
    see(doc, "The backend prints a line about watching for file changes, and the website prints a Local address.")
    done(doc, "You can start and stop the project without re-reading the book.")
    problems(doc, "Always activate the private box before backend commands. The terminal shows (venv) when it is on.")

    doc.add_heading("Lesson 30. What to learn next", level=1)
    one_line(doc, "Use your own project as the next textbook.")
    needs(doc, "No new tools. Just the project you built.")
    steps(
        doc,
        [
            "Change one screen at a time. Open the notifications page and add a filter for the type of message.",
            "Add one new field. Give the customer profile a nickname, then show it on the profile page.",
            "Add one new address. Build a monthly spending address and draw it as a new chart.",
            "Teach the assistant two more questions, reusing the maths that already exists in services.py.",
            "Learn Git so you can save versions of your work and try changes safely.",
            "Write a test for every new feature, copying the style of the tests you already have.",
            "Put the backend online with a hosting company and the website on a static host, then change the website setting to the new address.",
            "Read your own code. Every file in this book explains its decisions in comments.",
        ],
    )
    done(doc, "You have a working project, a habit of checking your work, and a list of next steps. "
              "That is what finishing your first full stack project looks like.")

    # ============================================================ appendices
    base.page_break(doc)
    doc.add_heading("Appendix A. Words explained simply", level=1)
    doc.add_paragraph("Keep this page near you. Every technical word in the book appears here in plain language.")
    base.add_table(
        doc,
        ["Word", "Plain meaning"],
        [
            ["Terminal", "The text panel where you type commands. It is at the bottom of VS Code."],
            ["Command", "One line you type and run by pressing Enter."],
            ["Folder and path", "A folder holds files. A path is the address of a file, such as backend/config/settings.py."],
            ["VS Code", "The free editor where you create files and run commands."],
            ["Extension", "An add on for VS Code that adds features."],
            ["Virtual environment", "A private box of Python libraries for one project. Ours is venv."],
            ["Library", "Ready made code written by other people."],
            ["pip", "The tool that downloads Python libraries."],
            ["npm", "The tool that downloads website libraries."],
            ["Node.js", "The program that runs the website building tools."],
            ["Django", "A ready made backend structure written in Python."],
            ["React", "The tool that builds the pages you see in the browser."],
            ["Vite", "The tool that runs the website while you work and packs it up at the end."],
            ["Component", "A reusable piece of a page, such as a card or a table."],
            ["Prop", "A value passed into a component so it can display something."],
            ["State", "Data a page keeps in memory while it is open."],
            ["Hook", "A React helper that lets a component remember things or run code at the right time."],
            ["API", "The counter: fixed web addresses your backend answers."],
            ["Endpoint", "One of those addresses, such as /api/dashboard/."],
            ["Request and response", "The question the website sends and the answer it gets back."],
            ["JSON", "A simple text format for data, understood by both sides."],
            ["Token", "A signed pass that proves you are logged in."],
            ["Model", "A description of one database table."],
            ["Migration", "An instruction that creates or changes database tables."],
            ["Serializer", "The code that turns a database row into text for the website."],
            ["View", "The code that answers one web address."],
            ["CORS", "The browser rule that decides which website may call your backend."],
            ["Seed data", "Pretend rows created by a command so the app has something to show."],
            ["Build", "Packing the website into final files for hosting."],
            ["localhost and port", "Your own computer, and the numbered channel such as 8000 or 5173."],
        ],
        [4.2, 13.0],
    )

    doc.add_heading("Appendix B. Every file and what it does", level=1)
    doc.add_paragraph(
        "Ninety-two files make up the project. The list below gives each one a purpose and its "
        "length. The files created by commands are explained after the table."
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
        "Created by commands, so you never paste them: db.sqlite3 comes from migrate, the migrations "
        "folders come from makemigrations, node_modules and package-lock.json come from npm install, "
        "and dist comes from npm run build. The two .env files are copies of the .env.example files."
    )

    doc.add_heading("Appendix C. Logins and the demo script", level=1)
    base.add_table(
        doc,
        ["Who", "Email", "Password", "What it shows"],
        [
            ["Customer", "mohammed@bankflow.com", "Demo@12345", "Balance 85,450, income 45,000, spending 18,450, two loans"],
            ["Customer", "aisha@bankflow.com", "Demo@12345", "Another customer with different loans"],
            ["Customer", "rahul@bankflow.com", "Demo@12345", "A third customer with a pending loan"],
            ["Bank employee", "admin@bankflow.com", "Admin@12345", "The employee pages and monitoring"],
        ],
        [3.0, 5.2, 3.0, 6.0],
    )
    doc.add_paragraph("Show the project in this order when somebody asks to see it.")
    steps(
        doc,
        [
            "The landing page, scrolled slowly.",
            "Log in as the customer and show the dashboard.",
            "Open the account page and point out the hidden account number.",
            "Filter the transactions, then open one.",
            "Apply for a loan and show the EMI changing as you type.",
            "Move the sliders in the EMI calculator.",
            "Ask the assistant five questions, then open the history.",
            "Mark a notification as read.",
            "Log in as the bank employee, approve the pending loan, then open analytics and AI monitoring.",
        ],
    )

    doc.add_heading("Appendix D. All the commands in one place", level=1)
    doc.add_paragraph(
        "Every command in this book, in the order you use them. Type one group at a time and wait "
        "for it to finish before typing the next group."
    )
    doc.add_paragraph().add_run("Once only, prepare the backend:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "python -m venv venv\n"
        "venv\\Scripts\\activate\n"
        "pip install Django==5.2.6 djangorestframework==3.16.1 djangorestframework-simplejwt==5.5.1 "
        "django-cors-headers==4.9.0 python-dotenv==1.1.1 \"psycopg[binary]==3.2.10\"\n"
        "copy .env.example .env\n"
        "python manage.py check",
    )
    doc.add_paragraph().add_run("Once only, build the pretend bank:").bold = True
    command(
        doc,
        "python manage.py makemigrations users banking assistant\n"
        "python manage.py migrate\n"
        "python manage.py seed_demo --flush\n"
        "python manage.py test",
    )
    doc.add_paragraph().add_run("Once only, prepare the website:").bold = True
    command(
        doc,
        "cd ..\n"
        "cd frontend\n"
        "npm create vite@latest . -- --template react\n"
        "npm install\n"
        "npm install @mui/material @mui/icons-material @emotion/react @emotion/styled\n"
        "npm install axios react-router-dom recharts react-icons\n"
        "copy .env.example .env",
    )
    doc.add_paragraph().add_run("Every day, start the backend in the first terminal:").bold = True
    command(
        doc,
        "cd banking_app/backend\n"
        "venv\\Scripts\\activate\n"
        "python manage.py runserver 127.0.0.1:8000",
    )
    doc.add_paragraph().add_run("Every day, start the website in the second terminal:").bold = True
    command(doc, "cd banking_app/frontend\nnpm run dev")
    doc.add_paragraph().add_run("Useful extras:").bold = True
    command(
        doc,
        "python manage.py seed_demo --flush      (reset the pretend data)\n"
        "python manage.py test                   (check the backend)\n"
        "npm run build                           (pack the website for hosting)",
    )
    doc.add_paragraph(
        "Press the Ctrl and C keys together in a terminal to stop whatever is running in it. On "
        "macOS or Linux, use source venv/bin/activate instead of the activate line, and cp instead "
        "of copy."
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
