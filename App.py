import streamlit as st
import pandas as pd
import datetime
import base64

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ইনিশিয়ালাইজেশন (স্থায়ী ডাটা সংরক্ষণ)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"ক্রমিক নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup & Cleaning", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200},
        {"ক্রমিক নং": 2, "কাস্টমার নাম": "Sristi", "কাজের বিবরণ": "Asus Motherboard Repair", "পরিমান": 1, "দর": 2500, "মোট টাকা": 2500, "আদায়": 1500, "বাকি": 1000}
    ]

if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"क्रमिक নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000},
        {"ক্রমিক নং": 2, "পণ্যের বিবরণ": "DDR4 8GB RAM", "পরিমান": 15, "দর": 2400, "মোট টাকা": 36000}
    ]

if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = [
        {"ক্রমিক নং": 1, "শিক্ষা প্রতিষ্ঠানের নাম": "Sreebardi Govt. College", "এন্ট্রি পাসওয়ার্ড": "sreebardi@2026", "কনফার্ম পাসওয়ার্ড": "board@xyz2026"}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🎨 গ্লোবাল থিম: ইনপুট বক্সের কালো রঙ দূর করে সাদা করার CSS
# ==========================================
custom_css = """
<style>
    /* মূল অ্যাপ এবং সাইডবার ব্যাকগ্রাউন্ড সম্পূর্ণ সাদা */
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* ✍️ ইনপুট ফিল্ডের কালো ব্যাকগ্রাউন্ড পরিবর্তন করে সাদা করার স্টাইল */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }
    
    /* ইনপুট বক্সের ভেতরের লেখার কালার কালো */
    div[data-baseweb="input"] input {
        color: #111111 !important;
        background-color: #ffffff !important;
    }
    
    /* টেক্সট ফিল্ড লেবেল কালো */
    .stTextInput label, .stNumberInput label, .stFileUploader label {
        color: #222222 !important;
        font-weight: bold;
    }
    
    /* 🔴 লগইন বাতন লাল বক্স এবং সাদা টেক্সট */
    div.stButton > button {
        background-color: #d60000 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background-color: #bd0000 !important;
        color: #ffffff !important;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.2) !important;
    }
    
    div.stSidebar div.stButton > button {
        text-align: left !important;
        margin-bottom: 12px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং
# ==========================================
if not st.session_state.logged_in:
    _, col_center, _ = st.columns([1, 1.4, 1])
    with col_center:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('''
            <div style="text-align: center; margin-bottom: 25px;">
                <div style="font-size: 40px; font-weight: 900; color: #111111; font-family: sans-serif;">
                    🔒 SM-TECH - <span style="color: #d60000;">Admin</span>
                </div>
                <div style="font-size: 38px; font-weight: 900; color: #d60000; margin-top: 5px; font-family: sans-serif;">
                    Login
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.container(border=False):
            st.markdown('<div style="font-size: 20px; font-weight: bold; text-align: center; color: #d60000; margin-bottom: 20px;">অ্যাডমিন প্যানেল প্রবেশ করুন</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            st.markdown('<br>', unsafe_allow_html=True)
            
            login_btn = st.button("🔒 লগইন করুন", use_container_width=True)
            if login_btn:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড স্ক্রিন
# ==========================================
else:
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 15px; margin-bottom: 15px; padding-left: 5px;">
                <span style="font-size: 32px; margin-right: 12px; color: #d60000;">⚙️</span>
                <span style="font-size: 30px; font-weight: 900; color: #d60000; letter-spacing: 0.5px;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h3 style='color:#d60000; font-size:20px; font-weight:bold; margin-left:5px; margin-bottom:15px;'>মেনু নির্বাচন করুন</h3>", unsafe_allow_html=True)
        
        if st.button("⬜  Dashboard", use_container_width=True):
            st.session_state.current_menu = "Dashboard"; st.rerun()
        if st.button("👥  Customer & Repair", use_container_width=True):
            st.session_state.current_menu = "Customer & Repair"; st.rerun()
        if st.button("📦  Stock product", use_container_width=True):
            st.session_state.current_menu = "Stock product"; st.rerun()
        if st.button("💵  Sell Invoice", use_container_width=True):
            st.session_state.current_menu = "Sell Invoice"; st.rerun()
        if st.button("🔐  Password Save", use_container_width=True):
            st.session_state.current_menu = "Password Save"; st.rerun()

    # --- ড্যাশবোর্ড মডিউল ---
    if st.session_state.current_menu == "Dashboard":
        st.title("🖥️  ড্যাশবোর্ড")
        st.subheader("এসএম-টেক কম্পিউটার ও আইটি সল্যুশন")
        st.write("---")
        
        col1, col2, col3 = st.columns(3)
        total_due_amount = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock_value = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        
        col1.metric("মোট বাকির হিসাব (কাস্টমার)", f"{len(st.session_state.customer_dues)} জন")
        col2.metric("মোট বাকি টাকা", f"{total_due_amount} BDT")
        col3.metric("স্টক পণ্যের মোট মূল্য", f"{total_stock_value} BDT")
        
        st.write("### 📑 কাস্টমার বাকির সংক্ষিপ্ত বিবরণ")
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True, hide_index=True)

    # --- কাস্টমার ও রিপেয়ার ---
    elif st.session_state.current_menu == "Customer & Repair":
        st.title("👥 কাস্টমার বাকির হিসাব ও রিপেয়ার")
        with st.form("Add Customer Due", clear_on_submit=True):
            st.write("### ➕ নতুন বাকির হিসাব যুক্ত করুন")
            c_name = st.text_input("কাস্টমার নাম")
            c_desc = st.text_input("কাজের বিবরণ")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1: c_qty = st.number_input("পরিমান", min_value=1, value=1, step=1)
            with col_c2: c_price = st.number_input("দর (টাকা)", min_value=0, value=0, step=50)
            with col_c3: c_paid = st.number_input("আদায় (টাকা)", min_value=0, value=0, step=50)
            submitted = st.form_submit_button(label="💾 লিস্টে যুক্ত করুন")
            
            if submitted:
                if c_name and c_desc:
                    total_amt = c_qty * c_price
                    due_amt = total_amt - c_paid
                    new_sl = len(st.session_state.customer_dues) + 1
                    st.session_state.customer_dues.append({
                        "ক্রমিক নং": new_sl, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
                        "পরিমান": c_qty, "দর": c_price, "মোট টাকা": total_amt, "আদায়": c_paid, "বাকি": due_amt
                    })
                    st.success(f"সফলভাবে {c_name} এর বাকির হিসাব যুক্ত হয়েছে!")
                    st.rerun()

        st.write("### 📋 বর্তমান কাস্টমার বাকির তালিকা")
        if st.session_state.customer_dues:
            st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True, hide_index=True)

    # --- স্টক পণ্য ---
    elif st.session_state.current_menu == "Stock product":
        st.title("📦 দোকানের স্টক পণ্য ম্যানেজমেন্ট")
        with st.form("Add Shop Stock", clear_on_submit=True):
            st.write("### ➕ নতুন স্টক পণ্য যুক্ত করুন")
            s_desc = st.text_input("পণ্যের বিবরণ / নাম")
            col_s1, col_s2 = st.columns(2)
            with col_s1: s_qty = st.number_input("পরিমান", min_value=1, value=1, step=1)
            with col_s2: s_price = st.number_input("দর (টাকা)", min_value=0, value=0, step=50)
            submitted_stock = st.form_submit_button(label="📥 স্টকে যুক্ত করুন")
            
            if submitted_stock:
                if s_desc:
                    total_stock_amt = s_qty * s_price
                    new_sl_stock = len(st.session_state.shop_stock) + 1
                    st.session_state.shop_stock.append({
                        "ক্রমিক নং": new_sl_stock, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": total_stock_amt
                    })
                    st.success(f"স্টকে সফলভাবে {s_desc} যুক্ত হয়েছে!")
                    st.rerun()

        st.write("### 📋 বর্তমানে মজুদ মালামালের তালিকা")
        if st.session_state.shop_stock:
            st.dataframe(pd.DataFrame(st.session_state.shop_stock), use_container_width=True, hide_index=True)

    # --- পাসওয়ার্ড সংরক্ষণ ---
    elif st.session_state.current_menu == "Password Save":
        st.title("🔐 শিক্ষা প্রতিষ্ঠানের পাসওয়ার্ড সংরক্ষণ ব্যবস্থা")
        with st.form("Add Institution Password", clear_on_submit=True):
            st.write("### ➕ নতুন শিক্ষা প্রতিষ্ঠানের পাসওয়ার্ড যুক্ত করুন")
            inst_name = st.text_input("শিক্ষা প্রতিষ্ঠানের নাম")
            col_p1, col_p2 = st.columns(2)
            with col_p1: entry_pass = st.text_input("এন্ট্রি পাসওয়ার্ড")
            with col_p2: confirm_pass = st.text_input("কনফার্ম পাসওয়ার্ড")
            submitted_pass = st.form_submit_button(label="💾 পাসওয়ার্ড সংরক্ষণ করুন")
            
            if submitted_pass:
                if inst_name and (entry_pass or confirm_pass):
                    new_sl_pass = len(st.session_state.saved_passwords) + 1
                    st.session_state.saved_passwords.append({
                        "ক্রমিক নং": new_sl_pass, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                    })
                    st.success("পাসওয়ার্ড সফলভাবে সংরক্ষিত হয়েছে!")
                    st.rerun()

        st.write("### 📋 সংরক্ষিত পাসওয়ার্ডের তালিকা")
        if st.session_state.saved_passwords:
            st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True, hide_index=True)

    # --- 🧾 সেল ইনভয়েস ---
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 পয়েন্ট অব সেল ও ইনভয়েস (A5 সাইজ)")
        
        uploaded_logo = st.file_uploader("🖼️ দোকানের লোগো আপলোড করুন", type=["png", "jpg", "jpeg"])
        logo_base64 = ""
        if uploaded_logo is not None:
            bytes_data = uploaded_logo.read()
            logo_base64 = f"data:image/png;base64,{base64.b64encode(bytes_data).decode()}"
        
        st.markdown("### 👤 Customer Info")
        col_in1, col_in2, col_in3 = st.columns([1.5, 2, 2])
        with col_in1: inv_custom_num = st.text_input("Invoice No", value="1001")
        with col_in2: cust_name = st.text_input("কাস্টমারের নাম", value="খুচরা কাস্টমার")
        with col_in3: cust_address = st.text_input("Address", value="Dhaka, Bangladesh")
            
        st.write("---")
        st.markdown("### 🛒 Add Items to Invoice")
        col_item1, col_item2, col_item3 = st.columns([3, 1, 1.5])
        with col_item1: prod_desc = st.text_input("Product Name / Description", placeholder="যেমন: DDR4 8GB RAM")
        with col_item2: prod_qty = st.number_input("QTY", min_value=1, value=1, step=1)
        with col_item3: prod_price = st.number_input("Unit Price (BDT)", min_value=0, value=500, step=50)
            
        if st.button("➕ Add Item to List", use_container_width=True):
            if prod_desc:
                st.session_state.invoice_items.append({
                    "Description": prod_desc, "Qty": prod_qty, "Price": prod_price, "Amount": prod_qty * prod_price
                })
                st.toast("আইটেম যুক্ত হয়েছে!")
                st.rerun()
                
        if st.session_state.invoice_items:
            st.dataframe(pd.DataFrame(st.session_state.invoice_items), use_container_width=True)
