import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Order Confirmation", page_icon="✅", layout="wide")

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


st.title("Confirm Order")

if "selected_store" not in st.session_state:
    st.warning("No store selected. Please go back and select a store.")
    st.stop()

if "username" not in st.session_state:
    st.warning("No username found. Please log in again.")
    st.stop()

if "order_summary" not in st.session_state or not st.session_state["order_summary"]:
    st.warning("No order details found. Please go back and place an order.")
    st.stop()

store_name = st.session_state["selected_store"]
student_name = st.session_state["username"]
discount_name = st.session_state.get("discount_name", "")
order_summary = st.session_state["order_summary"]
discount_applied = st.session_state.get("discount_applied", 0)
discount_container = st.session_state.get("discount_container")
final_price = st.session_state.get("final_price", 0)

order_data = [
    {"Item Name": item, "Quantity": qty, "Price (₱)": f"{price:.2f}", "Total (₱)": f"{qty * price:.2f}"}
    for item, (qty, price) in order_summary.items()
]

st.markdown("### **Order Summary**")
st.table(pd.DataFrame(order_data))

if discount_applied > 0:
    st.markdown(f"**Discount Applied:** -₱{discount_applied:.2f}")
    if discount_container:
        st.markdown(f"**Container Discount applied: -10%**")
st.markdown(f"### **Total Price: ₱{final_price:.2f}**")

qr_payments = {}
if os.path.exists("payments.txt"):
    with open("payments.txt", "r") as file:
        for line in file:
            values = line.strip().split(",")
            if len(values) == 2:
                qr_payments[values[0]] = values[1]

if store_name in qr_payments and os.path.exists(qr_payments[store_name]):
    st.image(qr_payments[store_name], caption="Scan this QR to pay", width=350)
else:
    st.error("No QR payment image found for this store.")

st.markdown("**Please present the proof of payment upon pick up**")

st.markdown("### **Upload Proof of Payment**")

uploaded_file = st.file_uploader("Upload your payment proof (JPG/PNG)", type=["jpg", "png"])


col1, col2 = st.columns(2)

with col1:
    if st.button("Go Back"):
        st.switch_page("pages/Student_Menu.py")

with col2:
    if st.button("Confirm Order"):
        menu_file = "samplemenu.txt"
        discount_file = "discounts.txt"
        if uploaded_file:
            UPLOAD_FOLDER = "proof_of_payments"
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{store_name}_{student_name}_{timestamp}.png"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with open("proof_of_payments.txt", "a") as file:
                file.write(f"{store_name},{student_name},{file_path}\n")
            
            st.session_state["proof_of_payment_path"] = file_path  
            
            if os.path.exists(menu_file):
                updated_menu = []
                with open(menu_file, "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 6 and values[0] == store_name:
                            _, item, description, price, stock, availability = values
                            stock = int(stock)
                            
                            if item in order_summary:
                                qty_ordered, _ = order_summary[item]
                                stock -= qty_ordered
                                availability = "Out of stock" if stock == 0 else "Available"

                            updated_menu.append(f"{store_name},{item},{description},{price},{stock},{availability}\n")
                        else:
                            updated_menu.append(line)
                
                with open(menu_file, "w") as file:
                    file.writelines(updated_menu)

            if discount_applied > 0 and os.path.exists(discount_file):
                updated_discounts = []
                with open(discount_file, "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 4 and values[0] == store_name and values[1] == discount_name:
                            continue 
                        updated_discounts.append(line)

                with open(discount_file, "w") as file:
                    file.writelines(updated_discounts)

            st.success("Order confirmed successfully!")
            time.sleep(2)
            st.switch_page("pages/Student_Stores.py")
        else:
            st.warning("Please Upload Proof of Payment!")

