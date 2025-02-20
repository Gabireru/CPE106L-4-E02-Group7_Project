import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("login")

def logout():
    st.session_state["logged_in"] = False
    st.rerun()

st.markdown("<h1 style='text-align: center;'>🏠 Home Page</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Welcome! Choose an option below.</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("✏️ Edit Account Details"):
        st.warning("⚠️ This feature will be implemented soon.")

with col2:
    if st.button("📜 Menu"):
        st.switch_page("pages/menu")

with col3:
    if st.button("💰 Discounts"):
        st.switch_page("pages/discount")

st.markdown("<hr>", unsafe_allow_html=True)
if st.button("🚪 Logout"):
    logout()
