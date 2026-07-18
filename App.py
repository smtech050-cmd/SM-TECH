import streamlit as st
import pandas as pd
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="Sristi Computer Repair & POS", layout="wide")

# ডামি ডাটাবেজ সেশন (ডাটা ধরে রাখার জন্য)
if "repairs" not in st.session_state:
    st.session_state.repairs = [
        {"ID": 1, "Customer": "Abir Rahman", "Device": "HP Laptop", "Status": "In Progress", "Cost (BDT)": 1200},
        {"ID": 2, "Customer": "Sristi", "Device": "Asus Motherboard", "Status": "Ready", "Cost (BDT)": 2500}
    ]

if "stock" not in st.session_state:
    st.session_state.stock = [
        {"ID": 1, "Item": "512GB NVMe SSD", "Qty": 15, "Price (BDT)": 4200},
        {"ID": 2, "Item": "DDR4 8GB RAM", "Qty": 22, "Price (BDT)": 2400}
    ]

# সাইডবার নেভিগেশন (Sidebar)
st.sidebar.title("⚙️ Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Customer & Repair", "Stock / Inventory", "POS & Invoice"])

# ==========================================
# 📊 1. DASHBOARD
# ==========================================
if menu == "Dashboard":
    st.title("🖥️ Repair & POS Dashboard")
    st.subheader("Sristi Computer Repair")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Repairs", len(st.session_state.repairs))
    col2.metric("Pending Jobs", len([r for r in st.session_state.repairs if r["Status"] != "Ready"]))
    col3.metric("Total Stock Items", len(st.session_state.stock))
    
    st.write("### Quick Overview")
    st.dataframe(pd.DataFrame(st.session_state.repairs), use_container_width=True)

# ==========================================
# 🔧 2. CUSTOMER & REPAIR
# ==========================================
elif menu == "Customer & Repair":
    st.title("🔧 Repair Job Management")
    
    # নতুন রিপেয়ার ইনপুট ফর্ম
    with st.form("Add Repair Job"):
        st.write("### Log New Repair")
        cust_name = st.text_input("Customer Name")
        device = st.text_input("Device Name")
        cost = st.number_input("Estimated Cost (BDT)", min_value=0, step=100)
        submitted = st.form_submit_with_button_kwargs(label="Add Job")
        
        if submitted and cust_name and device:
            new_id = len(st.session_state.repairs) + 1
            st.session_state.repairs.append({
                "ID": new_id, "Customer": cust_name, "Device": device, "Status": "Pending", "Cost (BDT)": cost
            })
            st.success(f"Successfully logged job for {cust_name}!")
            st.rerun()

    st.write("### Current Repair Jobs")
    st.dataframe(pd.DataFrame(st.session_state.repairs), use_container_width=True)

# ==========================================
# 📦 3. STOCK / INVENTORY
# ==========================================
elif menu == "Stock / Inventory":
    st.title("📦 Stock & Inventory Control")
    
    with st.form("Add Stock Item"):
        item_name = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price per Unit (BDT)", min_value=0, step=50)
        submitted = st.form_submit_with_button_kwargs(label="Add Item")
        
        if submitted and item_name:
            new_id = len(st.session_state.stock) + 1
            st.session_state.stock.append({
                "ID": new_id, "Item": item_name, "Qty": qty, "Price (BDT)": price
            })
            st.success(f"Added {item_name} to inventory!")
            st.rerun()

    st.write("### Available Inventory")
    st.dataframe(pd.DataFrame(st.session_state.stock), use_container_width=True)

# ==========================================
# 🧾 4. POS & INVOICE
# ==========================================
elif menu == "POS & Invoice":
    st.title("🧾 Point of Sale & Invoice Generation")
    
    cust_select = st.text_input("Customer Name", value="Walking Customer")
    total_bill = st.number_input("Total Amount (BDT)", min_value=0)
    
    if st.button("Generate & Print Invoice"):
        inv_num = f"INV-{int(datetime.datetime.now().timestamp())}"
        st.success(f"Invoice Generated: {inv_num}")
        
        # প্রিন্ট রেডি ইনভয়েস ভিউ
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:20px; border-radius:10px; background-color:#fafafa; color: #333;">
            <h2>SRISTI COMPUTER REPAIR</h2>
            <hr>
            <p><b>Invoice No:</b> {inv_num}</p>
            <p><b>Date:</b> {datetime.datetime.now().strftime('%d-%m-%Y')}</p>
            <p><b>Customer:</b> {cust_select}</p>
            <table style="width:100%; border-collapse: collapse; margin-top:10px;">
                <tr style="background-color:#eee;"><th style="padding:8px; text-align:left;">Description</th><th style="padding:8px; text-align:right;">Total</th></tr>
                <tr><td style="padding:8px;">Computer Repair Services / Parts</td><td style="padding:8px; text-align:right;">{total_bill} BDT</td></tr>
            </table>
            <h3 style="text-align:right; margin-top:15px;">Total Paid: {total_bill} BDT</h3>
        </div>
        """, unsafe_allowed_html=True)
        
        st.info("💡 Tip: Use your browser's Print shortcut (Ctrl+P / Cmd+P) to save this as a PDF or Print.")
