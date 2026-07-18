import streamlit as st
import datetime
import pandas as pd

# পেজ কনফিগারেশন এবং রেসপনসিভ লেআউট (মোবাইল ও কম্পিউটার ফ্রেন্ডলি)
st.set_page_config(page_title="SM-TECH POS & Inventory", page_icon="💻", layout="wide")

# ==========================================
# 💾 সেশন স্টেট ইনিশিয়ালাইজেশন (ডাটাবেস বিকল্প)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "stock_data" not in st.session_state:
    # ডামি ডাটা (শুরু করার জন্য)
    st.session_state["stock_data"] = [
        {"id": 1, "Date": "17-07-2026", "New Products": "SSD 120GB", "Quantity": 10, "Cost Price": 1200.0, "Sell Rate": 1600.0},
        {"id": 2, "Date": "18-07-2026", "New Products": "RAM 8GB DDR4", "Quantity": 6, "Cost Price": 1800.0, "Sell Rate": 2200.0},
    ]

if "sales_data" not in st.session_state:
    st.session_state["sales_data"] = []

if "customers_data" not in st.session_state:
    st.session_state["customers_data"] = []

if "invoice_items" not in st.session_state:
    st.session_state["invoice_items"] = [{"description": "", "qty": 1, "uprice": 0.0}]

if "editing_stock_id" not in st.session_state:
    st.session_state["editing_stock_id"] = None

# সিএসএস স্টাইল (অ্যাপ্লিকেশন ইউজার ইন্টারফেস সুন্দর করার জন্য)
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1A479B; text-align: center; margin-bottom: 20px;}
    .card-box { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #1A479B; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    @media (max-width: 768px) {
        .main-title { font-size: 22px; }
        .stButton button { width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 লগইন স্ক্রিন (ADMIN LOGIN)
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<h2 class='main-title'>🔐 SM-TECH - Admin Login</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            username = st.text_input("Username (ইউজারনেম)")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password")
            submit_login = st.form_submit_button("লগইন করুন")
            
            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state["logged_in"] = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! (Default: admin / admin123)")
    st.stop()

# ==========================================
# 📱 নেভিগেশন সাইডবার মেনু
# ==========================================
st.sidebar.markdown("### 💻 SM-TECH POS v2.0")
menu_choice = st.sidebar.radio("মেনু নেভিগেশন:", [
    "🏠 ড্যাশবোর্ড",
    "📦 স্টক ম্যানেজমেন্ট",
    "🔍 পণ্য সার্চ",
    "🧾 ইনভয়েস তৈরি ও প্রিন্ট",
    "👤 কাস্টমার ম্যানেজমেন্ট",
    "📊 বিক্রয় রিপোর্ট",
    "💰 লাভ-লোকসানের হিসাব"
])

if st.sidebar.button("🔓 লগআউট"):
    st.session_state["logged_in"] = False
    st.rerun()

# ==========================================
# 🏠 ড্যাশবোর্ড (DASHBOARD)
# ==========================================
if menu_choice == "🏠 ড্যাশবোর্ড":
    st.markdown("<h2 class='main-title'>🏠 বিজনেস ড্যাশবোর্ড</h2>", unsafe_allow_html=True)
    
    # হিসাব নিকাশ
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
                if st.button("💾 আপডেট সংরক্ষণ করুন"):
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
                if st.button("❌ বাতিল"):
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
            
        if st.button("স্টক আপডেট করুন"):
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
# 🔍 পণ্য সার্চ (PRODUCT SEARCH)
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
# 🧾 ইনভয়েস তৈরি ও প্রিন্ট (INVOICE GENERATOR)
# ==========================================
elif menu_choice == "🧾 ইনভয়েস তৈরি ও প্রিন্ট":
    st.markdown("<h2 class='main-title'>🧾 ক্যাশ মেমো / ইনভয়েস জেনারেটর</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Customer Name (কাস্টমারের নাম)")
        customer_phone = st.text_input("Customer Phone (মোবাইল নম্বর)")
        customer_address = st.text_input("Address (ঠিকানা)")
    with col_b:
        invoice_no = st.text_input("Invoice No", value=f"SM-{datetime.datetime.now().strftime('%d%m%y%H%M%S')}")
    
    st.markdown("---")
    st.subheader("🛒 বিলের বিবরণ")
    
    prod_options = {p['New Products']: p for p in st.session_state["stock_data"] if p['Quantity'] > 0}
    
    updated_items = []
    for i, item in enumerate(st.session_state["invoice_items"]):
        col_desc, col_qty, col_uprice = st.columns([5, 2, 3])
        
        with col_desc:
            selected_prod = st.selectbox(f"পণ্যের নাম সিলেক্ট করুন #{i+1}", [""] + list(prod_options.keys()), key=f"inv_prod_{i}")
        with col_qty:
            max_q = prod_options[selected_prod]['Quantity'] if selected_prod else 100
            qty = st.number_input(f"QTY #{i+1}", min_value=1, max_value=max_q, value=1, key=f"inv_qty_{i}")
        with col_uprice:
            default_price = float(prod_options[selected_prod]['Sell Rate']) if selected_prod else 0.0
            uprice = st.number_input(f"মূল্য #{i+1}", min_value=0.0, value=default_price, key=f"inv_price_{i}")
            
        if selected_prod:
            updated_items.append({
                "prod_name": selected_prod,
                "qty": qty,
                "uprice": uprice,
                "cost_price": float(prod_options[selected_prod]['Cost Price'])
            })
            
    col_btn1, col_btn2, _ = st.columns([2, 2, 6])
    with col_btn1:
        if st.button("➕ নতুন রো যোগ করুন"):
            st.session_state["invoice_items"].append({"description": "", "qty": 1, "uprice": 0.0})
            st.rerun()
    with col_btn2:
        if st.button("❌ শেষ রো বাদ দিন") and len(st.session_state["invoice_items"]) > 1:
            st.session_state["invoice_items"].pop()
            st.rerun()
            
    discount = st.number_input("DISCOUNT (ডিসকাউন্ট টাকা)", min_value=0.0, value=0.0)
    
    if st.button("🛒 সেল সম্পন্ন ও ইনভয়েস প্রিন্ট করুন"):
        if customer_name and updated_items:
            sub_total = 0
            total_cost = 0
            table_rows_html = ""
            
            if not any(c['phone'] == customer_phone for c in st.session_state["customers_data"]):
                st.session_state["customers_data"].append({"name": customer_name, "phone": customer_phone, "address": customer_address})
            
            for index, item in enumerate(updated_items):
                amount = item["qty"] * item["uprice"]
                sub_total += amount
                total_cost += (item["qty"] * item["cost_price"])
                
                for p in st.session_state["stock_data"]:
                    if p["New Products"] == item["prod_name"]:
                        p["Quantity"] -= item["qty"]
                        break
                
                table_rows_html += f"""
                <tr style="height: 28px;">
                    <td style='text-align:center;'>{index+1}</td>
                    <td style='padding-left: 5px;'>{item['prod_name']}</td>
                    <td style='text-align:center;'>{item['qty']}</td>
                    <td style='text-align:center;'>{item['uprice']:.2f}</td>
                    <td style='text-align:center;'>{amount:.2f}</td>
                </tr>
                """
            
            # মেমোর আকৃতি ঠিক রাখতে ১২টি রো পূরণ করার জন্য ব্ল্যাঙ্ক রো জেনারেটর
            remaining_rows = max(0, 12 - len(updated_items))
            for i in range(remaining_rows):
                table_rows_html += """
                <tr style="height: 28px;">
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
                """
            
            total_bill = sub_total - discount
            total_profit = total_bill - total_cost
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            st.session_state["sales_data"].append({
                "invoice_no": invoice_no,
                "customer": customer_name,
                "date": current_date,
                "total": total_bill,
                "profit": total_profit,
                "discount": discount
            })
            
            amount_in_words = f"{int(total_bill)} Taka Only"
            
            # =========================================================
            # 🎨 পিক্সেল-পারফেক্ট ক্যাশ মেমো টেমপ্লেট (HTML/CSS)
            # =========================================================
            invoice_html = f"""
            <html>
            <head>
            <meta charset="UTF-8">
            <style>
                @page {{ size: 8.5in 11in; margin: 0.3in; }}
                body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 10px; color: #000; }}
                
                .outer-border {{ border: 2.5px solid #1A479B; padding: 15px; border-radius: 4px; box-sizing: border-box; min-height: 10.2in; position: relative; }}
                
                .header-container {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
                .logo-section {{ text-align: left; }}
                .logo-main {{ font-size: 38px; font-weight: 900; margin: 0; line-height: 1; font-style: italic; }}
                .logo-sm {{ color: #1A479B; }}
                .logo-tech {{ color: #E31E24; }}
                .sub-logo {{ font-size: 13.5px; font-weight: bold; color: #00A651; letter-spacing: 0.5px; margin: 2px 0 0 0; }}
                .tagline {{ font-size: 11px; font-style: italic; font-weight: 500; color: #000; margin: 1px 0 0 0; }}
                
                .owner-section {{ text-align: right; color: #1A479B; line-height: 1.2; }}
                .owner-name {{ font-size: 15px; font-weight: bold; }}
                .owner-title {{ font-size: 11px; color: #000; font-weight: bold; margin-bottom: 4px; }}
                .owner-phone {{ font-size: 13px; font-weight: bold; margin: 0; }}
                
                .info-container {{ display: flex; justify-content: space-between; margin-top: 15px; margin-bottom: 10px; }}
                .info-left {{ width: 68%; font-size: 13px; font-weight: bold; color: #1A479B; }}
                .bill-to-badge {{ background-color: #1A479B; color: white; display: inline-block; padding: 3px 8px; font-size: 12px; font-weight: bold; clip-path: polygon(0 0, 85% 0, 100% 100%, 0% 100%); margin-right: 5px; }}
                .dots-line {{ color: #000; font-weight: normal; font-size: 13px; }}
                
                .info-right {{ width: 28%; text-align: left; font-size: 13px; font-weight: bold; color: #1A479B; }}
                .invoice-badge {{ background-color: #1A479B; color: white; text-align: center; padding: 4px 0; font-size: 16px; font-weight: bold; letter-spacing: 1px; border-radius: 2px; margin-bottom: 6px; width: 100%; }}
                
                .product-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                .product-table th {{ background-color: #1A479B; color: white; border: 1.5px solid #1A479B; padding: 6px; font-size: 12px; font-weight: bold; text-align: center; }}
                .product-table td {{ border-left: 1.5px solid #1A479B; border-right: 1.5px solid #1A479B; border-bottom: 1px solid #dcdcdc; font-size: 12px; font-weight: bold; }}
                .product-table tr:last-child td {{ border-bottom: 1.5px solid #1A479B; }}
                
                .col-sl {{ width: 6%; text-align: center; }}
                .col-desc {{ width: 48%; }}
                .col-qty {{ width: 10%; text-align: center; }}
                .col-uprice {{ width: 16%; text-align: center; }}
                .col-amount {{ width: 20%; text-align: center; }}
                
                .subtotal-row td {{ border: none !important; }}
                .subtotal-box {{ background-color: #1A479B; color: white; text-align: center; font-size: 13px; font-weight: bold; padding: 7px; border: 1.5px solid #1A479B; border-radius: 0 0 0 8px; }}
                .subtotal-val {{ border: 1.5px solid #1A479B !important; text-align: center !important; font-size: 13px; font-weight: bold; background: #fff; }}
                
                .footer-container {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 30px; position: absolute; bottom: 25px; left: 15px; right: 15px; }}
                .words-text {{ font-size: 12px; font-weight: bold; color: #1A479B; margin-bottom: 15px; }}
                
                .payment-box {{ border: 1.5px solid #1A479B; border-collapse: collapse; width: 220px; text-align: center; font-size: 11px; font-weight: bold; color: #1A479B; }}
                .payment-box td {{ border: 1px solid #1A479B; padding: 5px; }}
                
                .signature-section {{ text-align: center; color: #1A479B; font-size: 11px; font-weight: bold; line-height: 1.3; width: 200px; }}
                .sig-line {{ border-top: 1.5px solid #1A479B; padding-top: 3px; font-size: 11px; }}
                .sig-company {{ font-size: 9px; font-weight: normal; color: #1A479B; }}
            </style>
            </head>
            <body>
            <div class="outer-border">
                
                <!-- ১. হেডার সেকশন -->
                <div class="header-container">
                    <div class="logo-section">
                        <h1 class="logo-main"><span class="logo-sm">SM-</span><span class="logo-tech">TECH</span></h1>
                        <p class="sub-logo">COMPUTER & IT SOLUTION</p>
                        <p class="tagline">Smart Technology-Trusted Service</p>
                    </div>
                    <div class="owner-section">
                        <span class="owner-name">S.m. Ibrahim</span><br>
                        <span class="owner-title">Owner</span><br>
                        <p class="owner-phone">01940-556114<br>01810-499166</p>
                    </div>
                </div>
                
                <!-- ২. কাস্টমার ইনফো সেকশন -->
                <div class="info-container">
                    <div class="info-left">
                        <div style="margin-bottom: 6px; display: flex; align-items: center;">
                            <div class="bill-to-badge">Bill To</div>
                            <span style="color:#1A479B;">Name:</span>
                            <span class="dots-line">&nbsp;{customer_name}....................................................................................</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="color:#1A479B;">Address:</span>
                            <span class="dots-line">&nbsp;{customer_address}..........................................................................................</span>
                        </div>
                        <div>
                            <span class="dots-line">.......................................................................................................................</span>
                        </div>
                    </div>
                    <div class="info-right">
                        <div class="invoice-badge">INVOICE</div>
                        <span style="color:#1A479B;">Invoice No:</span> <span class="dots-line">{invoice_no}</span><br>
                        <div style="margin-top: 4px;">
                            <span style="color:#1A479B;">Date:</span> <span class="dots-line">{current_date}.......................</span>
                        </div>
                    </div>
                </div>
                
                <!-- ৩. প্রোডাক্ট আইটেম টেবিল -->
                <table class="product-table">
                    <thead>
                        <tr>
                            <th class="col-sl">S.L</th>
                            <th class="col-desc">DESCRIPTION</th>
                            <th class="col-qty">QTY</th>
                            <th class="col-uprice">U.PRICE</th>
                            <th class="col-amount">AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_html}
                        <tr class="subtotal-row" style="height: 32px;">
                            <td colspan="3"></td>
                            <td class="subtotal-box">SUB TOTAL</td>
                            <td class="subtotal-val">{total_bill:.2f}</td>
                        </tr>
                    </tbody>
                </table>
                
                <!-- ৪. ফুটার ও পেমেন্ট গেটওয়ে -->
                <div class="footer-container">
                    <div>
                        <div class="words-text">Amount In Words:<span style="color:#000; font-weight: normal;">&nbsp;{amount_in_words}............................................................</span></div>
                        
                        <table class="payment-box">
                            <tr>
                                <td colspan="4" style="background-color: #1A479B; color: white; border: none; padding: 2px; font-weight: bold;">Payment Methods</td>
                            </tr>
                            <tr>
                                <td>Cash</td>
                                <td>Bkash</td>
                                <td>Nagad</td>
                                <td>Bank</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div class="signature-section">
                        <div class="sig-line">Authorised Signature</div>
                        <div style="font-size: 11px; font-weight: bold; margin-top: 1px;">SM-TECH</div>
                        <div class="sig-company">Computer & IT Solutions</div>
                    </div>
                </div>
                
            </div>
            
            <script>
                window.onload = function() {{ 
                    window.print(); 
                }}
            </script>
            </body>
            </html>
            """
            st.success("বিক্রয় সফল হয়েছে এবং স্টক আপডেট করা হয়েছে!")
            st.download_button("📥 মেমো ডাউনলোড ও প্রিন্ট", data=invoice_html, file_name=f"Invoice_{invoice_no}.html", mime="text/html")
        else:
            st.error("কাস্টমারের নাম এবং কমপক্ষে ১টি প্রোডাক্ট সিলেক্ট করুন।")

# ==========================================
# 👤 কাস্টমার ম্যানেজমেন্ট (CUSTOMER MANAGEMENT)
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
# 📊 বিক্রয় রিপোর্ট (SALES REPORT)
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
# 💰 লাভ-লোকসানের হিসাব (PROFIT LOSS)
# ==========================================
elif menu_choice == "💰 লাভ-লোকসানের হিসাব":
    st.markdown("<h2 class='main-title'>💰 লাভ-লোকসানের নিখুঁত হিসাব</h2>", unsafe_allow_html=True)
    
    if st.session_state["sales_data"]:
        df_p = pd.DataFrame(st.session_state["sales_data"])
        df_summary = df_p.groupby("date")[["total", "profit"]].sum().reset_index()
        df_summary.columns = ["তারিখ", "মোট বিক্রি (৳)", "নীট লাভ (৳)"]
        st.dataframe(df_summary, use_container_width=True)
        
        st.markdown("### 📈 বিক্রয় বনাম লাভ গ্রাফ চিত্র")
        st.line_chart(df_summary.set_index("তারিখ"))
    else:
        st.info("হিসাব দেখানোর জন্য পর্যাপ্ত বিক্রয় ডাটা নেই।")
