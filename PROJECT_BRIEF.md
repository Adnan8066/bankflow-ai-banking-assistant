# BankFlow - AI Banking Assistant

## What it is

BankFlow is a complete, working banking application built as a portfolio and learning project. A
customer can register, log in, see a dashboard, explore transactions, apply for a demo loan,
calculate an EMI and chat with an AI assistant that answers questions about their own account. A
second role, bank employee, can manage customers, review loans, read analytics and monitor what
customers ask the assistant.

Every account, transaction, loan and notification is fictional. The application never moves money
and holds no real banking data, so it is safe to demonstrate to anyone.

## Who it is for

It is written for three audiences at once. A student or job seeker can show it as proof of full
stack skills. A team can use it as a reference for how a React and Django project fits together.
A beginner can follow the step by step guides in this repository and build the same application
from an empty laptop.

## What it does

Customer side

- Registration, login and logout with JWT access and refresh tokens, refreshed automatically when they expire
- Dashboard with available balance, monthly income, monthly expenses, savings rate, active loans and five charts
- Account page that shows the account number with the middle digits masked
- Transactions with search, category, type and date filters, sorting, pagination, CSV export and a detail page
- Loans with status tabs, a demo application form that previews the EMI as you type, and a repayment schedule
- EMI calculator with sliders, a principal versus interest chart, and server side verification of the result
- AI assistant that understands natural questions, answers from the customer's own data and saves the history
- Notifications with read and unread state
- Profile editing and password change
- Light and dark mode that follows the user's choice on every screen

Bank employee side

- Portfolio dashboard: customers, accounts, transactions, loans, pending loans and demo transaction volume
- Customer management with search and a customer 360 view
- Transaction management across every customer with the same filters
- Loan management with approve, activate and reject actions that notify the customer
- Analytics with income and expense trends, category split, transaction counts and the active loan ratio
- AI monitoring with the question log, intent breakdown and answer provider

## Technology

| Layer | Choice |
| --- | --- |
| Frontend | React 18, Vite 5, React Router 6, Material UI 5, Recharts, Axios |
| Backend | Python, Django 5, Django REST Framework, SimpleJWT, django-cors-headers |
| Database | SQLite for development, PostgreSQL by changing one environment variable |
| Authentication | JWT access and refresh tokens, role based permissions |
| AI | A modular service with deterministic rule based answers and an optional external model |
| Quality | 32 Django tests, a GitHub Actions workflow, a Vite production build check |

## How it is put together

```
React pages  ->  Axios service layer  ->  Django URLs  ->  Views  ->  Services  ->  Models  ->  Database
     ^                                                                                              |
     +---------------------------- JSON response, rendered as cards, tables and charts --------------+
```

The front end never talks to the database. It calls fixed API addresses, the backend decides what
the signed in user is allowed to see, and one service layer holds every calculation so the
dashboard, the charts, the EMI calculator and the AI assistant always agree with each other.

The AI assistant follows the same discipline. It first detects the intent of the question, then
retrieves the real demo numbers, and only then writes a sentence. If no external model is
configured, the built in answers reply instead, so the feature always works offline.

## Try it

| Role | Email | Password |
| --- | --- | --- |
| Customer | `mohammed@bankflow.com` | `Demo@12345` |
| Bank employee | `admin@bankflow.com` | `Admin@12345` |

The demo customer has a balance of 85,450 rupees, a monthly income of 45,000, monthly spending of
18,450 and two active loans, so every screen has something meaningful to show.

Run the backend on `http://127.0.0.1:8000` and the website on `http://localhost:5173`; the README
has the exact commands for both.

## What makes it worth looking at

- The money maths lives in one file, so no two screens can disagree
- Roles are enforced in the interface and again in the API, not just hidden in the menu
- The assistant cannot invent a balance, because the numbers are retrieved before the sentence is written
- Demo numbers are chosen to match the demo script exactly, so a live demonstration never surprises you
- Dark mode, CSV export, password change and the daily spending insight were added after the first
  version, showing how the project keeps growing

## Where it could go next

Streaming answers with tool calling, budgets and spend alerts, statement export to PDF, refresh
token rotation with blacklisting, two factor authentication, Celery and Redis for scheduled
summaries, WebSocket notifications, and a hosted deployment with Docker Compose.
