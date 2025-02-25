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

st.sidebar.title("Student")

if user_role == "student":
    st.sidebar.page_link("pages/Student_Home.py", label="Home")
    st.sidebar.page_link("pages/Student_Stores.py", label="Stores")
else:
    st.sidebar.write("Please log in to see pages.")
    
Student_Name = st.session_state["store_name"]

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")
if "edit_expanded" not in st.session_state:
    st.session_state["edit_expanded"] = False
def logout():
    st.session_state["logged_in"] = False
    st.rerun()
    
st.markdown(f"<h1 style='text-align: center;'>Welcome! {Student_Name}.</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


if st.button("Edit Account Details"):
    st.session_state["edit_expanded"] = not st.session_state["edit_expanded"] 


if st.session_state["edit_expanded"]:
    with st.expander("Edit Account Details", expanded=True):
        st.write("Update your account details below:")

        current_username = st.session_state.get("username", "")

        new_username = st.text_input("New Username", value=current_username, key="new_username")
        new_password = st.text_input("New Password", type="password", key="new_password")

        if st.button("Update", key="update_btn"):
            if new_username and new_password:
                updated_lines = []
                with open("users.txt", "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 4 and values[0] == current_username:
                            updated_lines.append(f"{new_username},{new_password},{values[2]},{values[3]}\n")
                        else:
                            updated_lines.append(line)

                with open("users.txt", "w") as file:
                    file.writelines(updated_lines)

                st.session_state["username"] = new_username
                st.success("Account details updated successfully!")
                
            else:
                st.error("Please fill in both fields before updating.")


if st.button("Logout"):
    logout()