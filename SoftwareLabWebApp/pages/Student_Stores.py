import streamlit as st
import os

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] { display: none !important; }
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
        }
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100% !important;
        }
        section[data-testid="stSidebar"] { visibility: visible !important; }
    </style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")

Student_Name = st.session_state.get("store_name", "")

st.sidebar.title("Student")
st.sidebar.page_link("pages/Student_Home.py", label="Home")
st.sidebar.page_link("pages/Student_Stores.py", label="Stores")

st.markdown(f"<h1 style='text-align: center;'>Welcome, {Student_Name}!</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

Store = {}
if os.path.exists("users.txt"):
    with open("users.txt", "r") as file:
        for line in file:
            values = line.strip().split(",")
            if len(values) == 4 and values[3] == "admin":
                username, password, store_name = values[:3]
                Store[store_name] = username  

st.markdown("Select a Store:")
for Store in Store.keys():
    if st.button(Store):
        st.session_state["selected_store"] = Store
        st.switch_page("pages/Student_Menu.py")
                       

def logout():
    st.session_state["logged_in"] = False
    st.session_state("selected_store", None)
    st.rerun()
