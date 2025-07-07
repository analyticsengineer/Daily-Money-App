import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

# Notion setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DAILY_DB_ID = os.getenv("NOTION_DAILY_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Function to send data to Notion
def add_daily_expenses(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_DAILY_DB_ID},
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
            "Notes": {
                "rich_text": [{"text": {"content": data["note"]}}]
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code not in [200, 201]:
        st.error(f"❌ Error {response.status_code}: {response.text}")
    return response.status_code in [200, 201]

# --- Page UI ---
st.set_page_config(page_title="💹 Daily Money", layout="centered")
st.title("📈 Log Daily Money")

# Initialize session state only once
for key, default in {
    "transaction": "",
    "amount_str": "",
    "category": "",
    "expense_type": "Expense",
    "payment_method": "",
    "note": ""
}.items():
    st.session_state.setdefault(key, default)

# Form
with st.form("daily_money_tracker_form"):
    st.text_input("Transaction Name", key="transaction")
    date_value = st.date_input("Date", value=date.today())
    st.text_input("Amount (use numbers only)", placeholder="e.g. 5,000", key="amount_str")
    st.text_input("Category (enter manually)", key="category")
    st.selectbox("Type", ["Expense", "Income", "Investment", "Savings", "Transfer"], key="expense_type")
    st.text_input("Payment Method (enter manually)", key="payment_method")
    st.text_area("Notes (optional)", height=80, key="note")
    submit = st.form_submit_button("Submit")

    if submit:
        try:
            amount = float(st.session_state.amount_str.replace(",", ""))

            data = {
                "transaction": st.session_state.transaction,
                "date": str(date_value),
                "amount": amount,
                "category": st.session_state.category,
                "type": st.session_state.expense_type,
                "payment_method": st.session_state.payment_method,
                "note": st.session_state.note
            }

            success = add_daily_expenses(data)
            if success:
                st.success("✅ Daily Money logged successfully!")

                # Reset form values
                for field in ["transaction", "amount_str", "category", "payment_method", "note"]:
                    st.session_state[field] = ""
        except ValueError:
            st.error("❌ Invalid number format. Use numbers only (e.g., 5 or 5%).")
