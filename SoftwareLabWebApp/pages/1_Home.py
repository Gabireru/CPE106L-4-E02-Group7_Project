import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.markdown("""
    <style>
        /* Hide the first sidebar navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
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
        /* Ensure only the custom sidebar is visible */
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }
    </style>
""", unsafe_allow_html=True)

user_role = st.session_state.get("role", "") 

st.sidebar.title("Admin")

if user_role == "admin":
    st.sidebar.page_link("pages/1_Home.py", label="Home")
    st.sidebar.page_link("pages/2_Menu.py", label="Menu")
    st.sidebar.page_link("pages/3_Discounts.py", label="Discounts")
    st.sidebar.page_link("pages/4_Stock Management.py", label="Stock Management")
    st.sidebar.page_link("pages/5_Transactions.py", label="Transactions")


store_name = st.session_state.get("store_name", "")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")
if "edit_expanded" not in st.session_state:
    st.session_state["edit_expanded"] = False
def logout():
    st.session_state["logged_in"] = False
    st.rerun()
    
st.markdown(f"<h1 style='text-align: center;'>Welcome! {store_name}.</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


if st.button("Edit Account Details"):
    st.session_state["edit_expanded"] = not st.session_state["edit_expanded"] 

if st.session_state.get("edit_expanded", False):
    with st.expander("Edit Account Details", expanded=True):
        st.write("Update your account details below:")

        current_username = st.session_state.get("username", "")

        new_username = st.text_input("New Username", value=current_username, key="new_username")
        new_password = st.text_input("New Password", type="password", key="new_password")

        if st.button("Update", key="update_btn"):
            if not new_username and not new_password:
                st.error("Please fill in at least one field before updating.")
            else:
                existing_usernames = set()
                updated_lines = []
                username_exists = False

                with open("users.txt", "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if values:
                            existing_usernames.add(values[0])

                if new_username != current_username and new_username in existing_usernames:
                    st.error("Username already exists. Please choose a different one.")
                else:
                    with open("users.txt", "r") as file:
                        for line in file:
                            values = line.strip().split(",")
                            if len(values) == 4 and values[0] == current_username:
                                updated_username = new_username if new_username else values[0]
                                updated_password = new_password if new_password else values[1]
                                updated_lines.append(f"{updated_username},{updated_password},{values[2]},{values[3]}\n")
                            else:
                                updated_lines.append(line)

                    with open("users.txt", "w") as file:
                        file.writelines(updated_lines)

                    if new_username:
                        st.session_state["username"] = new_username
                    st.success("Account details updated successfully!")


if st.button("Menu Page"):
    st.switch_page("pages/2_Menu.py")
    
if st.button("Discount Page"):
    st.switch_page("pages/3_Discounts.py")
    
if st.button("Stock Management Page"):
    st.switch_page("pages/4_Stock Management.py")
    
if st.button("Transaction Page"):
    st.switch_page("pages/5_Transactions.py")

if st.button("Logout"):
    logout()