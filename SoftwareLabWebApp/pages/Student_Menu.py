import streamlit as st
import os
st.set_page_config(page_title="Menu", layout="wide")

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

store_name = st.session_state["selected_store"]

st.title(f"{store_name} Menu")

if os.path.exists("samplemenu.txt"):
        menu_items = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 6 and values[0] == store_name:
                    _, item, description, price, stock, availability = values
                    menu_items.append({
                        "name": item,
                        "description": description,
                        "price": float(price.split()[0]), 
                        "stock": int(stock),
                        "available": availability.lower() == "available"
                    })

        if menu_items:
            col1, col2= st.columns([3, 1])

            with col1: 

                with st.expander(f"{store_name} Menu", expanded=True):
                    st.markdown("Select Items to Order:")
                    order = {}
                    for item in menu_items:
                        if item["available"]:
                            quantity = st.number_input(
                                f"**{item['name']}** - {item['description']} (₱{item['price']:.2f})",
                                min_value=0, max_value=item["stock"], value=0, step=1
                            )
                            if quantity > 0:
                                order[item["name"]] = (quantity, item["price"])

                    total_price = sum(qty * price for qty, price in order.values())
            with col2:
                    discount = 0.00
                    discount_found = False
                    discount_name = st.text_input("Discount Vouchers")

                    if os.path.exists("discounts.txt"):
                        with open("discounts.txt", "r") as file:
                            discount_lines = file.readlines()

                        for line in discount_lines:
                            values = line.strip().split(",")
                            if len(values) == 4 and values[0] == store_name and values[1] == discount_name:
                                discount = float(values[2].split(' ')[0])
                                discount_found = True
                                break
                            elif discount_name == "":
                                discount_found = True
                                break
                                
                    final_price = total_price - discount          
                    
                    st.markdown(f"Total: **₱{final_price:.2f}**")
                    if discount > 0:
                        st.markdown(f"*(Discount applied: -₱{discount:.2f})*")
                    elif discount_name and not discount_found:
                        st.warning("Invalid discount voucher.")
                        
                    if st.button("Place Order"):
                        st.session_state["order_summary"] = order
                        st.session_state["discount_applied"] = discount
                        st.session_state["discount_name"] = discount_name
                        st.session_state["final_price"] = final_price
                        if discount_found:
                            st.switch_page("pages/Student_ConfirmOrder.py")
                        st.rerun() 
                            
        else:
            st.warning(f"No menu items found for {store_name}.")
        
            
if st.button("Back"):
    st.switch_page("pages/Student_Stores.py")
        