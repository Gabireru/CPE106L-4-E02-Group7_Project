import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
pd.set_option("display.max_colwidth", None)  


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")


store_name = st.session_state.get("store_name", "")


st.markdown(f"<h1 style='text-align: center;'>{store_name} Menu</h1>", unsafe_allow_html=True)

st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                div[data-testid="stDataFrame"] td { 
                    white-space: normal !important; 
                    word-break: break-word !important;
                    overflow-wrap: break-word !important;
                }
                div[data-testid="stDataFrameContainer"] {
                    width: 100% !important;
                }
                .stButton > button {
                    width: 100%;
                    height: 60px;
                    font-size: 20px;
                    font-weight: bold;
                    border-radius: 10px;
                }
            </style>
            """, unsafe_allow_html=True)

def add_item():
    with st.expander("Add Item", expanded=False):
        st.write("Fill in the details below:")

        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        price = st.number_input("Price", min_value=0, step=1)
        if st.button("Add Item"):
            if item_name and  description and price <= 0:
                st.error("Please fill in all fields before submitting.")
                return
            
            item_exists = False
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 4 and values[1] == item_name:
                        item_exists = True
                        break 

            if item_exists:
                st.error(f"Item '{item_name}' already exists!")
            else:
                with open("samplemenu.txt", "a") as file:
                    file.write(f"{store_name},{item_name},{description},{price} php\n")

                st.success(f"Item '{item_name}' added successfully!")
                st.rerun() 

def update_item():
    with st.expander("Update Item", expanded=False):
        st.write("Select or search an item to update.")

        lines = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 4 and values[0] == store_name:  
                    lines.append(values)

        if not lines:
            st.warning("No items available to update.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Item Name", "Description", "Price"])
        

        search_query = st.text_input("Search Item")
        if search_query:
            df = df[df["Item Name"].str.contains(search_query, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to update", df["Item Name"].tolist())

        item_details = df[df["Item Name"] == selected_item].iloc[0]
        current_item_name = item_details["Item Name"]
        current_description = item_details["Description"]
        current_price = item_details["Price"].replace(" php", "")

        new_item_name = st.text_input("Item Name", value=current_item_name)  
        new_description = st.text_area("Description", value=current_description)
        new_price = st.number_input("Price", min_value=0, step=1, value=int(current_price))


        if st.button("Update Item"):
            updated_lines = []
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 4 and values[0] == store_name and values[1] == current_item_name:
                        updated_lines.append(f"{store_name},{new_item_name},{new_description},{new_price} php\n")
                    else:
                        updated_lines.append(line)


            with open("samplemenu.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"✅ Item '{current_item_name}' updated to '{new_item_name}' successfully!")
            st.rerun()  

def delete_item():
    with st.expander("Delete Item", expanded=False):
        st.write("Search and select an item to delete.")

        lines = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 4 and values[0] == store_name: 
                    lines.append(values)

        if not lines:
            st.warning("No items available to delete.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Item Name", "Description", "Price"])

        search_query_delete = st.text_input("Search Item", key="delete_search")

        if search_query_delete:
            df = df[df["Item Name"].str.contains(search_query_delete, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to delete", df["Item Name"].tolist(), key="delete_select")

        item_details = df[df["Item Name"] == selected_item].iloc[0]
        item_name = item_details["Item Name"]
        item_description = item_details["Description"]
        item_price = item_details["Price"]

        st.markdown(f"**Item Name:** {item_name}")
        st.markdown(f"**Description:** {item_description}")
        st.markdown(f"**Price:** {item_price}")

        if st.button("Confirm Delete", key="delete_button"):
            updated_lines = []
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 4 and values[0] == store_name and values[1] == item_name:
                        continue  
                    updated_lines.append(line)


            with open("samplemenu.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"Item '{item_name}' deleted successfully!")
            st.rerun()  

    
               
col1, col2, col3 = st.columns([2, 2, 2])

with col1: 
    add_item()
    
with col2: 
    update_item()
    
with col3: 
    delete_item()


lines = []
with open("samplemenu.txt", "r") as file:
    for line in file:
        values = line.strip().split(",")
        if len(values) == 4 and values[0] == store_name:
            lines.append(values[1:])  


df = pd.DataFrame(lines, columns=["Item Name", "Description", "Price"])


st.data_editor(df, 
    use_container_width=True, 
    hide_index=True, 
    column_config={
        "Description": st.column_config.TextColumn(width="large", help="Full description visible")
    }
)
