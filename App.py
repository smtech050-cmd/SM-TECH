import streamlit as st
import pandas as pd
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin Login", layout="wide")

# ==========================================
# 🔐 লগইন সেশন স্টেট (Login Session State)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 🎨 ডার্ক ব্লু নিয়ন থিম সিএসএস (Custom CSS)
# ==========================================
login_css = """
<style>
    /* পুরো পেজের ব্যাকগ্রাউন্ড ও টেক্সট কাস্টমাইজেশন */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #001f4d 0%, #000a1a 100%);
        color: white;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    /* লগইন বক্সের মেইন কন্টেইনার */
    .login-box {
        background-color: rgba(0, 15, 38, 0.85);
        border: 2px solid #0055ff;
        box-shadow: 0px 0px 25px rgba(0, 85, 255, 0.4);
        border-radius: 15px;
        padding: 40px;
        max-width: 500px;
        margin: auto;
        text-align: center;
    }
    .login-title {
        font-size: 28px;
        font-weight: bold;
        color: white;
        margin-bottom: 5px;
    }
    .login-subtitle {
        font-size: 32px;
        font-weight: bold;
        color: #00a2ff;
        margin-bottom: 25px;
    }
    .panel-header {
        font-size: 20px;
        color: #e0e0e0;
        margin-bottom: 20px;
        border-bottom: 1px solid #0055ff;
        padding-bottom: 10px;
    }
    /* ইনপুট লেবেল কালার */
    .stTextInput label {
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
        "sub_title": "Sristi Computer Repair",
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
        "btn_inv": "Generate & Print Invoice",
        "inv_gen": "Invoice Generated: {}",
        "desc": "Description",
        "total": "Total",
        "service_desc": "Computer Repair Services / Parts",
        "total_paid": "Total Paid: {} BDT",
        "tip": "💡 Tip: Use your browser's Print shortcut (Ctrl+P / Cmd+P) to save this as a PDF or Print."
    },
    "বাংলা": {
        "nav_title": "⚙️ SM-TECH",
        "go_to": "মেনু সিলেক্ট করুন",
        "menu": ["ড্যাশবোর্ড", "কাস্টমার ও রিপেয়ার", "স্টক / ইনভেন্টরি", "POS ও ইনভয়েস"],
        "dash_title": "🖥️ রিপেয়ার ও POS ড্যাশবোর্ড",
        "sub_title": "সৃষ্টি কম্পিউটার রিপেয়ার",
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
        "succ_job": "সফলভাবে {} এর জন্য জব যুক্ত হয়েছে!",
        "curr_job": "### বর্তমান রিপেয়ার লিস্ট",
        "stock_title": "📦 স্টক ও ইনভেন্টরি কন্ট্রোল",
        "add_stock": "নতুন স্টক আইটেম",
        "item_name": "আইটেমের নাম",
        "qty": "পরিমাণ",
        "price": "গায়ের দাম (টাকা)",
        "btn_item": "আইটেম যুক্ত করুন",
        "succ_stock": "স্টকে {} যুক্ত হয়েছে!",
        "avail_stock": "### balconies মজুদ মালামাল",
        "pos_title": "🧾 পয়েন্ট অব সেল ও ইনভয়েস",
        "walking": "খুচরা কাস্টমার",
        "total_bill": "মোট বিল (টাকা)",
        "btn_inv": "ইনভয়েস তৈরি ও প্রিন্ট করুন",
        "inv_gen": "ইনভয়েস তৈরি হয়েছে: {}",
        "desc": "বিবরণ",
        "total": "মোট",
        "service_desc": "কম্পিউটার মেরামত সার্ভিস / পার্টস বাবদ",
        "total_paid": "সর্বমোট পরিশোধ: {} টাকা",
        "tip": "💡 টিপস: এই ইনভয়েসটি PDF সেভ বা প্রিন্ট করতে কিবোর্ড থেকে Ctrl+P চাপুন।"
    }
}

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং (যদি লগইন না থাকে)
# ==========================================
if not st.session_state.logged_in:
    st.markdown(login_css, unsafe_allowed_html=True)
    
    # পেজের মাঝে আনার জন্য কলাম লেআউট
    _, col_center, _ = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('<br><br>', unsafe_allowed_html=True)
        st.markdown('''
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 50px;">🔒</span>
                <span style="font-size: 36px; font-weight: bold; color: white;">SM-TECH - </span>
                <span style="font-size: 36px; font-weight: bold; color: #00a2ff;">Admin Login</span>
            </div>
        ''', unsafe_allowed_html=True)
        
        with st.container(border=True):
            st.markdown('<div class="panel-header">অ্যাডমিন প্যানেল প্রবেশ করুন</div>', unsafe_allowed_html=True)
            
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            
            st.markdown('<br>', unsafe_allowed_html=True)
            login_btn = st.button("🔓 লগইন করুন", use_container_width=True)
            
            if login_btn:
                # 📢 এখানে আপনার নিজের ইউজারনেম ও পাসওয়ার্ড সেট করতে পারেন
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড স্ক্রিন (লগইন সফল হলে)
# ==========================================
else:
    # ডাটাবেজ সেশন
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
    
    # লগআউট বাটন
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
        cust_select = st.text_input(t["c_name"], value=t["walking"])
        total_bill = st.number_input(t["total_bill"], min_value=0)
        
        if st.button(t["btn_inv"]):
            inv_num = f"INV-{int(datetime.datetime.now().timestamp())}"
            st.success(t["inv_gen"].format(inv_num))
            
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:20px; border-radius:10px; background-color:#fafafa; color: #333;">
                <h2>SRISTI COMPUTER REPAIR</h2>
                <hr>
                <p><b>Invoice No:</b> {inv_num}</p>
                <p><b>Customer:</b> {cust_select}</p>
                <table style="width:100%; border-collapse: collapse; margin-top:10px;">
                    <tr style="background-color:#eee;"><th style="padding:8px; text-align:left;">{t['desc']}</th><th style="padding:8px; text-align:right;">{t['total']}</th></tr>
                    <tr><td style="padding:8px;">{t['service_desc']}</td><td style="padding:8px; text-align:right;">{total_bill} BDT</td></tr>
                </table>
                <h3 style="text-align:right; margin-top:15px;">{t['total_paid'].format(total_bill)}</h3>
            </div>
            """, unsafe_allowed_html=True)
            st.info(t["tip"])
