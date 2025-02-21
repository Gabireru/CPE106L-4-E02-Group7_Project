import streamlit as st
import os

st.set_page_config(page_title="Admin Login", page_icon="🔑", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} /* Hides the navbar */
    footer {visibility: hidden;} /* Hides the footer */
    header {visibility: hidden;} /* Hides the header */
    [data-testid="collapsedControl"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            visibility: hidden;
            width: 0px;
        }
    /* Hide the sidebar toggle button */
        [data-testid="collapsedControl"] {
            display: none;
        }

        /* Hide the sidebar itself */
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    <script>
        window.onload = function() {
            var sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.visibility = 'hidden';
                sidebar.style.width = '0px';
            }
        }
    </script>
""", unsafe_allow_html=True)


users_file = "users.txt"

if not os.path.exists(users_file):
    st.error("Database not found.")

def check_user(username, password):
    with open(users_file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            if username == values[0] and password == values[1]:
                return values[2] 
    return None

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "store_name" not in st.session_state:
    st.session_state["store_name"] = None

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["store_name"] = None
    st.rerun()


if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔒Login</h2>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        if st.form_submit_button("Login"):
            store_name = check_user(username, password)
            if store_name:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["store_name"] = store_name 
                st.success(f"Welcome, {store_name}! Redirecting...")
                st.switch_page("pages/1_Home.py")
            else:
                st.error("Invalid Username or Password")

if st.session_state["logged_in"]:
    st.switch_page("pages/1_Home.py")
