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
# 🎨 শক্তিশালী কাস্টম সিএসএস (লগইন বক্স ও বাটন সম্পূর্ণ রঙিন)
# ==========================================
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1A479B; text-align: center; margin-bottom: 20px;}
    .card-box { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #1A479B; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    
    /* 📱 গ্লোবাল বাটন স্টাইল */
    div.stButton > button {
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 15px !important;
        font-size: 15px !important;
        width: 100% !important;
        display: block !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.9 !important;
        transform: scale(0.98);
    }
    
    /* 🔐 লগইন ফর্ম এবং ইনপুট বক্সের ব্যাকগ্রাউন্ড ও বর্ডার কালার ফিক্স */
    div[data-testid="stForm"] {
        border: 2px solid #1A479B !important;
        border-radius: 12px !important;
        padding: 25px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* ইনপুট ফিল্ডের ভেতরের সাধারণ ছাই কালার চেঞ্জ করে সুন্দর লাইট ব্লু করা */
    div[data-testid="stForm"] div[data-testid="stBaseTextInput"] aria-label,
    div[data-testid="stForm"] input[type="text"], 
    div[data-testid="stForm"] input[type="password"] {
        background-color: #EBF2FA !important;
        border: 2px solid #1A479B !important;
        border-radius: 8px !important;
        color: #1A479B !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    
    /* ইনপুট বক্সের কন্টেইনার ব্যাকগ্রাউন্ড ফিক্স */
    div[data-testid="stForm"] div[data-testid="stTextInput"] > div {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* 🟦 লগইন সাবমিট বাটনটিকে সম্পূর্ণ সলিড গাঢ় নীল করা */
    div[data-testid="stForm"] button[data-testid="stFormSubmitButton"] {
        background-color: #1A479B !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        padding: 12px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0px 4px 8px rgba(26, 71, 155, 0.3) !important;
    }
    
    div[data-testid="stForm"] button[data-testid="stFormSubmitButton"] p {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    
    @media (max-width: 768px) {
        .main-title { font-size: 22px; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 লগইন স্ক্রিন (ADMIN LOGIN)
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='main-title'>🔐 SM-TECH - Admin Login</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.3, 1])
    with col_l2:
        with st.form("login_form"):
            st.markdown("<div style='text-align: center; font-size: 18px; font-weight: bold; color: #1A479B; margin-bottom: 15px;'>অ্যাডমিন প্যানেলে প্রবেশ করুন</div>", unsafe_allow_html=True)
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("লগইন করুন")
            
            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state["logged_in"] = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড!")
    st.stop()

# ==========================================
# 📱 নেভিগেশন সাইডবার (রঙিন সলিড বক্স বোতাম)
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
    btn_color = item["color"]
    
    border_style = "2px solid #FFFFFF" if is_active else "none"
    shadow_style = "0px 4px 10px rgba(0,0,0,0.3)" if is_active else "none"
    
    st.sidebar.markdown(f"""
        <style>
        div[data-testid="stSidebar"] div.element-container:has(button[key="menu_{item['name']}"]) button,
        div[data-testid="stSidebar"] button[key="menu_{item['name']}"] {{
            background-color: {btn_color} !important;
            color: #FFFFFF !important;
            border: {border_style} !important;
            box-shadow: {shadow_style} !important;
        }}
        div[data-testid="stSidebar"] button[key="menu_{item['name']}"] p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button(
        item["name"], 
        key=f"menu_{item['name']}",
        use_container_width=True
    ):
        st.session_state["menu_choice"] = item["name"]
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown("""
    <style>
    div[data-testid="stSidebar"] button[key="logout_btn"] {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    div[data-testid="stSidebar"] button[key="logout_btn"] p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.sidebar.button("🔓 লগআউট", key="logout_btn", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

# কারেন্ট অ্যাক্টিভ মেনু
menu_choice = st.session_state["menu_choice"]

# ==========================================
# 🏠 ড্যাশবোর্ড (DASHBOARD)
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
        st.markdown(f"<div class='card-box'><h4>📦 মোট প্রোডাক্ট আইটেম</h4><h2>{total_items} টি ({total_qty} পিস)</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='card-box'><h4>👤 মোট কাস্টমার</h4><h2>{total_cust} জন</h2></div>", unsafe_allow_html=True)

# ==========================================
# 📦 স্টক ম্যানেজমেন্ট (STOCK MANAGEMENT)
# ==========================================
elif menu_choice == "📦 স্টক ম্যানেজমেন্ট":
    st.markdown("<h2 class='main-title'>📦 স্টক মালের হিসাব</h2>", unsafe_allow_html=True)
    
    if st.session_state["editing_stock_id"] is not None:
        st.subheader("📝 পণ্য স্টক এডিট করুন")
        prod_id = st.session_state["editing_stock_id"]
        
        edit_item = None
        edit_idx = -1
        for idx, item in enumerate(st.session_state["stock_data"]):
            if item["id"] == prod_id:
                edit_item = item
                edit_idx = idx
                break
                
        if edit_item:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                item_name = st.text_input("Product Name", value=edit_item["New Products"])
            with col2:
                quantity = st.number_input("Quantity", min_value=0, value=int(edit_item["Quantity"]))
            with col3:
                cost_price = st.number_input("Cost Price", min_value=0.0, value=float(edit_item["Cost Price"]))
            with col4:
                sell_rate = st.number_input("Sell Rate", min_value=0.0, value=float(edit_item["Sell Rate"]))
                
            btn_c1, btn_c2, _ = st.columns([2, 2, 8])
            with btn_c1:
                st.markdown("""<style>button[key="save_update_btn"] { background-color: #1A479B !important; color: white !important; }</style>""", unsafe_allow_html=True)
                if st.button("💾 আপডেট সংরক্ষণ করুন", key="save_update_btn"):
                    st.session_state["stock_data"][edit_idx] = {
                        "id": prod_id,
                        "Date": edit_item["Date"],
                        "New Products": item_name,
                        "Quantity": quantity,
                        "Cost Price": cost_price,
                        "Sell Rate": sell_rate
                    }
                    st.session_state["editing_stock_id"] = None
                    st.success("স্টক সফলভাবে আপডেট হয়েছে!")
                    st.rerun()
            with btn_c2:
                st.markdown("""<style>button[key="cancel_btn"] { background-color: #7F8C8D !important; color: white !important; }</style>""", unsafe_allow_html=True)
                if st.button("❌ বাতিল", key="cancel_btn"):
                    st.session_state["editing_stock_id"] = None
                    st.rerun()
    else:
        st.subheader("➕ নতুন পণ্য স্টক করুন")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            item_name = st.text_input("New Products (পণ্যের নাম)")
        with col2:
            quantity = st.number_input("Quantity (পরিমাণ)", min_value=0, value=0)
        with col3:
            cost_price = st.number_input("Cost Price (ক্রয় মূল্য)", min_value=0.0, value=0.0)
        with col4:
            sell_rate = st.number_input("Sell Rate (বিক্রয় মূল্য)", min_value=0.0, value=0.0)
            
        st.markdown("""
            <style>
            button[key="add_stock_btn"] { background-color: #1A479B !important; color: white !important; }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("স্টক আপডেট করুন", key="add_stock_btn"):
            if item_name and quantity > 0:
                current_date = datetime.date.today().strftime("%d-%m-%Y")
                new_id = max([i["id"] for i in st.session_state["stock_data"]], default=0) + 1
                st.session_state["stock_data"].append({
                    "id": new_id,
                    "Date": current_date,
                    "New Products": item_name,
                    "Quantity": quantity,
                    "Cost Price": cost_price,
                    "Sell Rate": sell_rate
                })
                st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
                st.rerun()
            else:
                st.error("দয়া করে পণ্যের নাম এবং সঠিক পরিমাণ লিখুন।")
                
    st.markdown("---")
    st.subheader("📋 বর্তমান স্টক তালিকা")
    
    if st.session_state["stock_data"]:
        h_sl, h_date, h_name, h_qty, h_cost, h_sell, h_action = st.columns([1, 2, 3, 2, 2, 2, 3])
        h_sl.markdown("**Sl.**")
        h_date.markdown("**Date**")
        h_name.markdown("**Product Name**")
        h_qty.markdown("**Quantity**")
        h_cost.markdown("**Cost Price**")
        h_sell.markdown("**Sell Rate**")
        h_action.markdown("**Actions**")
        st.markdown("<hr style='margin: 5px 0px;' />", unsafe_allow_html=True)
        
        for idx, item in enumerate(st.session_state["stock_data"]):
            c_sl, c_date, c_name, c_qty, c_cost, c_sell, c_action = st.columns([1, 2, 3, 2, 2, 2, 3])
            c_sl.write(idx + 1)
            c_date.write(item["Date"])
            c_name.write(item["New Products"])
            c_qty.write(item["Quantity"])
            c_cost.write(f"৳{item['Cost Price']}")
            c_sell.write(f"৳{item['Sell Rate']}")
            
            btn_edit, btn_del = c_action.columns(2)
            
            st.markdown(f"""
                <style>
                button[key="edit_{item['id']}"] {{ background-color: #2980B9 !important; color: white !important; }}
                button[key="del_{item['id']}"] {{ background-color: #C0392B !important; color: white !important; }}
                </style>
            """, unsafe_allow_html=True)
            
            if btn_edit.button("✏️ Edit", key=f"edit_{item['id']}"):
                st.session_state["editing_stock_id"] = item['id']
                st.rerun()
            if btn_del.button("🗑️ Delete", key=f"del_{item['id']}"):
                st.session_state["stock_data"].pop(idx)
                st.success("পণ্যটি সফলভাবে মুছে ফেলা হয়েছে।")
                st.rerun()
            st.markdown("<hr style='margin: 2px 0px; opacity: 0.3;' />", unsafe_allow_html=True)
    else:
        st.info("স্টকে কোনো পণ্য নেই।")

# ==========================================
# 🔍 পণ্য সার্চ ও অনুসন্ধান
# ==========================================
elif menu_choice == "🔍 পণ্য সার্চ":
    st.markdown("<h2 class='main-title'>🔍 পণ্য সার্চ ও অনুসন্ধান</h2>", unsafe_allow_html=True)
    search_query = st.text_input("পণ্যের নাম লিখে সার্চ করুন...")
    if search_query:
        results = [i for i in st.session_state["stock_data"] if search_query.lower() in i["New Products"].lower()]
        if results:
            df = pd.DataFrame(results).drop(columns=["id"])
            df.columns = ["তারিখ", "পণ্যের নাম", "পরিমাণ (Stock)", "ক্রয়মূল্য", "বিক্রয়মূল্য"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("এই নামে কোনো পণ্য পাওয়া যায়নি।")

# ==========================================
# 🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট
# ==========================================
elif menu_choice == "🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট":
    st.markdown("<h2 class='main-title'>🧾 ক্যাশ মেমো (হাতে লেখার জন্য খালি প্যাড)</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Customer Name (কাস্টমারের নাম)")
        customer_phone = st.text_input("Customer Phone (মোবাইল নম্বর)")
        customer_address = st.text_input("Address (ঠিকানা)")
    with col_b:
        invoice_no = st.text_input("Invoice No", value=f"SM-{datetime.datetime.now().strftime('%d%m%y%H%M%S')}")
        total_bill_input = st.number_input("Total Amount (মোট টাকার পরিমাণ - অপশনাল)", min_value=0.0, value=0.0)

    st.markdown("""<style>button[key="invoice_btn"] { background-color: #1A479B !important; color: white !important; }</style>""", unsafe_allow_html=True)
    if st.button("🛒 ইনভয়েস প্যাড জেনারেট ও প্রিন্ট করুন", key="invoice_btn"):
        if customer_name:
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            if not any(c['phone'] == customer_phone for c in st.session_state["customers_data"]):
                st.session_state["customers_data"].append({"name": customer_name, "phone": customer_phone, "address": customer_address})
            if total_bill_input > 0:
                st.session_state["sales_data"].append({"invoice_no": invoice_no, "customer": customer_name, "date": current_date, "total": total_bill_input, "profit": total_bill_input * 0.15, "discount": 0.0})
            
            table_rows_html = "".join([f"<tr style='height: 26px;'><td style='text-align:center; color:#dcdcdc;'>{i}</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>" for i in range(1, 9)])
            amount_display = f"{total_bill_input:.2f}" if total_bill_input > 0 else ""
            
            invoice_html = f"""
            <html><head><meta charset="UTF-8"><style>
                @page {{ size: 5in 7in; margin: 0.15in; }}
                body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; color: #000; background-color: #fff; }}
                .outer-border {{ border: 2px solid #1A479B; padding: 8px; border-radius: 4px; box-sizing: border-box; height: 6.7in; position: relative; }}
                .header-container {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; }}
                .logo-main {{ font-size: 24px; font-weight: 900; margin: 0; line-height: 1; font-style: italic; }}
                .logo-sm {{ color: #1A479B; }} .logo-tech {{ color: #E31E24; }}
                .sub-logo {{ font-size: 9.5px; font-weight: bold; color: #00A651; margin: 1px 0 0 0; }}
                .tagline {{ font-size: 8px; font-style: italic; color: #000; margin: 0; }}
                .owner-section {{ text-align: right; color: #1A479B; }}
                .owner-name {{ font-size: 11px; font-weight: bold; }}
                .owner-phone {{ font-size: 9px; font-weight: bold; margin: 0; }}
                .info-container {{ display: flex; justify-content: space-between; margin-top: 8px; }}
                .info-left {{ width: 65%; font-size: 10px; font-weight: bold; color: #1A479B; }}
                .bill-to-badge {{ background-color: #1A479B; color: white; display: inline-block; padding: 1px 4px; font-size: 9px; margin-right: 3px; }}
                .dots-line {{ color: #000; font-weight: normal; }}
                .info-right {{ width: 32%; font-size: 9px; font-weight: bold; color: #1A479B; }}
                .invoice-badge {{ background-color: #1A479B; color: white; text-align: center; padding: 2px 0; font-size: 11px; font-weight: bold; border-radius: 2px; width: 100%; margin-bottom: 3px; }}
                .product-table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
                .product-table th {{ background-color: #1A479B; color: white; border: 1.2px solid #1A479B; padding: 4px 2px; font-size: 9px; text-align: center; }}
                .product-table td {{ border-left: 1.2px solid #1A479B; border-right: 1.2px solid #1A479B; border-bottom: 1px solid #e2e2e2; font-size: 10px; }}
                .subtotal-box {{ background-color: #1A479B; color: white; text-align: center; font-size: 10px; font-weight: bold; padding: 4px; }}
                .subtotal-val {{ border: 1.2px solid #1A479B !important; text-align: center !important; font-size: 10px; font-weight: bold; }}
                .footer-container {{ display: flex; justify-content: space-between; align-items: flex-end; position: absolute; bottom: 12px; left: 8px; right: 8px; }}
                .words-text {{ font-size: 9px; font-weight: bold; color: #1A479B; }}
                .payment-box {{ border: 1.2px solid #1A479B; border-collapse: collapse; width: 160px; text-align: center; font-size: 8px; color: #1A479B; }}
                .payment-box td {{ border: 1px solid #1A479B; padding: 2px; }}
                .signature-section {{ text-align: center; color: #1A479B; font-size: 9px; font-weight: bold; width: 130px; }}
                .sig-line {{ border-top: 1.2px solid #1A479B; padding-top: 2px; }}
            </style></head><body>
            <div class="outer-border">
                <div class="header-container">
                    <div><h1 class="logo-main"><span class="logo-sm">SM-</span><span class="logo-tech">TECH</span></h1><p class="sub-logo">COMPUTER & IT SOLUTION</p><p class="tagline">Smart Technology-Trusted Service</p></div>
                    <div class="owner-section"><span class="owner-name">S.m. Ibrahim</span><br><span class="owner-title">Owner</span><p class="owner-phone">01940-556114<br>01810-499166</p></div>
                </div>
                <div class="info-container">
                    <div class="info-left">
                        <div style="display: flex; align-items: center;"><div class="bill-to-badge">Bill To</div>Name:<span class="dots-line">&nbsp;{customer_name}...................................</span></div>
                        <div>Address:<span class="dots-line">&nbsp;{customer_address}..........................................</span></div>
                    </div>
                    <div class="info-right"><div class="invoice-badge">INVOICE</div>Inv No: <span class="dots-line">{invoice_no[:12]}</span><br>Date: <span class="dots-line">{current_date}</span></div>
                </div>
                <table class="product-table">
                    <thead><tr><th style="width:7%;">S.L</th><th style="width:51%;">DESCRIPTION</th><th style="width:9%;">QTY</th><th style="width:15%;">U.PRICE</th><th style="width:18%;">AMOUNT</th></tr></thead>
                    <tbody>{table_rows_html}<tr style="height: 24px;"><td colspan="3"></td><td class="subtotal-box">SUB TOTAL</td><td class="subtotal-val">{amount_display}</td></tr></tbody>
                </table>
                <div class="footer-container">
                    <div><div class="words-text">In Words:<span style="color:#000; font-weight: normal;">&nbsp;...........................................</span></div><table class="payment-box"><tr><td colspan="4" style="background-color: #1A479B; color: white;">Payment Methods</td></tr><tr><td>Cash</td><td>Bkash</td><td>Nagad</td><td>Bank</td></tr></table></div>
                    <div class="signature-section"><div class="sig-line">Authorised Signature</div><div style="margin-top: 1px;">SM-TECH</div></div>
                </div>
            </div>
            <script>window.onload = function() {{ window.print(); }}</script>
            </body></html>
            """
            st.success("খালি ইনভয়েস প্যাড সফলভাবে জেনারেট হয়েছে!")
            st.download_button("📥 মেমো ডাউনলোড ও প্রিন্ট", data=invoice_html, file_name=f"Blank_Invoice_{invoice_no}.html", mime="text/html")
        else:
            st.error("দয়া করে কাস্টমারের নাম ইনপুট দিন।")

# ==========================================
# 👤 কাস্টমার ম্যানেজমেন্ট
# ==========================================
elif menu_choice == "👤 কাস্টমার ম্যানেজমেন্ট":
    st.markdown("<h2 class='main-title'>👤 কাস্টমার ম্যানেজমেন্ট</h2>", unsafe_allow_html=True)
    if st.session_state["customers_data"]:
        df_cust = pd.DataFrame(st.session_state["customers_data"])
        df_cust.columns = ["কাস্টমারের নাম", "মোবাইল নম্বর", "ঠিকানা"]
        st.dataframe(df_cust, use_container_width=True)
    else:
        st.info("এখনো কোনো কাস্টমার রেজিস্টার্ড হয়নি।")

# ==========================================
# 📊 বিক্রয় রিপোর্ট
# ==========================================
elif menu_choice == "📊 বিক্রয় রিপোর্ট":
    st.markdown("<h2 class='main-title'>📊 বিক্রয় রিপোর্ট তালিকা</h2>", unsafe_allow_html=True)
    if st.session_state["sales_data"]:
        df_sales = pd.DataFrame(st.session_state["sales_data"]).drop(columns=["profit"])
        df_sales.columns = ["ইনভয়েস নম্বর", "কাস্টমার নাম", "তারিখ", "মোট বিল (৳)", "ডিসকাউন্ট (৳)"]
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("কোনো বিক্রয়ের রেকর্ড পাওয়া যায়নি।")

# ==========================================
# 💰 লাভ-লোকসানের হিসাব
# ==========================================
elif menu_choice == "💰 লাভ-লোকসানের হিসাব":
    st.markdown("<h2 class='main-title'>💰 লাভ-লোকসানের হিসাব</h2>", unsafe_allow_html=True)
    if st.session_state["sales_data"]:
        df_p = pd.DataFrame(st.session_state["sales_data"])
        df_summary = df_p.groupby("date")[["total", "profit"]].sum().reset_index()
        df_summary.columns = ["তারিখ", "মোট বিক্রি (৳)", "নীট লাভ (৳)"]
        st.dataframe(df_summary, use_container_width=True)
        st.line_chart(df_summary.set_index("তারিখ"))
    else:
        st.info("হিসাব দেখানোর জন্য পর্যাপ্ত বিক্রয় ডাটা নেই।")
