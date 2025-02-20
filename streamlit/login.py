import streamlit as st
import os

st.set_page_config(page_title="Admin Login", page_icon="🔑", layout="centered")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

USER_DB_FILE = "users.txt"

def init_db():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "w") as file:
            file.write("admin,password123\n")

def check_user(username, password):
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as file:
            users = file.readlines()
            for user in users:
                try:
                    stored_username, stored_password = user.strip().split(",")
                    if username == stored_username and password == stored_password:
                        return True
                except ValueError:
                    continue
    return False

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def logout():
    st.session_state["logged_in"] = False
    st.rerun()

init_db()

if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔒 Admin Login</h2>", unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login")

    if submit:
        if check_user(username, password):
            st.session_state["logged_in"] = True
            st.success("✅ Logged in successfully! Redirecting...")
            st.switch_page("pages/home")
        else:
            st.error("❌ Invalid Username or Password")

if st.session_state["logged_in"]:
    st.switch_page("pages/home")
