# BankFlow – AI Banking Assistant

A complete, runnable **full-stack demo banking application**: React + Vite + Material UI on the
front end, Django + Django REST Framework + JWT on the back end, Recharts for analytics and a
modular AI banking assistant service.

> **This is a demonstration project.** Every customer, account, transaction, loan and notification
> is fictional. The app never moves real money, never contacts a real bank and must never be used
> with real credentials or financial data.

---

## Get the code on your computer

```bash
git clone https://github.com/Adnan8066/bankflow-ai-banking-assistant.git
cd bankflow-ai-banking-assistant
```

Then follow [Backend setup](#6-backend-setup) and [Frontend setup](#7-frontend-setup), or read the
step by step walkthroughs in `FULL_CODE.md`.

The repository is public. Change that any time in the repository **Settings**, under **General**,
**Danger zone**, **Change repository visibility**.

---

## 1. Project overview

BankFlow lets a customer register, log in, see a banking dashboard, explore transactions, apply for
demo loans, calculate EMIs, read notifications and chat with an AI assistant that answers questions
using **their own simulated banking data**. A second role - bank employee / admin - can manage
customers, transactions, loans, view analytics and monitor what customers ask the AI.

Everything works offline: if no external AI key is configured, a rule based intent engine answers
the questions instead.

---

## 2. Features

**Customer**

- Register, login, logout with JWT (access + refresh, automatic refresh on 401)
- Protected routes and role based access (customer vs bank employee)
- Dashboard: available balance, monthly income, monthly expenses, active loans
- Charts: income vs expense (6 months), spending by category, monthly transaction count, loan status
- Account page with masked account number, type, status, IFSC-style demo identifier
- Transactions: search, category filter, credit/debit filter, date range filter, sorting, pagination,
  running balance and a transaction details page
- Loans: list, status tabs, demo application form with live EMI preview, loan details with a
  12-instalment amortisation schedule and repayment progress
- EMI calculator: sliders + inputs, EMI, total interest, total repayment, principal vs interest chart,
  server-side verification through the Django API
- AI Banking Assistant: chat UI, chat history sidebar, suggested questions, intent-aware answers
- Notifications with read / unread state and "mark all as read"
- Profile: view and update name, phone, address, occupation, monthly income

**Bank employee / admin**

- Admin dashboard: customers, accounts, transactions, loans, pending loans, demo transaction volume
- Customer management with search and a customer 360 dialog (accounts, profile, loans)
- Transaction management across every customer with filters and pagination
- Loan management: approve / activate / reject a demo loan (creates a customer notification)
- Analytics dashboard: portfolio trend, category split, transaction count, active loan ratio
- AI assistant monitoring: total questions, intent breakdown, provider split, full question log

---

## 3. Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Vite 5, React Router 6, Material UI 5, Recharts, Axios, React Icons |
| Backend | Python, Django 5, Django REST Framework, SimpleJWT, django-cors-headers, python-dotenv |
| Database | SQLite (default, zero setup) or PostgreSQL (switch with `DB_ENGINE=postgres`) |
| AI | Modular service (`assistant/ai_service.py`) with rule based fallback and an optional LLM hook |
| Auth | JWT access/refresh tokens, `Authorization: Bearer <access>` |

---

## 4. Architecture

```
React (Vite, port 5173)
  └── axios api.js  ── JWT header + auto refresh
        │
        ▼
Django REST Framework (port 8000)
  ├── users/       custom User (email login, roles) + CustomerProfile
  ├── banking/     Account → Transaction, Loan, Notification + dashboard/analytics services
  └── assistant/   ChatMessage + ai_service (intent detection → data retrieval → answer)
        │
        ▼
SQLite / PostgreSQL (fictional demo data)
```

Request flow of an AI question:

1. React posts `{ "message": "How much did I spend this month?" }` to `/api/assistant/chat/`.
2. `ai_service.detect_intent()` maps the sentence to an intent (`expense_summary`).
3. `build_context(user)` retrieves the structured demo banking snapshot from the database.
4. Either the LLM layer (if `AI_PROVIDER=openai` and a key exists) or the rule based engine writes
   the answer from that snapshot - numbers are never invented.
5. The question and answer are stored in `ChatMessage` and returned to React with
   `{ response, type, data, provider }`.

---

## 5. Folder structure

```
banking_app/
├── README.md
├── FULL_CODE.md               # every source file, headline-wise, copy-paste ready
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/                settings.py, urls.py, wsgi.py, asgi.py
│   ├── users/                 models, serializers, views, permissions, signals, urls/
│   ├── banking/               models, serializers, views, admin_views, services,
│   │                          urls/, management/commands/seed_demo.py
│   └── assistant/             models, serializers, views, ai_service, urls
│
└── frontend/
    ├── index.html, package.json, vite.config.js, .env.example
    └── src/
        ├── main.jsx, App.jsx, theme.js, index.css
        ├── components/        AppLayout, Navbar, Sidebar, DashboardCard, TransactionTable,
        │                      LoanCard, ChatMessage, ProtectedRoute, Common
        ├── context/           AuthContext.jsx
        ├── services/          api.js, authService.js, bankingService.js, aiService.js, adminService.js
        ├── utils/             formatCurrency.js, calculations.js
        └── pages/             Landing, Login, Register, Dashboard, Account, Transactions,
                               TransactionDetails, Loans, LoanDetails, EMICalculator,
                               AIAssistant, Notifications, Profile, NotFound
            └── admin/         AdminDashboard, CustomerManagement, TransactionManagement,
                               LoanManagement, AdminAnalytics, AIMonitor
```

---

## 6. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
copy .env.example .env           # Windows   (cp on macOS / Linux)
python manage.py makemigrations users banking assistant
python manage.py migrate
python manage.py seed_demo --flush
python manage.py runserver 127.0.0.1:8000
```

API root: <http://127.0.0.1:8000/api/> · Django admin: <http://127.0.0.1:8000/admin/>

Run the tests (25 tests: auth, profile, banking, EMI, admin permissions, AI intents):

```bash
python manage.py test
```

---

## 7. Frontend setup

```bash
cd frontend
npm install
copy .env.example .env           # cp on macOS / Linux
npm run dev                      # http://localhost:5173
npm run build                    # production bundle in dist/
npm run preview                  # serve the production build
```

`frontend/.env`

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

---

## 8. Database setup

**SQLite (default, recommended for the demo)** - nothing to install, the file `backend/db.sqlite3`
is created by `migrate`.

**PostgreSQL (optional)** - create the database, then in `backend/.env`:

```
DB_ENGINE=postgres
POSTGRES_DB=bankflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Re-run `python manage.py migrate` and `python manage.py seed_demo --flush`.

---

## 9. Environment variables

`backend/.env`

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (change in production) |
| `DJANGO_DEBUG` | `True` locally, `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma separated host names |
| `CORS_ALLOWED_ORIGINS` | Allowed front-end origins (default `http://localhost:5173`) |
| `DB_ENGINE` | `sqlite` or `postgres` |
| `POSTGRES_*` | PostgreSQL connection details |
| `AI_PROVIDER` | `fallback` (rule based, default) or `openai` |
| `OPENAI_API_KEY` | Optional key - never hard-code it, never commit `.env` |
| `OPENAI_MODEL` | Model name used when `AI_PROVIDER=openai` |

`frontend/.env`

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | Base URL of the Django API |

---

## 10. API endpoints

All customer endpoints require the header `Authorization: Bearer <access_token>`.

**Authentication**

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/auth/register/` | Register a demo customer (creates an account automatically) |
| POST | `/api/auth/login/` | Login, returns `access` + `refresh` |
| POST | `/api/auth/refresh/` | Exchange a refresh token for a new access token |

**Customer**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET / PUT | `/api/profile/` | Read or update the customer profile (name, phone, address, occupation, income) |
| GET | `/api/dashboard/` | KPI cards + charts data in one call |
| GET | `/api/account/` | Masked account details |
| GET | `/api/transactions/` | List with `search`, `category`, `type`, `status`, `start_date`, `end_date`, `ordering`, `page` |
| GET | `/api/transactions/<id>/` | Single transaction detail |
| GET / POST | `/api/loans/` | List loans / submit a demo loan application |
| GET | `/api/loans/<id>/` | Loan detail |
| POST | `/api/emi/` | Server-side EMI calculation |
| GET | `/api/notifications/` | Notifications (`?unread=true` for unread only) |
| PUT | `/api/notifications/<id>/` | Mark read / unread |
| POST | `/api/notifications/read-all/` | Mark every notification as read |
| POST | `/api/assistant/chat/` | Ask BankFlow AI |
| GET / DELETE | `/api/assistant/history/` | Read or clear the saved chat history |
| GET | `/api/assistant/suggestions/` | Suggested question chips |

**Bank employee / admin (role `ADMIN` required)**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/admin/analytics/` | KPI totals + all admin charts |
| GET | `/api/admin/analytics/overview/` | The six KPI numbers only |
| GET | `/api/admin/customers/` | Customer table (`?search=`) |
| GET | `/api/admin/customers/<id>/` | Customer 360 view |
| GET | `/api/admin/transactions/` | All transactions with filters |
| GET | `/api/admin/loans/` | All loans with filters |
| PATCH | `/api/admin/loans/<id>/` | `{ "status": "APPROVED" }` etc. (notifies the customer) |
| GET | `/api/admin/users/` | User management table |
| GET | `/api/assistant/monitor/` | AI monitoring dashboard data |

**AI request / response example**

```json
POST /api/assistant/chat/
{ "message": "How much did I spend this month?" }

{
  "id": 12,
  "message": "How much did I spend this month?",
  "response": "You spent ₹18,450 this month. Your income for the month is ₹45,000, so your net savings are ₹26,550.",
  "type": "expense_summary",
  "intent": "expense_summary",
  "provider": "fallback",
  "data": { "amount": 18450.0, "income": 45000.0, "savings": 26550.0 }
}
```

---

## 11. How to run

Terminal 1

```bash
cd backend
venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```

Terminal 2

```bash
cd frontend
npm run dev
```

Open <http://localhost:5173>.

### Demo logins

| Role | Email | Password |
| --- | --- | --- |
| Customer (Mohammed Adnan, balance ₹85,450) | `mohammed@bankflow.com` | `Demo@12345` |
| Customer (Aisha Khan) | `aisha@bankflow.com` | `Demo@12345` |
| Customer (Rahul Verma) | `rahul@bankflow.com` | `Demo@12345` |
| Bank employee / admin | `admin@bankflow.com` | `Admin@12345` |

### 5-10 minute demo flow

1. Landing page - hero, features, AI preview, security, demo logins.
2. Login as `mohammed@bankflow.com`.
3. Dashboard - balance ₹85,450, income ₹45,000, expenses ₹18,450, 2 active loans, four charts.
4. Account page - masked account number and account status.
5. Transactions - filter by category, type, date; open a transaction detail.
6. Loans - status tabs, apply for a new demo loan (live EMI preview).
7. EMI calculator - move the sliders, see the Django API verification message.
8. AI Assistant - ask: *What is my balance?*, *How much did I spend this month?*,
   *What was my biggest expense?*, *What loans do I have?*, *What is EMI?* - and show the history panel.
9. Analytics + notifications.
10. Log out, log in as `admin@bankflow.com` - admin dashboard, customer 360, approve a pending loan,
    analytics and AI monitoring.
11. Explain the flow: React → axios/JWT → DRF views → services → ORM → SQLite → AI service.

---

## 12. Future improvements

- Real LLM integration with streaming responses and function/tool calling
- Budgets, goals and spend alerts; recurring transaction detection
- Statement export (CSV/PDF) and downloadable receipts
- Refresh-token blacklisting, 2FA and device management
- Celery + Redis for background jobs (EMI reminders, monthly summaries)
- WebSocket notifications instead of polling
- Docker Compose for one-command startup, plus CI with GitHub Actions
- End-to-end tests with Playwright and API schema docs with drf-spectacular
