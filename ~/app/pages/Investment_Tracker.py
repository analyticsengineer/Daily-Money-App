import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

# Notion setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
INVESTMENT_RETURN_DB_ID = os.getenv("NOTION_INVESTMENT_DB_ID")  # Use a specific variable for clarity

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Function to send data to Notion
def add_investment_tracker(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": INVESTMENT_RETURN_DB_ID},
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
            "Investment Return": {
                "number": data["investment_return"]
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

    # Debugging line
    if response.status_code not in [200, 201]:
        st.error(f"❌ Error {response.status_code}: {response.text}")

    return response.status_code in [200, 201]

# --- Streamlit App UI ---
st.set_page_config(page_title="Notion Money Tracker App", layout="centered")

# --- Investment Tracker Page ---
if page == "Investment Tracker":
    st.title("📈 Log Investment")

    with st.form("investment_tracker_form"):
        transaction = st.text_input("Transaction Name")
        date_value = st.date_input("Date", value=date.today())
        amount_str = st.text_input("Amount (use numbers only)", placeholder="e.g. 5,000")
        category = st.text_input("Category (enter manually)")
        investment_return_str = st.text_input("Investment Return (%)", placeholder="e.g. 5 or 5%")
        expense_type = st.selectbox("Type", ["Expense", "Income", "Investment", "Savings", "Transfer"])
        payment_method = st.text_input("Payment Method (enter manually)")
        note = st.text_area("Notes (optional)", height=80)
        submit = st.form_submit_button("Submit")

        if submit:
            try:
                amount = float(amount_str.replace(",", ""))
                investment_return = float(investment_return_str.replace("%", "").strip())

                data = {
                    "transaction": transaction,
                    "date": str(date_value),
                    "amount": amount,
                    "category": category,
                    "investment_return": investment_return,
                    "type": expense_type,
                    "payment_method": payment_method,
                    "note": note
                }

                success = add_investment_tracker(data)
                if success:
                    st.success("✅ Investment logged successfully!")
            except ValueError:
                st.error("❌ Invalid number format. Use numbers only (e.g., 5 or 5%).")
