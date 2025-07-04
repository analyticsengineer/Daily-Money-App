import streamlit as st
from PIL import Image

# Optional: Load a custom image/logo
# image = Image.open("logo.png")
# st.image(image, width=120)

# Set page config
st.set_page_config(page_title="My Money Tracker", page_icon="💸", layout="centered")

# Title and intro
st.title("💸 My Personal Money Tracker")
st.markdown("#### Built for simplicity. Backed by clarity.")

st.markdown(
    """
Welcome to your personal finance hub, where money meets intention.  
Track your daily expenses, monitor your monthly performance, and review your investments — all in one place.

**What You’ll Find Here:**
- 📆 **Daily Expenses**: Log and review where your money goes, day by day.
- 📊 **Monthly Overview**: Compare income vs expenses and check your monthly budget health.
- 📈 **Investment Tracker**: Stay on top of returns and performance percentages.

---

###  Money Care:
- Keep your entries consistent — you’ll thank yourself later.
- Use the sidebar to navigate between pages.
- All data is securely stored in your Notion workspace.

Let’s take control of your money story.
"""
)

if st.button("🚀 Start Tracking Now"):
    st.switch_page("pages/Daily-Expenses.py")
