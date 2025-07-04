import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2025-07-04"
}

# Database IDs
DAILY_EXPENSES_DB_ID = os.getenv("NOTION_DATABASE_ID")


def add_daily_expense(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DAILY_EXPENSES_DB_ID},
        "properties": {
            "Transaction": {
                "title": [{"text": {"content": data["transaction"]}}]
            },
            "Date": {
                "date": {"start": data["date"]}
            },
            "Amount": {
                "number": data["amount"]
            },
            "Category": {
                "select": {"name": data["category"]}
            },
            "Type": {
                "select": {"name": data["type"]}
            },
            "Payment Method": {
                "select": {"name": data["payment_method"]}
            },
            "Note": {
                "rich_text": [{"text": {"content": data["note"]}}]
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code in [200, 201]


# --- Streamlit UI ---

st.set_page_config(page_title="Notion Money Tracker App", layout="centered")

st.sidebar.title("📊 Notion Money Tracker App")
page = st.sidebar.radio("Select a page", ["Daily Expenses", "Monthly Overview", "Investment Tracker"])

if page == "Daily Expenses":
    st.title("🧾 Log Daily Expenses")

    with st.form("daily_expense_form"):
        transaction = st.text_input("Transaction Name")
        date_value = st.date_input("Date", value=date.today())
        amount_str = st.text_input("Amount (use numbers only)", placeholder="e.g. 5,000")
        category = st.text_input("Category (enter manually)")
        expense_type = st.selectbox("Type", ["Expense", "Income", "Investment", "Savings", "Transfer"])
        payment_method = st.text_input("Payment Method (enter manually)")
        note = st.text_area("Note (optional)", height=80)
        submit = st.form_submit_button("Submit")

        if submit:
            try:
                amount = float(amount_str.replace(",", ""))
                data = {
                    "transaction": transaction,
                    "date": str(date_value),
                    "amount": amount,
                    "category": category,
                    "type": expense_type,
                    "payment_method": payment_method,
                    "note": note
                }
                success = add_daily_expense(data)
                if success:
                    st.success("✅ Expense added successfully!")
                else:
                    st.error("❌ Failed to add expense to Notion.")
            except ValueError:
                st.error("❌ Invalid amount format. Use numbers only.")
