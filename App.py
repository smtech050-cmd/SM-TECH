import streamlit as st
import pandas as pd
import datetime
import base64
import streamlit.components.v1 as components

# PWA ম্যানিফেস্ট ও সার্ভিস ওয়ার্কার লিংক ইনজেক্ট করা
components.html(
    """
    <script>
        // manifest.json লিংক যুক্ত করা
        var link = document.createElement('link');
        link.rel = 'manifest';
        link.href = 'https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/manifest.json';
        document.head.appendChild(link);

        // Service Worker রেজিস্টার করা
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/sw.js')
            .then(function(reg) {
                console.log('Service Worker Registered!', reg);
            }).catch(function(err) {
                console.log('Service Worker Failed!', err);
            });
        }
    </script>
    """,
    height=0,
)
# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ইনিশিয়ালাইজেশন
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
# 🎨 গ্লোবাল থিম: ডার্ক মোড ওভাররাইড করে ইনপুট বক্স সাদা করার ১০০% কার্যকরী CSS
# ==========================================
custom_css = """
<style>
    /* মূল অ্যাপ ব্যাকগ্রাউন্ড সম্পূর্ণ সাদা */
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    
    /* ✍️ ইনপুট বক্স ১০০% সাদা করার জন্য স্ট্রং CSS */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stTextInput div[data-baseweb="input"] {
        border: 1px solid #cccccc !important;
    }

    /* ইনপুট বক্সের ভেতরের লেখার কালার কালো */
    .stTextInput input, 
    .stNumberInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* প্লেসহোল্ডার কালার */
    input::placeholder {
        color: #777777 !important;
        -webkit-text-fill-color: #777777 !important;
    }

    /* পাসওয়ার্ড দেখার চোখের আইকন কালো করা */
    div[data-baseweb="input"] svg {
        fill: #333333 !important;
        color: #333333 !important;
    }
    
    /* টেক্সট ফিল্ড লেবেল কালো */
    .stTextInput label, .stNumberInput label {
        color: #222222 !important;
        font-weight: bold !important;
    }
    
    /* 🔴 লগইন ও সাইডবার বাটন লাল বক্স এবং সাদা টেক্সট */
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
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* বাটনের ভিতরের টেক্সট নিশ্চিত সাদা করার জন্য */
    div.stButton p {
        color: #ffffff !important; 
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

    # ড্যাশবোর্ড মডিউল
    if st.session_state.current_menu == "Dashboard":
        st.title("🖥️  ড্যাশবোর্ড")
        st.write("---")
        col1, col2, col3 = st.columns(3)
        total_due = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        col1.metric("মোট কাস্টমার", f"{len(st.session_state.customer_dues)} জন")
        col2.metric("মোট বাকি টাকা", f"{total_due} BDT")
        col3.metric("স্টক পণ্যের মূল্য", f"{total_stock} BDT")
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
