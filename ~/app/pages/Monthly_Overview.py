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

# Database ID for Monthly Overview
MONTHLY_OVERVIEW_DB_ID = os.getenv("NOTION_DATABASE_ID")

# Function to add monthly overview data
def add_monthly_overview(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": MONTHLY_OVERVIEW_DB_ID},
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
            "Monthly_budget": {  # Ensure this field name matches Notion exactly
                "number": data["monthly_budget"]
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

# --- Monthly Overview Page ---
if page == "Monthly Overview":
    st.title("🧾 Log Monthly Savings / Overview")

    with st.form("monthly_overview_form"):
        transaction = st.text_input("Transaction Name")
        date_value = st.date_input("Date", value=date.today())
        amount_str = st.text_input("Amount (use numbers only)", placeholder="e.g. 5,000")
        category = st.text_input("Category (enter manually)")
        monthly_budget_str = st.text_input("Monthly Budget (use numbers only)", placeholder="e.g. 2,000")
        expense_type = st.selectbox("Type", ["Expense", "Income", "Investment", "Savings", "Transfer"])
        payment_method = st.text_input("Payment Method (enter manually)")
        note = st.text_area("Note (optional)", height=80)
        submit = st.form_submit_button("Submit")

        if submit:
            try:
                amount = float(amount_str.replace(",", ""))
                monthly_budget = float(monthly_budget_str.replace(",", ""))
                data = {
                    "transaction": transaction,
                    "date": str(date_value),
                    "amount": amount,
                    "category": category,
                    "monthly_budget": monthly_budget,
                    "type": expense_type,
                    "payment_method": payment_method,
                    "note": note
                }
                success = add_monthly_overview(data)
                if success:
                    st.success("✅ Monthly overview logged successfully!")
                else:
                    st.error("❌ Failed to log data in Notion.")
            except ValueError:
                st.error("❌ Invalid amount format. Use numbers only.")

# --- Investment Tracker Page ---
elif page == "Investment Tracker":
    st.title("💳 Investment Tracker")
    if st.button("🚀 Start Tracking Now"):
        st.switch_page("pages/Investment-Tracker.py")

# --- Daily Expenses Page ---
elif page == "Daily Expenses":
    st.title("💸 Daily Expenses")
    if st.button("🚀 Start Logging Now"):
        st.switch_page("pages/Daily-Expenses.py")
