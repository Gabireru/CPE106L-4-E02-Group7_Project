import streamlit as st

st.set_page_config(page_title="Discounts", page_icon="💰", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("login")

st.markdown("<h1 style='text-align: center;'>💰 Discounts Page</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>This page will display available discounts soon.</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("pages/home")

with col2:
    if st.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()
