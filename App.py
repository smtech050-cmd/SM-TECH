import streamlit as st
import datetime
import pandas as pd

# পেজ কনফিগারেশন এবং রেসপনসিভ লেআউট
st.set_page_config(page_title="SM-TECH POS & Inventory", page_icon="💻", layout="wide")

# ==========================================
# 💾 সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = [
        {"id": 1, "Date": "17-07-2026", "New Products": "SSD 120GB", "Quantity": 10, "Cost Price": 1200.0, "Sell Rate": 1600.0},
        {"id": 2, "Date": "18-07-2026", "New Products": "RAM 8GB DDR4", "Quantity": 6, "Cost Price": 1800.0, "Sell Rate": 2200.0},
    ]

if "sales_data" not in st.session_state:
    st.session_state["sales_data"] = []

if "customers_data" not in st.session_state:
    st.session_state["customers_data"] = []

if "editing_stock_id" not in st.session_state:
    st.session_state["editing_stock_id"] = None

if "menu_choice" not in st.session_state:
    st.session_state["menu_choice"] = "🏠 ড্যাশবোর্ড"

# ==========================================
# 🎨 গ্লোবাল ডার্ক নিয়ন সিএসএস (সাইডবার সম্পূর্ণ ডার্ক ফিক্স)
# ==========================================
st.markdown("""
    <style>
    /* 🌌 মেইন অ্যাপ ব্যাকগ্রাউন্ড */
    .stApp {
        background: radial-gradient(circle at center, #0a1931 0%, #020b1e 100%) !important;
        color: #ffffff !important;
    }
    
    /* 📱 সাইডবার কন্টেইনার সম্পূর্ণ ডার্ক ও টেক্সট সাদা */
    div[data-testid="stSidebar"] {
        background-color: #030f26 !important;
        border-right: 1px solid #00b4d8 !important;
    }
    
    div[data-testid="stSidebar"] h3, 
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    
    .main-title { 
        font-size: 32px; 
        font-weight: bold; 
        color: #ffffff; 
        text-align: center; 
        margin-bottom: 25px;
        text-shadow: 0 0 10px rgba(0, 180, 216, 0.5);
    }
    .neon-text {
        color: #00b4d8 !important;
        text-shadow: 0 0 8px rgba(0, 180, 216, 0.8);
    }
    
    .card-box { 
        background-color: #04143a; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #00b4d8; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
    }
    
    /* 📱 গ্লোবাল বাটন কাস্টমাইজেশন */
    div.stButton > button {
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 12px 15px !important;
        font-size: 15px !important;
        width: 100% !important;
        display: block !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.9 !important;
        transform: scale(0.98);
    }
    
    /* 🔐 নিয়ন লগইন ফর্ম স্টাইল */
    div[data-testid="stForm"] {
        border: 2px solid #00b4d8 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        background: #020f30 !important;
        box-shadow: 0px 0px 25px rgba(0, 180, 216, 0.25) !important;
    }
    
    div[data-testid="stForm"] label p {
        color: #ffffff !important;
    }
    
    div[data-testid="stForm"] input[type="text"], 
    div[data-testid="stForm"] input[type="password"] {
        background-color: #031640 !important;
        border: 1.5px solid #00b4d8 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 12px !important;
    }
    
    div[data-testid="stForm"] button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(90deg, #0077b6 0%, #00b4d8 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0px 4px 15px rgba(0, 180, 216, 0.4) !important;
    }
    
    div[data-testid="stForm"] button[data-testid="stFormSubmitButton"] p {
        color: #FFFFFF !important;
    }
    
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #04143a !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 লগইন স্ক্রিন (ADMIN LOGIN)
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='main-title'>🔒 SM-TECH - <span class='neon-text'>Admin Login</span></h2>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        with st.form("login_form"):
            st.markdown("<div style='text-align: center; font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 20px;'>অ্যাডমিন প্যানেলে প্রবেশ করুন</div>", unsafe_allow_html=True)
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            submit_login = st.form_submit_button("🔒 লগইন করুন")
            
            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state["logged_in"] = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড!")
    st.stop()

# ==========================================
# 📱 সাইডবার নেভিগেশন (সম্পূর্ণ ডার্ক সলিড বাটন)
# ==========================================
st.sidebar.markdown("### 💻 SM-TECH POS v2.0")
st.sidebar.markdown("---")

menu_items = [
    {"name": "🏠 ড্যাশবোর্ড", "color": "#1A479B"},
    {"name": "📦 স্টক ম্যানেজমেন্ট", "color": "#F39C12"},
    {"name": "🔍 পণ্য সার্চ", "color": "#00A651"},
    {"name": "🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট", "color": "#E31E24"},
    {"name": "👤 কাস্টমার ম্যানেজমেন্ট", "color": "#2980B9"},
    {"name": "📊 বিক্রয় রিপোর্ট", "color": "#16A085"},
    {"name": "💰 লাভ-লোকসানের হিসাব", "color": "#8E44AD"}
]

for item in menu_items:
    is_active = st.session_state["menu_choice"] == item["name"]
    # অ্যাক্টিভ হলে উজ্জ্বল সলিড কালার, না হলে ডার্ক ব্যাকগ্রাউন্ড
    btn_color = item["color"] if is_active else "#05183b"
    border_style = "1.5px solid #00b4d8" if is_active else "1px solid #1e293b"
    text_color = "#ffffff" if is_active else "#94a3b8"
    shadow_style = "0px 0px 12px rgba(0, 180, 216, 0.4)" if is_active else "none"
    
    st.sidebar.markdown(f"""
        <style>
        div[data-testid="stSidebar"] button[key="menu_{item['name']}"] {{
            background-color: {btn_color} !important;
            border: {border_style} !important;
            box-shadow: {shadow_style} !important;
        }}
        div[data-testid="stSidebar"] button[key="menu_{item['name']}"] p {{
            color: {text_color} !important;
            font-weight: bold !important;
        }}
        div[data-testid="stSidebar"] button[key="menu_{item['name']}"]:hover {{
            border-color: #00b4d8 !important;
            background-color: #082152 !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button(item["name"], key=f"menu_{item['name']}", use_container_width=True):
        st.session_state["menu_choice"] = item["name"]
        st.rerun()

st.sidebar.markdown("---")

# লগআউট বাটনের ডার্ক ও রেড মিক্স থিম
st.sidebar.markdown("""
    <style>
    div[data-testid="stSidebar"] button[key="logout_btn"] {
        background-color: #270b11 !important;
        border: 1px solid #ff4b4b !important;
    }
    div[data-testid="stSidebar"] button[key="logout_btn"] p {
        color: #ff8585 !important;
    }
    div[data-testid="stSidebar"] button[key="logout_btn"]:hover {
        background-color: #ff4b4b !important;
    }
    div[data-testid="stSidebar"] button[key="logout_btn"]:hover p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.sidebar.button("🔓 লগআউট", key="logout_btn", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

# কারেন্ট অ্যাক্টিভ মেনু ভিউ
menu_choice = st.session_state["menu_choice"]

# ==========================================
# 🏠 ড্যাশবোর্ড ভিউ
# ==========================================
if menu_choice == "🏠 ড্যাশবোর্ড":
    st.markdown("<h2 class='main-title'>🏠 বিজনেস ড্যাশবোর্ড</h2>", unsafe_allow_html=True)
    
    total_sales = sum([item["total"] for item in st.session_state["sales_data"]])
    total_profit = sum([item["profit"] for item in st.session_state["sales_data"]])
    total_items = len(st.session_state["stock_data"])
    total_qty = sum([item["Quantity"] for item in st.session_state["stock_data"]])
    total_cust = len(st.session_state["customers_data"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='card-box'><h4>💰 মোট বিক্রয়</h4><h2>৳ {total_sales:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card-box'><h4>📈 মোট লাভ</h4><h2>৳ {total_profit:,.2f}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card-box'><h4>📦 মোট প্রোডাক্ট</h4><h2>{total_items} টি ({total_qty} পিস)</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='card-box'><h4>👤 মোট কাস্টমার</h4><h2>{total_cust} জন</h2></div>", unsafe_allow_html=True)

# ==========================================
# 📦 স্টক ম্যানেজমেন্ট ভিউ
# ==========================================
elif menu_choice == "📦 স্টক ম্যানেজমেন্ট":
    st.markdown("<h2 class='main-title'>📦 স্টক মালের হিসাব</h2>", unsafe_allow_html=True)
    
    if st.session_state["editing_stock_id"] is not None:
        st.subheader("📝 পণ্য স্টক এডিট করুন")
        prod_id = st.session_state["editing_stock_id"]
        edit_item = next((item for item in st.session_state["stock_data"] if item["id"] == prod_id), None)
        edit_idx = next((idx for idx, item in enumerate(st.session_state["stock_data"]) if item["id"] == prod_id), -1)
                
        if edit_item:
            col1, col2, col3, col4 = st.columns(4)
            with col1: item_name = st.text_input("Product Name", value=edit_item["New Products"])
            with col2: quantity = st.number_input("Quantity", min_value=0, value=int(edit_item["Quantity"]))
            with col3: cost_price = st.number_input("Cost Price", min_value=0.0, value=float(edit_item["Cost Price"]))
            with col4: sell_rate = st.number_input("Sell Rate", min_value=0.0, value=float(edit_item["Sell Rate"]))
                
            btn_c1, btn_c2, _ = st.columns([2, 2, 8])
            with btn_c1:
                if st.button("💾 আপডেট সংরক্ষণ", key="save_update_btn"):
                    st.session_state["stock_data"][edit_idx] = {"id": prod_id, "Date": edit_item["Date"], "New Products": item_name, "Quantity": quantity, "Cost Price": cost_price, "Sell Rate": sell_rate}
                    st.session_state["editing_stock_id"] = None
                    st.success("স্টক সফলভাবে আপডেট হয়েছে!")
                    st.rerun()
            with btn_c2:
                if st.button("❌ বাতিল", key="cancel_btn"):
                    st.session_state["editing_stock_id"] = None
                    st.rerun()
    else:
        st.subheader("➕ নতুন পণ্য স্টক করুন")
        col1, col2, col3, col4 = st.columns(4)
        with col1: item_name = st.text_input("New Products (পণ্যের নাম)")
        with col2: quantity = st.number_input("Quantity (পরিমাণ)", min_value=0, value=0)
        with col3: cost_price = st.number_input("Cost Price (ক্রয় মূল্য)", min_value=0.0, value=0.0)
        with col4: sell_rate = st.number_input("Sell Rate (বিক্রয় মূল্য)", min_value=0.0, value=0.0)
            
        if st.button("স্টক আপডেট করুন", key="add_stock_btn"):
            if item_name and quantity > 0:
                current_date = datetime.date.today().strftime("%d-%m-%Y")
                new_id = max([i["id"] for i in st.session_state["stock_data"]], default=0) + 1
                st.session_state["stock_data"].append({"id": new_id, "Date": current_date, "New Products": item_name, "Quantity": quantity, "Cost Price": cost_price, "Sell Rate": sell_rate})
                st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
                st.rerun()
                
    st.markdown("---")
    st.subheader("📋 বর্তমান স্টক তালিকা")
    if st.session_state["stock_data"]:
        df_stock = pd.DataFrame(st.session_state["stock_data"]).drop(columns=["id"])
        st.dataframe(df_stock, use_container_width=True)
    else:
        st.info("স্টকে কোনো পণ্য নেই।")

# ==========================================
# 🔍 পণ্য সার্চ
# ==========================================
elif menu_choice == "🔍 পণ্য সার্চ":
    st.markdown("<h2 class='main-title'>🔍 পণ্য সার্চ ও অনুসন্ধান</h2>", unsafe_allow_html=True)
    search_query = st.text_input("পণ্যের নাম লিখে সার্চ করুন...")
    if search_query:
        results = [i for i in st.session_state["stock_data"] if search_query.lower() in i["New Products"].lower()]
        if results:
            df = pd.DataFrame(results).drop(columns=["id"])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("এই নামে কোনো পণ্য পাওয়া যায়নি।")

# ==========================================
# 🧾 ইনভয়েস প্রিন্ট
# ==========================================
elif menu_choice == "🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট":
    st.markdown("<h2 class='main-title'>🧾 ক্যাশ মেমো জেনারেটর</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Customer Name")
        customer_phone = st.text_input("Customer Phone")
        customer_address = st.text_input("Address")
    with col_b:
        invoice_no = st.text_input("Invoice No", value=f"SM-{datetime.datetime.now().strftime('%d%m%y%H%M%S')}")
        total_bill_input = st.number_input("Total Amount", min_value=0.0, value=0.0)

    if st.button("🛒 ইনভয়েস প্যাড প্রিন্ট করুন", key="invoice_btn"):
        if customer_name:
            st.success("ইনভয়েস প্যাড সফলভাবে জেনারেট হয়েছে!")
        else:
            st.error("দয়া করে কাস্টমারের নাম ইনপুট দিন।")
