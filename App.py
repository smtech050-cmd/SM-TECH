import streamlit as st
import pandas as pd
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔐 লগইন সেশন স্টেট
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 🎨 ডার্ক ব্লু নিয়ন থিম সিএসএস (লগইন ও ব্যাকগ্রাউন্ড)
# ==========================================
login_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #001f4d 0%, #000a1a 100%);
        color: white;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .panel-header {
        font-size: 20px;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #0055ff;
        padding-bottom: 10px;
    }
    .stTextInput label, .stNumberInput label {
        color: #a0c0ff !important;
        font-weight: bold;
    }
</style>
"""

# ==========================================
# 🌐 ভাষা ডিকশনারি
# ==========================================
LANG = {
    "English": {
        "nav_title": "⚙️ SM-TECH",
        "go_to": "Go to",
        "menu": ["Dashboard", "Customer & Repair", "Stock / Inventory", "POS & Invoice"],
        "dash_title": "🖥️ Repair & POS Dashboard",
        "sub_title": "SM-TECH Computer & IT Solution",
        "t_repairs": "Total Repairs",
        "p_jobs": "Pending Jobs",
        "t_stock": "Total Stock Items",
        "quick_ov": "### Quick Overview",
        "rep_title": "🔧 Repair Job Management",
        "log_new": "### Log New Repair",
        "c_name": "Customer Name",
        "d_name": "Device Name",
        "est_cost": "Estimated Cost (BDT)",
        "btn_add": "Add Job",
        "succ_job": "Successfully logged job for {}!",
        "curr_job": "### Current Repair Jobs",
        "stock_title": "📦 Stock & Inventory Control",
        "add_stock": "Add Stock Item",
        "item_name": "Item Name",
        "qty": "Quantity",
        "price": "Price per Unit (BDT)",
        "btn_item": "Add Item",
        "succ_stock": "Added {} to inventory!",
        "avail_stock": "### Available Inventory",
        "pos_title": "🧾 Point of Sale & Invoice Generation",
        "walking": "Walking Customer",
        "total_bill": "Total Amount (BDT)",
        "btn_inv": "📄 Generate Invoice"
    },
    "বাংলা": {
        "nav_title": "⚙️ SM-TECH",
        "go_to": "মেনু সিলেক্ট করুন",
        "menu": ["ড্যাশবোর্ড", "কাস্টমার ও রিপেয়ার", "স্টক / ইনভেন্টরি", "POS ও ইনভয়েস"],
        "dash_title": "🖥️ রিপেয়ার ও POS ড্যাশবোর্ড",
        "sub_title": "এসএম-টেক কম্পিউটার ও আইটি সリューション",
        "t_repairs": "মোট রিপেয়ার",
        "p_jobs": "চলতি কাজ",
        "t_stock": "মোট স্টক আইটেম",
        "quick_ov": "### সংক্ষিপ্ত বিবরণ",
        "rep_title": "🔧 রিপেয়ার জব ম্যানেজমেন্ট",
        "log_new": "### নতুন রিপেয়ার এন্ট্রি",
        "c_name": "কাস্টমারের নাম",
        "d_name": "ডিভাইসের নাম",
        "est_cost": "আনুমানিক খরচ (টাকা)",
        "btn_add": "জব যুক্ত করুন",
        "succ_job": "সফলভাবে {} এর জন্য জব যুক্ত হয়েছে!",
        "curr_job": "### বর্তমান রিপেয়ার লিস্ট",
        "stock_title": "📦 স্টক ও ইনভেন্টরি কন্ট্রোল",
        "add_stock": "নতুন স্টক আইটেম",
        "item_name": "আইটেমের নাম",
        "qty": "পরিমাণ",
        "price": "গায়ের দাম (টাকা)",
        "btn_item": "আইটেম যুক্ত করুন",
        "succ_stock": "স্টকে {} যুক্ত হয়েছে!",
        "avail_stock": "### বর্তমানে মজুদ মালামাল",
        "pos_title": "🧾 পয়েন্ট অব সেল ও ইনভয়েস",
        "walking": "খুচরা কাস্টমার",
        "total_bill": "মোট বিল (টাকা)",
        "btn_inv": "📄 ইনভয়েস তৈরি করুন"
    }
}

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং
# ==========================================
if not st.session_state.logged_in:
    st.markdown(login_css, unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('''
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 50px;">🔒</span>
                <span style="font-size: 36px; font-weight: bold; color: white;">SM-TECH - </span>
                <span style="font-size: 36px; font-weight: bold; color: #00a2ff;">Admin Login</span>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown('<div class="panel-header">অ্যাডমিন প্যানেল প্রবেশ করুন</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            
            st.markdown('<br>', unsafe_allow_html=True)
            login_btn = st.button("🔓 লগইন করুন", use_container_width=True)
            
            if login_btn:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড স্ক্রিন (লগইন সফল হলে)
# ==========================================
else:
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

    # ⚙️ সাইডবার নেভিগেশন
    st.sidebar.title(LANG["English"]["nav_title"])
    
    if st.sidebar.button("🔒 Logout / লগআউট"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.write("---")
    selected_lang = st.sidebar.selectbox("Language / ভাষা", ["English", "বাংলা"], index=0)
    t = LANG[selected_lang]

    st.sidebar.markdown(f"**{t['go_to']}**")
    menu_choice = st.sidebar.radio("", t["menu"], label_visibility="collapsed")

    # --- 📊 ড্যাশবোর্ড মডিউল ---
    if menu_choice == t["menu"][0]:
        st.title(t["dash_title"])
        st.subheader(t["sub_title"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric(t["t_repairs"], len(st.session_state.repairs))
        col2.metric(t["p_jobs"], len([r for r in st.session_state.repairs if r["Status"] != "Ready"]))
        col3.metric(t["t_stock"], len(st.session_state.stock))
        
        st.write(t["quick_ov"])
        st.dataframe(pd.DataFrame(st.session_state.repairs), use_container_width=True)

    # --- 🔧 রিপেয়ার মডিউল ---
    elif menu_choice == t["menu"][1]:
        st.title(t["rep_title"])
        with st.form("Add Repair Job"):
            st.write(t["log_new"])
            cust_name = st.text_input(t["c_name"])
            device = st.text_input(t["d_name"])
            cost = st.number_input(t["est_cost"], min_value=0, step=100)
            submitted = st.form_submit_button(label=t["btn_add"])
            
            if submitted and cust_name and device:
                new_id = len(st.session_state.repairs) + 1
                st.session_state.repairs.append({
                    "ID": new_id, "Customer": cust_name, "Device": device, "Status": "Pending", "Cost (BDT)": cost
                })
                st.success(t["succ_job"].format(cust_name))
                st.rerun()

        st.write(t["curr_job"])
        st.dataframe(pd.DataFrame(st.session_state.repairs), use_container_width=True)

    # --- 📦 স্টক মডিউল ---
    elif menu_choice == t["menu"][2]:
        st.title(t["stock_title"])
        with st.form("Add Stock Item"):
            st.write(t["add_stock"])
            item_name = st.text_input(t["item_name"])
            qty = st.number_input(t["qty"], min_value=0, step=1)
            price = st.number_input(t["price"], min_value=0, step=50)
            submitted = st.form_submit_button(label=t["btn_item"])
            
            if submitted and item_name:
                new_id = len(st.session_state.stock) + 1
                st.session_state.stock.append({
                    "ID": new_id, "Item": item_name, "Qty": qty, "Price (BDT)": price
                })
                st.success(t["succ_stock"].format(item_name))
                st.rerun()

        st.write(t["avail_stock"])
        st.dataframe(pd.DataFrame(st.session_state.stock), use_container_width=True)

    # --- 🧾 POS ও ইনভয়েস মডিউল ---
    elif menu_choice == t["menu"][3]:
        st.title(t["pos_title"])
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            cust_name = st.text_input(t["c_name"], value=t["walking"])
            cust_address = st.text_input("Address (ঠিকানা)", value="Dhaka, Bangladesh")
        with col_in2:
            item_desc = st.text_input("Description (পণ্যের নাম বা বিবরণ)", value="Motherboard & SSD Service")
            total_bill = st.number_input(t["total_bill"], min_value=0, value=1500)
            
        st.write("---")
        
        if st.button(t["btn_inv"]):
            inv_num = f"{int(datetime.datetime.now().timestamp()) % 100000}"
            current_date = datetime.datetime.now().strftime('%d-%m-%Y')
            
            logo_path = "logo.png" 
            
            # 📐 H 7" এবং W 5" সাইজের আপগ্রেডেড ক্যাশ মেমো থিম
            invoice_html = f"""
            <div id="print-area" style="
                border: 3px solid #1e3a8a; 
                padding: 18px; 
                background-color: white; 
                color: black; 
                font-family: 'Arial', sans-serif; 
                width: 5in; 
                height: 7in; 
                margin: auto; 
                border-radius: 4px;
                box-sizing: border-box;
                position: relative;
            ">
                
                <!-- টপ ব্র্যান্ডিং হেডার উইথ লোগো -->
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 5px;">
                    <tr>
                        <td style="width: 20%; vertical-align: middle; text-align: left;">
                            <img src="{logo_path}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover;" onerror="this.style.display='none';">
                        </td>
                        <td style="width: 48%; vertical-align: middle; padding-left: 8px;">
                            <span style="font-size: 30px; font-weight: 900; color: #1e3a8a; font-family: 'Arial Black', Impact, sans-serif; line-height: 1.1; display: block; letter-spacing: -0.5px;">SM-TECH</span>
                            <span style="font-size: 8.5px; font-weight: 800; color: #059669; letter-spacing: 0.8px; display: block; margin-top: 2px;">COMPUTER & IT SOLUTION</span>
                            <span style="font-size: 8px; font-style: italic; color: #555; display: block; margin-top: 2px;">Smart Technology-Trusted Service</span>
                        </td>
                        <td style="width: 32%; text-align: right; font-size: 11px; line-height: 1.4; vertical-align: middle; font-weight: bold; color: #111;">
                            <span style="font-size: 14px; font-weight: 900; color: #1e3a8a; display: block; margin-bottom: 2px;">S.m. Ibrahim</span>
                            <span style="font-size: 10px; color: #555; display: block; margin-top: -3px; margin-bottom: 2px; font-weight: normal;">Owner</span>
                            <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01940-556114</span>
                            <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01810-499166</span>
                        </td>
                    </tr>
                </table>
                
                <div style="border-top: 2.5px solid #1e3a8a; margin-top: 8px; margin-bottom: 12px;"></div>
                
                <!-- কাস্টমার এবং বিল বিবরণী -->
                <table style="width: 100%; font-size: 11px; margin-bottom: 12px; line-height: 1.4;">
                    <tr>
                        <td style="width: 55%; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 7px; font-weight: bold; font-size: 9.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">Bill To</span>
                            <div style="margin-top: 4px;"><b>Name:</b> {cust_name}</div>
                            <div style="margin-top: 2px;"><b>Address:</b> {cust_address}</div>
                        </td>
                        <td style="width: 45%; text-align: right; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 12px; font-weight: bold; font-size: 10.5px; letter-spacing: 0.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">INVOICE</span>
                            <div style="margin-top: 4px;"><b>Invoice No:</b> # {inv_num}</div>
                            <div style="margin-top: 2px;"><b>Date:</b> {current_date}</div>
                        </td>
                    </tr>
                </table>
                
                <!-- মেইন প্রোডাক্ট টেবিল -->
                <table style="width: 100%; border-collapse: collapse; font-size: 11px; border: 1px solid #1e3a8a;">
                    <thead>
                        <tr style="background-color: #1e3a8a; color: white; text-align: center; font-weight: bold; font-size: 10px;">
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 8%;">S.L</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 6px; width: 52%;">DESCRIPTION</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 10%;">QTY</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 14%;">U.PRICE</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 16%;">AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="text-align: center; height: 26px;">
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">1</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px 6px; text-align: left;">{item_desc}</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">1</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">{total_bill}/-</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px; font-weight: bold;">{total_bill}/-</td>
                        </tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">2</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">3</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">4</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">5</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">6</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">7</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">8</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">9</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">10</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        
                        <!-- সাব টোটাল অংশ -->
                        <tr>
                            <td colspan="3" style="border: 1px solid #1e3a8a;"></td>
                            <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #1e3a8a; color: white; font-size: 10px;">SUB TOTAL</td>
                            <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #f3f4f6; font-size: 11px;">{total_bill} BDT</td>
                        </tr>
                    </tbody>
                </table>
                
                <!-- বটম পার্ট -->
                <table style="width: 100%; position: absolute; bottom: 18px; left: 18px; width: calc(100% - 36px); font-size: 10px;">
                    <tr>
                        <td style="width: 50%; vertical-align: bottom;">
                            <div style="border: 1px solid #1e3a8a; display: inline-block; border-radius: 2px; background-color: white;">
                                <div style="background-color: #1e3a8a; color: white; padding: 2px 6px; font-weight: bold; font-size: 8.5px;">Payment Methods</div>
                                <div style="padding: 3px 6px; font-weight: bold; color: #222; font-size: 9.5px;">Cash | Bkash | Nagad | Bank</div>
                            </div>
                        </td>
                        <td style="width: 50%; text-align: right; vertical-align: bottom;">
                            <div style="display: inline-block; text-align: center; width: 150px;">
                                <div style="border-top: 1px solid #000; margin-bottom: 3px;"></div>
                                <b>Authorised Signature</b><br>
                                <span style="font-size: 8.5px; color: #444;">SM-TECH Computer & IT Solutions</span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            """
            
            # অ্যাপ স্ক্রিনে দেখানো
            st.markdown(invoice_html, unsafe_allow_html=True)
            st.write("")
            
            # 📥 ৫×৭ সাইজ অনুযায়ী পিডিএফ প্রিন্ট বাটন
            st.components.v1.html(f"""
                <script>
                function printInvoice() {{
                    var WinPrint = window.open('', '', 'width=600,height=800');
                    WinPrint.document.write('<html><head><title>Print Invoice</title>');
                    WinPrint.document.write('<style>@page {{ size: 5in 7in; margin: 0; }} body {{ margin: 0; }}</style></head><body>');
                    WinPrint.document.write(`{invoice_html}`);
                    WinPrint.document.write('</body></html>');
                    WinPrint.document.close();
                    WinPrint.focus();
                    setTimeout(function() {{ WinPrint.print(); }}, 500);
                }}
                </script>
                <div style="text-align: center; margin-top: 5px;">
                    <button onclick="printInvoice()" style="background-color: #059669; color: white; padding: 10px 25px; font-size: 14px; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                        📥 Download 5"x7" PDF / Print Invoice
                    </button>
                </div>
            """, height=65)
