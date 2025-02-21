import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} /* Hides the navbar */
    footer {visibility: hidden;} /* Hides the footer */
    header {visibility: hidden;} /* Hides the header */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

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
                        if len(values) == 3 and values[0] == current_username:
                            updated_lines.append(f"{new_username},{new_password},{values[2]}\n")
                        else:
                            updated_lines.append(line)

                with open("users.txt", "w") as file:
                    file.writelines(updated_lines)

                st.session_state["username"] = new_username
                st.success("Account details updated successfully!")
                
            else:
                st.error("Please fill in both fields before updating.")

if st.button("Menu Page"):
    st.switch_page("pages/2_Menu.py")
if st.button("Discount Page"):
    st.switch_page("pages/3_Discounts.py")

if st.button("Logout"):
    logout()
