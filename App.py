import streamlit as st
import pandas as pd
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide", page_icon="💻")

# ==========================================
# 🔐 সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"ক্রমিক নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200}
    ]

if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"ক্রমিক নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000}
    ]

if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = [
        {"ক্রমিক নং": 1, "শিক্ষা প্রতিষ্ঠানের নাম": "Sreebardi Govt. College", "এন্ট্রি পাসওয়ার্ড": "sreebardi@2026", "কনফার্ম পাসওয়ার্ড": "board@xyz2026"}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🎨 ফুল-স্ক্রিন মোড ও রেসপনসিভ CSS
# ==========================================
custom_css = """
<style>
    /* 📱 মোবাইল ও সব ডিভাইসে ফুল স্ক্রিন করার মূল প্যাচ */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* অ্যাপের মূল ব্যাকগ্রাউন্ড */
    [data-testid="stAppViewContainer"] {
        background-color: #080d1a !important;
        background-image: radial-gradient(circle at 50% 20%, rgba(0, 102, 255, 0.15) 0%, transparent 50%) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0b1426 !important;
        border-right: 1px solid #1e2e4a !important;
    }

    /* Streamlit Header এবং Footer লুকিয়ে রাখা */
    header[data-testid="stHeader"], footer {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* ✍️ ইনপুট বক্সের ফুল-উইডথ ও রেসপনসিভ ডিজাইন */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"] {
        background-color: #0b1528 !important;
        border-radius: 12px !important;
        border: 1.5px solid #1e3a5f !important;
        width: 100% !important;
    }

    .stTextInput input, .stNumberInput input {
        color: #38bdf8 !important;
        background-color: #0b1528 !important;
        -webkit-text-fill-color: #38bdf8 !important;
        padding: 12px !important;
        font-size: 15px !important;
    }
    
    /* প্লেসহোল্ডার টেক্সট */
    input::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
    }

    /* আইকন ফিল্ড */
    div[data-baseweb="input"] svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
    }
    
    /* ইনপুট লেবেল */
    .stTextInput label, .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* 🔴 বাটন ফুল-উইডথ এবং গ্লোয়িং ফিল্টার */
    div.stButton > button {
        background: linear-gradient(90deg, #0052cc 0%, #0066ff 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.95 !important;
        box-shadow: 0 6px 20px rgba(0, 102, 255, 0.6) !important;
    }
    
    div.stButton p {
        color: #ffffff !important; 
    }

    /* সাইডবার বাটন */
    div.stSidebar div.stButton > button {
        text-align: left !important;
        margin-bottom: 8px !important;
        border-radius: 10px !important;
        background: #0f1c35 !important;
        border: 1px solid #1e3a5f !important;
        box-shadow: none !important;
    }

    /* লোগো কনটেইনার */
    .logo-img-wrapper {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: #ffffff;
        padding: 3px;
        box-shadow: 0 0 20px rgba(0, 102, 255, 0.5);
        border: 2px solid #0066ff;
        margin: 0 auto 12px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .logo-img-wrapper img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
    }
    
    /* টেবিল ডিজাইন */
    div[data-testid="stDataFrame"] {
        background-color: #0d1629 !important;
        border: 1px solid #1e2e4a !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🛑 ১. ফুল স্ক্রিন লগইন লেআউট
# ==========================================
if not st.session_state.logged_in:
    # মোবাইল এবং ডেসktop উভয়ের জন্য মার্জিন অ্যাডজাস্ট করা কলাম
    col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
    
    with col2:
        st.markdown('''
            <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
                <div class="logo-img-wrapper">
                    <img src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH Logo">
                </div>
                <div style="font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;">
                    Welcome to <span style="color: #1e88e5;">SM-TECH</span>
                </div>
                <div style="font-size: 11px; color: #94a3b8; letter-spacing: 1.2px; font-weight: 600; margin-top: 3px;">
                    COMPUTER & IT SOLUTIONS
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        username = st.text_input("Username (ইউজারনেম)", placeholder="আপনার মোবাইল নম্বর / ইমেইল")
        password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড দিন")
        st.markdown('<br>', unsafe_allow_html=True)
        
        login_btn = st.button("➔ লগইন করুন", use_container_width=True)
        if login_btn:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("লগইন সফল হয়েছে!")
                st.rerun()
            else:
                st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড
# ==========================================
else:
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 15px;">
                <span style="font-size: 28px; margin-right: 10px; color: #38bdf8;">💻</span>
                <span style="font-size: 22px; font-weight: 900; color: #ffffff;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h4 style='color:#38bdf8; margin-bottom:15px;'>মেনু নির্বাচন করুন</h4>", unsafe_allow_html=True)
        
        if st.button("⬜ Dashboard", use_container_width=True):
            st.session_state.current_menu = "Dashboard"; st.rerun()
        if st.button("👥 Customer & Repair", use_container_width=True):
            st.session_state.current_menu = "Customer & Repair"; st.rerun()
        if st.button("📦 Stock product", use_container_width=True):
            st.session_state.current_menu = "Stock product"; st.rerun()
        if st.button("💵 Sell Invoice", use_container_width=True):
            st.session_state.current_menu = "Sell Invoice"; st.rerun()
        if st.button("🔐 Password Save", use_container_width=True):
            st.session_state.current_menu = "Password Save"; st.rerun()

    # ড্যাশবোর্ড মডিউল
    if st.session_state.current_menu == "Dashboard":
        st.title("🖥️ ড্যাশবোর্ড")
        st.write("---")
        col1, col2, col3 = st.columns(3)
        total_due = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        col1.metric("মোট কাস্টমার", f"{len(st.session_state.customer_dues)} জন")
        col2.metric("মোট বাকি টাকা", f"{total_due} BDT")
        col3.metric("স্টক পণ্যের মূল্য", f"{total_stock} BDT")
        st.write("<br>", unsafe_allow_html=True)
        st.subheader("কাস্টমার ডিরেক্টরি & রিসেন্ট এন্ট্রি")
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True)

    # কাস্টমার ও রিপেয়ার
    elif st.session_state.current_menu == "Customer & Repair":
        st.title("👥 কাস্টমার বাকির হিসাব")
        with st.form("Add Customer Due", clear_on_submit=True):
            c_name = st.text_input("কাস্টমার নাম")
            c_desc = st.text_input("কাজের বিবরণ")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1: c_qty = st.number_input("পরিমান", min_value=1, value=1)
            with col_c2: c_price = st.number_input("দর (টাকা)", min_value=0, value=0)
            with col_c3: c_paid = st.number_input("আদায় (টাকা)", min_value=0, value=0)
            if st.form_submit_button("💾 লিস্টে যুক্ত করুন") and c_name:
                st.session_state.customer_dues.append({
                    "ক্রমিক নং": len(st.session_state.customer_dues) + 1, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
                    "পরিমান": c_qty, "দর": c_price, "মোট টাকা": c_qty*c_price, "আদায়": c_paid, "বাকি": (c_qty*c_price)-c_paid
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True)

    # স্টক পণ্য
    elif st.session_state.current_menu == "Stock product":
        st.title("📦 স্টক পণ্য ম্যানেজমেন্ট")
        with st.form("Add Shop Stock", clear_on_submit=True):
            s_desc = st.text_input("পণ্যের বিবরণ / নাম")
            col_s1, col_s2 = st.columns(2)
            with col_s1: s_qty = st.number_input("পরিমান", min_value=1, value=1)
            with col_s2: s_price = st.number_input("দর (টাকা)", min_value=0, value=0)
            if st.form_submit_button("📥 স্টকে যুক্ত করুন") and s_desc:
                st.session_state.shop_stock.append({
                    "ক্রমিক নং": len(st.session_state.shop_stock) + 1, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": s_qty*s_price
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.shop_stock), use_container_width=True)

    # পাসওয়ার্ড সংরক্ষণ
    elif st.session_state.current_menu == "Password Save":
        st.title("🔐 পাসওয়ার্ড সংরক্ষণ")
        with st.form("Add Password", clear_on_submit=True):
            inst_name = st.text_input("প্রতিষ্ঠানের নাম")
            col_p1, col_p2 = st.columns(2)
            with col_p1: entry_pass = st.text_input("এন্ট্রি পাসওয়ার্ড")
            with col_p2: confirm_pass = st.text_input("কনফার্ম পাসওয়ার্ড")
            if st.form_submit_button("💾 সংরক্ষণ করুন") and inst_name:
                st.session_state.saved_passwords.append({
                    "ক্রমিক নং": len(st.session_state.saved_passwords) + 1, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True)

    # সেল ইনভয়েস
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 পয়েন্ট অব সেল ও ইনভয়েস")
        col_in1, col_in2, col_in3 = st.columns([1.5, 2, 2])
        with col_in1: inv_custom_num = st.text_input("Invoice No", value="1001")
        with col_in2: cust_name = st.text_input("কাস্টমারের নাম", value="খুচরা কাস্টমার")
        with col_in3: cust_address = st.text_input("Address", value="Dhaka, Bangladesh")
            
        col_item1, col_item2, col_item3 = st.columns([3, 1, 1.5])
        with col_item1: prod_desc = st.text_input("Product Name / Description")
        with col_item2: prod_qty = st.number_input("QTY", min_value=1, value=1)
        with col_item3: prod_price = st.number_input("Unit Price", min_value=0, value=500)
            
        if st.button("➕ Add Item", use_container_width=True) and prod_desc:
            st.session_state.invoice_items.append({
                "Description": prod_desc, "Qty": prod_qty, "Price": prod_price, "Amount": prod_qty * prod_price
            })
            st.rerun()
                
        if st.session_state.invoice_items:
            st.dataframe(pd.DataFrame(st.session_state.invoice_items), use_container_width=True)
            if st.button("🗑️ Clear All"):
                st.session_state.invoice_items = []
                st.rerun()
