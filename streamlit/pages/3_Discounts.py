import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
pd.set_option("display.max_colwidth", None)  


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")


store_name = st.session_state.get("store_name", "")


st.markdown(f"<h1 style='text-align: center;'>{store_name} Discounts</h1>", unsafe_allow_html=True)

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

def add_discounts():
    with st.expander("Add Discount", expanded=False):
        st.write("Fill in the details below:")

        discount_name = st.text_input("Discount Name")
        Value = st.number_input("Value", min_value=0, step=1)
        if st.button("Add Discount"):
            if discount_name and Value <= 0:
                st.error("Please fill in all fields before submitting.")
                return
            
            discount_exist = False
            with open("discounts.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 3 and values[1] == discount_name:
                        discount_exist = True
                        break 

            if discount_exist:
                st.error(f"Discount '{discount_name}' already exists!")
            else:
                with open("discounts.txt", "a") as file:
                    file.write(f"{store_name},{discount_name},{Value} php off\n")

                st.success(f"Discount '{discount_name}' added successfully!")
                st.rerun() 

def update_discounts():
    with st.expander("Update Discount", expanded=False):
        st.write("Select or search an item to update.")

        lines = []
        with open("discounts.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 3 and values[0] == store_name:  
                    lines.append(values)

        if not lines:
            st.warning("No items available to update.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Discount Name", "Value"])
        

        search_query = st.text_input("Search Discount")
        if search_query:
            df = df[df["Discount Name"].str.contains(search_query, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to update", df["Discount Name"].tolist())

        item_details = df[df["Discount Name"] == selected_item].iloc[0]
        current_item_name = item_details["Discount Name"]
        Value = item_details["Value"].replace(" php off", "")

        new_item_name = st.text_input("Discount Name", value=current_item_name)  
        Value = st.number_input("Value", min_value=0, step=1, value=int(Value))


        if st.button("Update Discount"):
            updated_lines = []
            with open("discounts.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 3 and values[0] == store_name and values[1] == current_item_name:
                        updated_lines.append(f"{store_name},{new_item_name},{Value} php off\n")
                    else:
                        updated_lines.append(line)


            with open("discounts.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"✅ Discount '{current_item_name}' updated to '{new_item_name}' successfully!")
            st.rerun()  

def delete_discounts():
    with st.expander("Delete Discount", expanded=False):
        st.write("Search and select an item to delete.")

        lines = []
        with open("discounts.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 3 and values[0] == store_name: 
                    lines.append(values)

        if not lines:
            st.warning("No items available to delete.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Discount Name", "Value"])

        search_query_delete = st.text_input("Search Discount", key="delete_search")

        if search_query_delete:
            df = df[df["Discount Name"].str.contains(search_query_delete, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to delete", df["Discount Name"].tolist(), key="delete_select")

        item_details = df[df["Discount Name"] == selected_item].iloc[0]
        discount_name = item_details["Discount Name"]
        Value = item_details["Value"]

        st.markdown(f"**Discount Name:** {discount_name}")
        st.markdown(f"**Value:** {Value}")

        if st.button("Confirm Delete", key="delete_button"):
            updated_lines = []
            with open("discounts.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 3 and values[0] == store_name and values[1] == discount_name:
                        continue  
                    updated_lines.append(line)


            with open("discounts.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"Discount '{discount_name}' deleted successfully!")
            st.rerun()  

    
               
col1, col2, col3 = st.columns([2, 2, 2])

with col1: 
 add_discounts()
    
with col2: 
    update_discounts()
    
with col3: 
    delete_discounts()


lines = []
with open("discounts.txt", "r") as file:
    for line in file:
        values = line.strip().split(",")
        if len(values) == 3 and values[0] == store_name:
            lines.append(values[1:])  


df = pd.DataFrame(lines, columns=["Discount Name", "Value"])


st.data_editor(df, 
    use_container_width=True, 
    hide_index=True, 
)
