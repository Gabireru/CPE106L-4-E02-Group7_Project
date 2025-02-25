import streamlit as st
import os

st.set_page_config(page_title="Admin Login", page_icon="🔑", layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;} 
        div[data-testid="stDataFrame"] td { 
            white-space: normal !important; 
            word-break: break-word !important;
            overflow-wrap: break-word !important;
        }
        div[data-testid="stDataFrameContainer"] {
            width: 100% !important;
        }
        /* Hide the first sidebar navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
        .stButton > button {
            width: 100% !important;
            height: 70px !important;
            font-size: 20px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            display: block !important;
        }
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100% !important;
        }
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            visibility: hidden;
            width: 0px;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
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
                return values[2], values[3]
    return None, None

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "store_name" not in st.session_state:
    st.session_state["store_name"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
    
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["store_name"] = None
    st.session_state["role"] = None
    st.rerun()


if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔒Login</h2>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        if st.form_submit_button("Login"):
            store_name, role = check_user(username, password)
            if store_name:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["store_name"] = store_name 
                st.session_state["role"] = role 
                st.success(f"Welcome, {store_name}! Redirecting...")
                if role == "admin":
                    st.switch_page("pages/1_Home.py")
                else:
                    st.switch_page("pages/Student_Home.py")
            else:
                st.error("Invalid Username or Password")


