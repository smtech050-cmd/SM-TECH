import streamlit as st
import datetime
import base64
import pandas as pd

# পেজ কনফিগারেশন এবং রেসপনসিভ লেআউট (মোবাইল ও কম্পিউটার ফ্রেন্ডলি)
st.set_page_config(page_title="SM-TECH POS & Inventory", page_icon="💻", layout="wide")

# ==========================================
# 💾 সেশন স্টেট ইনিশিয়ালাইজেশন (ডাটাবেস বিকল্প)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "stock_data" not in st.session_state:
    # ডামি ডাটা
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

# সিএসএস স্টাইল (মোবাইল ও কম্পিউটারের স্ক্রিন সুন্দর দেখানোর জন্য)
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #0a4da2; text-align: center; margin-bottom: 20px;}
    .card-box { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #0a4da2; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
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
            password = st.text_input("Password (পাসওয়ার্ড)", type="password")
            submit_login = st.form_submit_button("লগইন করুন")
            
            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state["logged_in"] = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! (Default: admin / admin123)")
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
        
        # আইটেম খুঁজে বের করা
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
                    st.success("স্টক সফলভাবে আপডেট হয়েছে!")
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
                st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
                st.rerun()
            else:
                st.error("দয়া করে পণ্যের নাম এবং সঠিক পরিমাণ লিখুন।")
                
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
                st.success("পণ্যটি সফলভাবে মুছে ফেলা হয়েছে।")
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
            df.columns = ["তারিখ", "পণ্যের নাম", "পরিমাণ (Stock)", "ক্রয়মূল্য", "বিক্রয়মূল্য"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("এই নামে কোনো পণ্য পাওয়া যায়নি।")

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
    
    # স্টকের পণ্যের ড্রপডাউন লিস্ট
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
    
    if st.button("🛒 সেল সম্পন্ন ও ইনভয়েস প্রিন্ট করুন"):
        if customer_name and updated_items:
            sub_total = 0
            total_cost = 0
            table_rows_html = ""
            
            # কাস্টমার সেভ
            if not any(c['phone'] == customer_phone for c in st.session_state["customers_data"]):
                st.session_state["customers_data"].append({"name": customer_name, "phone": customer_phone, "address": customer_address})
            
            for index, item in enumerate(updated_items):
                amount = item["qty"] * item["uprice"]
                sub_total += amount
                total_cost += (item["qty"] * item["cost_price"])
                
                # স্টক আপডেট (Quantity মাইনাস করা)
                for p in st.session_state["stock_data"]:
                    if p["New Products"] == item["prod_name"]:
                        p["Quantity"] -= item["qty"]
                        break
                
                table_rows_html += f"""
                <tr>
                    <td style='text-align:center;'>{index+1}</td>
                    <td>{item['prod_name']}</td>
                    <td style='text-align:center;'>{item['qty']}</td>
                    <td style='text-align:right;'>{item['uprice']}</td>
                    <td style='text-align:right;'>{amount}</td>
                </tr>
                """
            
            total_bill = sub_total - discount
            total_profit = total_bill - total_cost
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # সেলস রিপোর্টে ডাটা সেভ
            st.session_state["sales_data"].append({
                "invoice_no": invoice_no,
                "customer": customer_name,
                "date": current_date,
                "total": total_bill,
                "profit": total_profit,
                "discount": discount
            })
            
            # ৫x৭ ইঞ্চি ক্যাш মেমো প্রিন্ট টেমপ্লেট
            invoice_html = f"""
            <html><head><style>
                @page {{ size: 5in 7in; margin: 0; }}
                body {{ font-family: Arial; padding: 15px; }}
                .header {{ text-align: center; color: #0a4da2; }}
                .table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                .table th, .table td {{ border: 1px solid #0a4da2; padding: 5px; font-size: 11px; }}
                .table th {{ background: #0a4da2; color: white; }}
            </style></head>
            <body>
                <div class="header">
                    <h2>SM-TECH</h2>
                    <p style="font-size:9px; margin:-10px 0 10px 0;">COMPUTER & IT SOLUTION</p>
                </div>
                <p style="font-size:11px;"><b>Memo:</b> {invoice_no} | <b>Date:</b> {current_date}<br>
                <b>Client:</b> {customer_name} ({customer_phone})</p>
                <table class="table">
                    <thead><tr><th>SL</th><th>Description</th><th>Qty</th><th>Price</th><th>Total</th></tr></thead>
                    <tbody>{table_rows_html}</tbody>
                </table>
                <h4 style="text-align:right;">Grand Total: ৳{total_bill}</h4>
                <script>window.onload = function() {{ window.print(); }}</script>
            </body></html>
            """
            st.success("বিক্রয় সফল হয়েছে এবং স্টক আপডেট করা হয়েছে!")
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
        st.info("এখনো কোনো কাস্টমার রেজিস্টার্ড হয়নি।")

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
        st.info("কোনো বিক্রয়ের রেকর্ড পাওয়া যায়নি।")

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
        
        st.markdown("### 📈 বিক্রয় বনাম লাভ গ্রাফ চিত্র")
        st.line_chart(df_summary.set_index("তারিখ"))
    else:
        st.info("হিসাব দেখানোর জন্য পর্যাপ্ত বিক্রয় ডাটা নেই।")
