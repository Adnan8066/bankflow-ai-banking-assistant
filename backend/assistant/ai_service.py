"""BankFlow AI service.

Design goals
------------
1. `answer(user, message)` is the single entry point used by the view.
2. Intent detection + data retrieval are completely independent from the
   language model, so the demo always works offline (rule based fallback).
3. If `AI_PROVIDER=openai` and an API key is present, the *same* retrieved
   banking context is sent to the LLM so the wording becomes natural while the
   numbers stay grounded in the database.
"""
import json
import re

from django.conf import settings

from banking.services import (
    big_category_names,
    category_total,
    customer_transactions,
    format_inr,
    get_dashboard,
    to_float,
)
from banking.models import Account, Loan

BANKING_KNOWLEDGE = {
    "emi": (
        "EMI stands for Equated Monthly Instalment. It is the fixed amount you pay "
        "every month towards a loan; each instalment contains a principal part and an "
        "interest part. A higher tenure lowers the EMI but increases the total interest."
    ),
    "kyc": (
        "KYC (Know Your Customer) is the identity verification process banks must follow. "
        "It usually needs a photo ID, address proof and a recent photograph. KYC keeps "
        "accounts compliant and protects customers from fraud."
    ),
    "savings account": (
        "A savings account is a deposit account for everyday money. It earns interest, "
        "allows withdrawals and is meant for personal use rather than business transactions."
    ),
    "credit score": (
        "A credit score is a three digit number (typically 300-900 in India) that estimates "
        "how reliably you repay debt. It is built from repayment history, credit utilisation, "
        "credit age, loan mix and new enquiries."
    ),
    "cibil": (
        "CIBIL is one of India's credit bureaus. It publishes your credit score, which banks "
        "review before approving loans or credit cards. Scores above 750 are usually preferred."
    ),
    "fixed deposit": (
        "A fixed deposit (FD) locks a lump sum with the bank for a fixed period at a fixed "
        "interest rate. It usually earns more than a savings account and is low risk."
    ),
    "interest rate": (
        "An interest rate is the percentage a bank pays you on deposits or charges you on a "
        "loan. Loans usually use reducing-balance interest, so interest is charged on the "
        "outstanding amount."
    ),
    "upi": (
        "UPI (Unified Payments Interface) is an instant bank-to-bank payment system in India. "
        "This demo app does not move real money - transfers shown here are simulated."
    ),
    "neft": (
        "NEFT is a bank transfer system that settles transactions in batches. It is commonly "
        "used for larger transfers between accounts in India."
    ),
    "rtgs": (
        "RTGS is the Real Time Gross Settlement system used for high value transfers that "
        "settle instantly, transfer by transfer."
    ),
    "compound interest": (
        "Compound interest is interest calculated on both the original amount and the interest "
        "already earned, so money grows faster over long periods."
    ),
}

INTENT_KEYWORDS = {
    "account_balance": ["balance", "how much money", "account balance", "available amount"],
    "account_details": ["account details", "account number", "my account", "ifsc", "account info",
                        "account type"],
    "recent_transactions": ["transaction", "transactions", "recent activity", "statement",
                            "last payment", "history"],
    "expense_summary": ["spend", "spent", "expense", "expenses", "how much did i spend",
                        "total spending"],
    "biggest_expense": ["biggest expense", "largest expense", "highest expense", "most spent",
                        "biggest spend"],
    "category_spend": ["spend on", "spent on", "expenses on", "category", "categories"],
    "loan_list": ["what loans", "my loans", "do i have", "loan do i", "loans do i"],
    "loan_emi": ["what is my emi", "my emi", "emi amount", "monthly instalment", "monthly installment"],
    "loan_remaining": ["remaining", "outstanding", "left to pay", "how much loan amount"],
    "compare_months": ["compare", "last month", "previous month", "versus", "than last"],
    "category_breakdown": ["spending categories", "category breakdown", "where does my money go",
                           "breakdown of my spending"],
    "financial_summary": ["summary", "give me a summary", "overview", "how am i doing",
                          "financial health"],
    "banking_knowledge": list(BANKING_KNOWLEDGE.keys()) + ["what is", "explain", "define"],
    "loan_info": ["loan", "loans", "borrow", "eligibility"],
    "emi_calculator": ["calculate emi", "emi calculator", "emi for"],
    "greeting": ["hello", "hi ", "hey", "good morning", "good evening"],
    "help": ["what can you do", "help", "who are you", "your name"],
}


def normalise(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def detect_intent(message):
    """Score each intent by keyword overlaps - deterministic and explainable."""
    text = normalise(message)
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += len(keyword.split()) * 2 + 1
        if score:
            scores[intent] = score
    if not scores:
        return "unknown"

    # A few tie-breakers so common demo questions land on the right intent.
    if "balance" in text:
        return "account_balance"
    if "emi" in text:
        if any(word in text for word in ["my emi", "emi amount", "emi per month",
                                         "emi do i", "emi i pay", "calculate emi"]):
            return "loan_emi"
        if any(word in text for word in ["what is", "explain", "define", "mean",
                                         "stand for"]):
            return "banking_knowledge"
    if any(word in text for word in ["spend", "spent", "expense", "expenses"]) and any(
        category.lower() in text for category in big_category_names()
    ):
        return "category_spend"
    if "loan" in text and any(word in text for word in ["what loans", "my loans", "list"]):
        return "loan_list"
    return max(scores, key=scores.get)


# --------------------------------------------------------------------- data --
def build_context(user):
    """Structured snapshot of the customer data the assistant is allowed to see."""
    dashboard = get_dashboard(user)
    account = Account.objects.filter(user=user).first()
    loans = Loan.objects.filter(user=user)
    return {
        "customer_name": user.name,
        "balance": dashboard["balance"],
        "monthly_income": dashboard["monthly_income"],
        "monthly_expenses": dashboard["monthly_expenses"],
        "previous_month_expenses": dashboard["previous_month_expenses"],
        "monthly_savings": dashboard["monthly_savings"],
        "top_category": dashboard["top_category"],
        "spending_categories": dashboard["spending_categories"],
        "monthly_trend": dashboard["monthly_trend"],
        "active_loans": dashboard["active_loans"],
        "monthly_emi_total": dashboard["monthly_emi_total"],
        "total_outstanding": dashboard["total_outstanding"],
        "account": {
            "number": account.masked_account_number if account else None,
            "type": account.get_account_type_display() if account else None,
            "status": account.get_status_display() if account else None,
            "ifsc": account.ifsc_code if account else None,
            "branch": account.branch if account else None,
        },
        "loans": [
            {
                "loan_id": loan.loan_id,
                "type": loan.get_loan_type_display(),
                "amount": to_float(loan.amount),
                "emi": to_float(loan.emi),
                "remaining": to_float(loan.remaining_amount),
                "status": loan.get_status_display(),
                "interest_rate": to_float(loan.interest_rate),
                "tenure_months": loan.tenure_months,
            }
            for loan in loans
        ],
        "recent_transactions": [
            {
                "date": t.date.strftime("%d %b %Y"),
                "description": t.description,
                "category": t.category,
                "type": t.transaction_type,
                "amount": to_float(t.amount),
            }
            for t in customer_transactions(user)[:5]
        ],
    }


# ----------------------------------------------------------- rule responses --
def _balance_answer(context):
    return {
        "response": (
            f"Your current available balance is ₹{format_inr(context['balance'])}."
        ),
        "type": "account_balance",
        "data": {"amount": context["balance"]},
    }


def _account_details(context):
    account = context["account"]
    if not account["number"]:
        return _no_account()
    return {
        "response": (
            f"Here are your demo account details:\n"
            f"• Account number: {account['number']}\n"
            f"• Type: {account['type']}\n"
            f"• Status: {account['status']}\n"
            f"• IFSC: {account['ifsc']}\n"
            f"• Branch: {account['branch']}\n"
            f"• Available balance: ₹{format_inr(context['balance'])}"
        ),
        "type": "account_details",
        "data": account,
    }


def _expense_summary(context):
    return {
        "response": (
            f"You spent ₹{format_inr(context['monthly_expenses'])} this month. "
            f"Your income for the month is ₹{format_inr(context['monthly_income'])}, "
            f"so your net savings are ₹{format_inr(context['monthly_savings'])}."
        ),
        "type": "expense_summary",
        "data": {
            "amount": context["monthly_expenses"],
            "income": context["monthly_income"],
            "savings": context["monthly_savings"],
        },
    }


def _biggest_expense(context):
    top = context["top_category"]
    if not top:
        return {
            "response": "You have no debit transactions recorded this month yet.",
            "type": "biggest_expense",
            "data": None,
        }
    return {
        "response": (
            f"Your largest expense category this month was {top['category']} at "
            f"₹{format_inr(top['amount'])}."
        ),
        "type": "biggest_expense",
        "data": top,
    }


def _category_spend(user, message, context):
    text = normalise(message)
    matches = []
    for item in context["spending_categories"]:
        if item["category"].lower() in text:
            matches.append(item)
    for name in big_category_names():
        if name.lower() in text and not any(m["category"] == name for m in matches):
            amount = category_total(user, [name])
            if amount:
                matches.append({"category": name, "amount": amount})

    if not matches:
        return _category_breakdown(context)
    lines = ", ".join(f"{m['category']} ₹{format_inr(m['amount'])}" for m in matches)
    return {
        "response": f"Here is what you spent on this month: {lines}.",
        "type": "category_spend",
        "data": matches,
    }


def _category_breakdown(context):
    categories = context["spending_categories"]
    if not categories:
        return _empty_month()
    lines = "\n".join(
        f"• {item['category']}: ₹{format_inr(item['amount'])}" for item in categories
    )
    return {
        "response": (
            f"Your spending categories for this month are:\n{lines}\n"
            f"Total: ₹{format_inr(context['monthly_expenses'])}"
        ),
        "type": "category_breakdown",
        "data": categories,
    }


def _recent_transactions(context):
    rows = context["recent_transactions"]
    if not rows:
        return {
            "response": "You have no transactions yet in this demo account.",
            "type": "recent_transactions",
            "data": [],
        }
    lines = "\n".join(
        f"• {row['date']} - {row['description']} "
        f"({'credit' if row['type'] == 'CREDIT' else 'debit'} "
        f"₹{format_inr(row['amount'])})"
        for row in rows
    )
    return {
        "response": f"Here are your latest 5 demo transactions:\n{lines}",
        "type": "recent_transactions",
        "data": rows,
    }


def _loan_list(context):
    loans = context["loans"]
    if not loans:
        return {
            "response": "You do not have any demo loans on record right now.",
            "type": "loan_list",
            "data": [],
        }
    lines = "\n".join(
        f"• {loan['type']} {loan['loan_id']} - ₹{format_inr(loan['amount'])} at "
        f"{loan['interest_rate']}% ({loan['status']})"
        for loan in loans
    )
    active = sum(1 for loan in loans if loan["status"] in ("Active", "Approved"))
    if active == len(loans):
        headline = (
            f"You currently have {active} active demo loan"
            f"{'' if active == 1 else 's'}"
        )
    else:
        headline = (
            f"You currently have {len(loans)} demo loan"
            f"{'' if len(loans) == 1 else 's'}, of which {active} "
            f"{'is' if active == 1 else 'are'} active or approved"
        )
    return {
        "response": f"{headline}:\n{lines}",
        "type": "loan_list",
        "data": loans,
    }


def _loan_emi(context):
    loans = [loan for loan in context["loans"] if loan["status"] in ("Active", "Approved")]
    if not loans:
        return {
            "response": (
                "You have no active demo loans, so there is no EMI to pay right now. "
                "You can estimate an EMI on a new loan using the EMI calculator."
            ),
            "type": "loan_emi",
            "data": [],
        }
    lines = "\n".join(
        f"• {loan['type']} ({loan['loan_id']}): ₹{format_inr(loan['emi'])} per month"
        for loan in loans
    )
    return {
        "response": (
            f"Your total monthly EMI is ₹{format_inr(context['monthly_emi_total'])}:\n{lines}"
        ),
        "type": "loan_emi",
        "data": loans,
    }


def _loan_remaining(context):
    loans = [loan for loan in context["loans"] if loan["remaining"] > 0]
    if not loans:
        return {
            "response": "You have no outstanding demo loan amount. Everything is repaid.",
            "type": "loan_remaining",
            "data": None,
        }
    lines = "\n".join(
        f"• {loan['type']} ({loan['loan_id']}): ₹{format_inr(loan['remaining'])} remaining"
        for loan in loans
    )
    return {
        "response": (
            f"Your total remaining demo loan amount is "
            f"₹{format_inr(context['total_outstanding'])}:\n{lines}"
        ),
        "type": "loan_remaining",
        "data": loans,
    }


def _compare_months(context):
    current = context["monthly_expenses"]
    previous = context["previous_month_expenses"]
    if previous == 0:
        return {
            "response": (
                f"You spent ₹{format_inr(current)} this month. There is no spending history "
                "for last month in this demo account yet."
            ),
            "type": "compare_months",
            "data": {"current": current, "previous": previous},
        }
    difference = current - previous
    direction = "more" if difference > 0 else "less"
    percent = abs(difference) / previous * 100
    return {
        "response": (
            f"This month you spent ₹{format_inr(current)} compared with "
            f"₹{format_inr(previous)} last month - that is ₹{format_inr(abs(difference))} "
            f"({percent:.1f}%) {direction}."
        ),
        "type": "compare_months",
        "data": {"current": current, "previous": previous,
                 "difference": round(difference, 2)},
    }


def _financial_summary(context):
    top = context["top_category"]
    top_line = (
        f"Your biggest category was {top['category']} (₹{format_inr(top['amount'])})."
        if top else "You have no debit transactions this month yet."
    )
    return {
        "response": (
            f"Here is your financial summary, {context['customer_name'].split()[0]}:\n"
            f"• Available balance: ₹{format_inr(context['balance'])}\n"
            f"• Income this month: ₹{format_inr(context['monthly_income'])}\n"
            f"• Expenses this month: ₹{format_inr(context['monthly_expenses'])}\n"
            f"• Net savings: ₹{format_inr(context['monthly_savings'])}\n"
            f"• Active loans: {context['active_loans']} with a monthly EMI of "
            f"₹{format_inr(context['monthly_emi_total'])}\n"
            f"{top_line}"
        ),
        "type": "financial_summary",
        "data": context,
    }


def _knowledge(message):
    text = normalise(message)
    for key, explanation in BANKING_KNOWLEDGE.items():
        if key in text:
            return {
                "response": explanation,
                "type": "banking_knowledge",
                "data": {"topic": key},
            }
    return {
        "response": (
            "I can explain banking basics such as EMI, KYC, savings accounts, credit "
            "scores, fixed deposits, interest rates, UPI, NEFT and RTGS. Ask me about any "
            "of those, or ask about your own demo balance, spending or loans."
        ),
        "type": "banking_knowledge",
        "data": None,
    }


def _help(context):
    return {
        "response": (
            f"Hi {context['customer_name'].split()[0]}, I am BankFlow AI. I can help you with:\n"
            "• Balance and account details\n"
            "• Recent transactions\n"
            "• This month's spending, biggest expense and spending categories\n"
            "• Your loans, EMI and outstanding amount\n"
            "• Banking concepts like EMI, KYC and credit score\n"
            "Try: “How much did I spend on food?”"
        ),
        "type": "help",
        "data": None,
    }


def _greeting(context):
    return {
        "response": (
            f"Hello {context['customer_name'].split()[0]}! I am BankFlow AI, your demo "
            "banking assistant. Ask me about your balance, spending, loans or any banking term."
        ),
        "type": "greeting",
        "data": None,
    }


def _no_account():
    return {
        "response": "I could not find a demo account linked to your profile yet.",
        "type": "error",
        "data": None,
    }


def _empty_month():
    return {
        "response": "You have no debit transactions recorded this month, so there is nothing to break down.",
        "type": "category_breakdown",
        "data": [],
    }


def _unknown(context):
    return {
        "response": (
            "I could not map that question to your demo banking data. Try asking about your "
            "balance, this month's spending, your biggest expense, your loans, your EMI, or a "
            "banking term such as “What is KYC?”"
        ),
        "type": "unknown",
        "data": None,
    }


RULE_ANSWERS = {
    "account_balance": _balance_answer,
    "account_details": _account_details,
    "expense_summary": _expense_summary,
    "biggest_expense": _biggest_expense,
    "category_breakdown": _category_breakdown,
    "recent_transactions": _recent_transactions,
    "loan_list": _loan_list,
    "loan_emi": _loan_emi,
    "loan_remaining": _loan_remaining,
    "compare_months": _compare_months,
    "financial_summary": _financial_summary,
    "help": _help,
    "greeting": _greeting,
}


def rule_based_answer(user, message, context, intent):
    """Deterministic, offline, always-available answers."""
    if intent == "category_spend":
        return _category_spend(user, message, context)
    if intent == "banking_knowledge":
        return _knowledge(message)
    if intent in ("loan_info", "emi_calculator"):
        if "emi" in normalise(message) and "loan" not in normalise(message):
            return _knowledge("emi")
        return _loan_list(context)
    handler = RULE_ANSWERS.get(intent)
    if handler:
        return handler(context)
    return _unknown(context)


# ------------------------------------------------------------------ LLM hook --
def llm_answer(user, message, context, intent):
    """Optional natural-language layer.

    Kept deliberately small: the prompt is grounded with the retrieved demo data
    so an external model can never invent balances. If anything fails we silently
    return None and the caller falls back to the rule based answer.
    """
    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key or getattr(settings, "AI_PROVIDER", "fallback") != "openai":
        return None
    try:
        import urllib.request

        payload = {
            "model": getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are BankFlow AI, a demo banking assistant. Answer only using the "
                        "JSON customer data provided. Use Indian rupee formatting. Never invent "
                        "numbers and never mention real banking actions.\n\n"
                        f"Customer data:\n{json.dumps(context, default=str)}"
                    ),
                },
                {"role": "user", "content": message},
            ],
            "temperature": 0.2,
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode())
        text = body["choices"][0]["message"]["content"].strip()
        return {"response": text, "type": intent, "data": None}
    except Exception:  # noqa: BLE001 - the demo must never break because of the API
        return None


def answer(user, message):
    """Main entry point used by POST /api/assistant/chat/."""
    context = build_context(user)
    intent = detect_intent(message)
    result = llm_answer(user, message, context, intent)
    provider = "openai" if result else "fallback"
    if result is None:
        result = rule_based_answer(user, message, context, intent)
    result["provider"] = provider
    result["intent"] = intent
    return result


def suggested_questions():
    return [
        "What is my current balance?",
        "How much did I spend this month?",
        "What was my biggest expense?",
        "How much did I spend on food?",
        "Show my recent transactions",
        "What loans do I have?",
        "What is my EMI?",
        "How much loan amount is remaining?",
        "Compare this month with last month",
        "Show my spending categories",
        "Give me a summary of my spending",
        "Explain EMI",
        "What is KYC?",
        "What is a credit score?",
    ]
