import streamlit as st
import mysql.connector
import datetime
import pandas as pd
import base64

# পেজ কনফিগারেশন এবং মোবাইল ফ্রেন্ডলি রেসপনসিভ লেআউট
st.set_page_config(page_title="SM-TECH POS & Inventory", page_icon="💻", layout="wide")

# ==========================================
# 🔌 MYSQL ডাটাবেস কানেকশন (আপনার ডাটাবেস তথ্য এখানে দিন)
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # আপনার হোস্টিং হোস্ট (যেমন: localhost)
        user="root",            # আপনার ডাটাবেস ইউজারনেম
        password="",            # আপনার ডাটাবেস পাসওয়ার্ড
        database="sm_tech_db"   # আপনার ডাটাবেস নাম
    )

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ম্যানেজমেন্ট
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "editing_stock_id" not in st.session_state:
    st.session_state["editing_stock_id"] = None
if "invoice_items" not in st.session_state:
    st.session_state["invoice_items"] = [{"description": "", "qty": 1, "uprice": 0}]

# সিএসএস স্টাইল (মোবাইল ও কম্পিউটারের স্ক্রিন সুন্দর দেখানোর জন্য)
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #0a4da2; text-align: center; margin-bottom: 20px;}
    .card-box { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #0a4da2; margin-bottom: 15px; }
    @media (max-width: 768px) {
        .main-title { font-size: 22px; }
        .stButton button { width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# লগইন স্ক্রিন
if not st.session_state["logged_in"]:
    st.markdown("<h2 class='main-title'>🔐 SM-TECH - Admin Login</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            username = st.text_input("Username (ইউজারনেম)")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password")
            submit_login = st.form_submit_button("লগইন করুন")
            
            if submit_login:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
                    user = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if user:
                        st.session_state["logged_in"] = True
                        st.success("লগইন সফল হয়েছে!")
                        st.rerun()
                    else:
                        st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড!")
                except Exception as e:
                    st.error("ডাটাবেস কানেক্ট করা যায়নি। দয়া করে আপনার MySQL সার্ভার চালু করুন।")
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
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # মোট বিক্রি ও মোট লাভ হিসাব
    cursor.execute("SELECT SUM(total_amount) as total_sales, SUM(profit) as total_profit FROM sales")
    sales_summary = cursor.fetchone()
    
    # মোট মালের আইটেম
    cursor.execute("SELECT COUNT(*) as total_items, SUM(quantity) as total_qty FROM stock")
    stock_summary = cursor.fetchone()
    
    # মোট কাস্টমার
    cursor.execute("SELECT COUNT(*) as total_cust FROM customers")
    cust_summary = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    tsales = sales_summary['total_sales'] if sales_summary['total_sales'] else 0
    tprofit = sales_summary['total_profit'] if sales_summary['total_profit'] else 0
    titems = stock_summary['total_items'] if stock_summary['total_items'] else 0
    tqty = stock_summary['total_qty'] if stock_summary['total_qty'] else 0
    tcust = cust_summary['total_cust'] if cust_summary['total_cust'] else 0

    # ৪টি ড্যাশবোর্ড কার্ড (মোবাইলে রেস্পনসিভ হবে)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='card-box'><h4>💰 মোট বিক্রয়</h4><h2>৳ {tsales:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card-box'><h4>📈 মোট লাভ</h4><h2>৳ {tprofit:,.2f}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card-box'><h4>📦 মোট প্রোডাক্ট আইটেম</h4><h2>{titems} টি ({tqty} পিস)</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='card-box'><h4>👤 মোট কাস্টমার</h4><h2>{tcust} জন</h2></div>", unsafe_allow_html=True)

# ==========================================
# 📦 স্টক ম্যানেজমেন্ট (STOCK MANAGEMENT)
# ==========================================
elif menu_choice == "📦 স্টক ম্যানেজমেন্ট":
    st.markdown("<h2 class='main-title'>📦 স্টক মালের হিসাব</h2>", unsafe_allow_html=True)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # এডিট মোড এক্টিভ কিনা চেক করা
    if st.session_state["editing_stock_id"] is not None:
        st.subheader("📝 পণ্য স্টক এডিট করুন")
        prod_id = st.session_state["editing_stock_id"]
        cursor.execute("SELECT * FROM stock WHERE id=%s", (prod_id,))
        edit_item = cursor.fetchone()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            item_name = st.text_input("Product Name", value=edit_item["product_name"])
        with col2:
            quantity = st.number_input("Quantity", min_value=0, value=int(edit_item["quantity"]))
        with col3:
            cost_price = st.number_input("Cost Price", min_value=0.0, value=float(edit_item["cost_price"]))
        with col4:
            sell_rate = st.number_input("Sell Rate", min_value=0.0, value=float(edit_item["sell_rate"]))
            
        btn_c1, btn_c2, _ = st.columns([2, 2, 8])
        with btn_c1:
            if st.button("💾 আপডেট সংরক্ষণ করুন"):
                cursor.execute("UPDATE stock SET product_name=%s, quantity=%s, cost_price=%s, sell_rate=%s WHERE id=%s", 
                               (item_name, quantity, cost_price, sell_rate, prod_id))
                conn.commit()
                st.session_state["editing_stock_id"] = None
                st.success("স্টক ডাটাবেসে সফলভাবে আপডেট হয়েছে!")
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
                cursor.execute("INSERT INTO stock (date_added, product_name, quantity, cost_price, sell_rate) VALUES (%s, %s, %s, %s, %s)", 
                               (current_date, item_name, quantity, cost_price, sell_rate))
                conn.commit()
                st.success(f"সফলভাবে '{item_name}' ডাটাবেস স্টকে যোগ করা হয়েছে!")
                st.rerun()
                
    st.markdown("---")
    st.subheader("📋 বর্তমান স্টক তালিকা")
    cursor.execute("SELECT * FROM stock ORDER BY id DESC")
    stocks = cursor.fetchall()
    
    if stocks:
        h_sl, h_date, h_name, h_qty, h_cost, h_sell, h_action = st.columns([1, 2, 3, 2, 2, 2, 3])
        h_sl.markdown("**Sl.**")
        h_date.markdown("**Date**")
        h_name.markdown("**Product Name**")
        h_qty.markdown("**Quantity**")
        h_cost.markdown("**Cost Price**")
        h_sell.markdown("**Sell Rate**")
        h_action.markdown("**Actions**")
        st.markdown("<hr style='margin: 5px 0px;' />", unsafe_allow_html=True)
        
        for idx, item in enumerate(stocks):
            c_sl, c_date, c_name, c_qty, c_cost, c_sell, c_action = st.columns([1, 2, 3, 2, 2, 2, 3])
            c_sl.write(idx + 1)
            c_date.write(item["date_added"])
            c_name.write(item["product_name"])
            c_qty.write(item["quantity"])
            c_cost.write(f"৳{item['cost_price']}")
            c_sell.write(f"৳{item['sell_rate']}")
            
            btn_edit, btn_del = c_action.columns(2)
            if btn_edit.button("✏️ Edit", key=f"edit_{item['id']}"):
                st.session_state["editing_stock_id"] = item['id']
                st.rerun()
            if btn_del.button("🗑️ Delete", key=f"del_{item['id']}"):
                cursor.execute("DELETE FROM stock WHERE id=%s", (item['id'],))
                conn.commit()
                st.success("পণ্যটি সফলভাবে মুছে ফেলা হয়েছে।")
                st.rerun()
    else:
        st.info("স্টকে কোনো পণ্য নেই।")
        
    cursor.close()
    conn.close()

# ==========================================
# 🔍 পণ্য সার্চ (PRODUCT SEARCH)
# ==========================================
elif menu_choice == "🔍 পণ্য সার্চ":
    st.markdown("<h2 class='main-title'>🔍 পণ্য সার্চ ও অনুসন্ধান</h2>", unsafe_allow_html=True)
    search_query = st.text_input("পণ্যের নাম লিখে সার্চ করুন...")
    
    if search_query:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stock WHERE product_name LIKE %s", (f"%{search_query}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if results:
            df = pd.DataFrame(results)
            df.columns = ["ID", "তারিখ", "পণ্যের নাম", "পরিমাণ (Stock)", "ক্রয়মূল্য", "বিক্রয়মূল্য"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("এই নামে কোনো পণ্য পাওয়া যায়নি।")

# ==========================================
# 🧾 ইনভয়েস তৈরি ও প্রিন্ট (INVOICE GENERATOR)
# ==========================================
elif menu_choice == "🧾 ইনভয়েস তৈরি ও প্রিন্ট":
    st.markdown("<h2 class='main-title'>🧾 ক্যাশ মেমো / ইনভয়েস জেনারেটর</h2>", unsafe_allow_html=True)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # অটো কাস্টমার সাজেস্ট ড্রপডাউন
    cursor.execute("SELECT name FROM customers")
    existing_custs = [c['name'] for c in cursor.fetchall()]
    
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
    cursor.execute("SELECT id, product_name, sell_rate, cost_price, quantity FROM stock WHERE quantity > 0")
    available_products = cursor.fetchall()
    prod_options = {p['product_name']: p for p in available_products}
    
    updated_items = []
    for i, item in enumerate(st.session_state["invoice_items"]):
        col_desc, col_qty, col_uprice = st.columns([5, 2, 3])
        
        with col_desc:
            selected_prod = st.selectbox(f"পণ্যের নাম সিলেক্ট করুন #{i+1}", [""] + list(prod_options.keys()), key=f"inv_prod_{i}")
        with col_qty:
            max_q = prod_options[selected_prod]['quantity'] if selected_prod else 100
            qty = st.number_input(f"QTY #{i+1}", min_value=1, max_value=max_q, value=1, key=f"inv_qty_{i}")
        with col_uprice:
            default_price = float(prod_options[selected_prod]['sell_rate']) if selected_prod else 0.0
            uprice = st.number_input(f"মূল্য #{i+1}", min_value=0.0, value=default_price, key=f"inv_price_{i}")
            
        if selected_prod:
            updated_items.append({
                "id": prod_options[selected_prod]['id'],
                "description": selected_prod, 
                "qty": qty, 
                "uprice": uprice,
                "cost_price": float(prod_options[selected_prod]['cost_price'])
            })
            
    col_btn1, col_btn2, _ = st.columns([2, 2, 6])
    with col_btn1:
        if st.button("➕ নতুন রো যোগ করুন"):
            st.session_state["invoice_items"].append({"description": "", "qty": 1, "uprice": 0})
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
            
            # কাস্টমার সেভ বা অটো আপডেট
            if customer_name not in existing_custs:
                cursor.execute("INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)", (customer_name, customer_phone, customer_address))
            
            for index, item in enumerate(updated_items):
                amount = item["qty"] * item["uprice"]
                sub_total += amount
                total_cost += (item["qty"] * item["cost_price"])
                
                # স্টক থেকে পরিমাণ মাইনাস বা আপডেট করা
                cursor.execute("UPDATE stock SET quantity = quantity - %s WHERE id = %s", (item["qty"], item["id"]))
                
                table_rows_html += f"""
                <tr>
                    <td style='text-align:center;'>{index+1}</td>
                    <td>{item['description']}</td>
                    <td style='text-align:center;'>{item['qty']}</td>
                    <td style='text-align:right;'>{item['uprice']}</td>
                    <td style='text-align:right;'>{amount}</td>
                </tr>
                """
            
            total_bill = sub_total - discount
            total_profit = total_bill - total_cost
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # সেলস রিপোর্টে ডাটা সেভ করা
            cursor.execute("INSERT INTO sales (invoice_no, customer_name, customer_phone, sale_date, total_amount, discount, profit) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (invoice_no, customer_name, customer_phone, current_date, total_bill, discount, total_profit))
            conn.commit()
            
            # ৫x৭ ইঞ্চি ক্যাশ মেমো প্রিন্ট টেমপ্লেট
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
            
    cursor.close()
    conn.close()

# ==========================================
# 👤 কাস্টমার ম্যানেজমেন্ট (CUSTOMER MANAGEMENT)
# ==========================================
elif menu_choice == "👤 কাস্টমার ম্যানেজমেন্ট":
    st.markdown("<h2 class='main-title'>👤 কাস্টমার ম্যানেজমেন্ট</h2>", unsafe_allow_html=True)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers ORDER BY id DESC")
    cust_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if cust_data:
        df_cust = pd.DataFrame(cust_data)
        df_cust.columns = ["ID", "কাস্টমারের নাম", "মোবাইল নম্বর", "ঠিকানা"]
        st.dataframe(df_cust, use_container_width=True)
    else:
        st.info("এখনো কোনো কাস্টমার রেজিস্টার্ড হয়নি।")

# ==========================================
# 📊 বিক্রয় রিপোর্ট (SALES REPORT)
# ==========================================
elif menu_choice == "📊 বিক্রয় রিপোর্ট":
    st.markdown("<h2 class='main-title'>📊 বিক্রয় রিপোর্ট তালিকা</h2>", unsafe_allow_html=True)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT invoice_no, customer_name, sale_date, total_amount, discount FROM sales ORDER BY id DESC")
    sales_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if sales_data:
        df_sales = pd.DataFrame(sales_data)
        df_sales.columns = ["ইনভয়েস নম্বর", "কাস্টমার নাম", "তারিখ", "মোট বিল (৳)", "ডিসকাউন্ট (৳)"]
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("কোনো বিক্রয়ের রেকর্ড পাওয়া যায়নি।")

# ==========================================
# 💰 লাভ-লোকসানের হিসাব (PROFIT LOSS LOSS)
# ==========================================
elif menu_choice == "💰 লাভ-লোকসানের হিসাব":
    st.markdown("<h2 class='main-title'>💰 লাভ-লোকসানের নিখুঁত হিসাব</h2>", unsafe_allow_html=True)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sale_date, SUM(total_amount) as sales, SUM(profit) as profits FROM sales GROUP BY sale_date ORDER BY id DESC")
    profit_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if profit_data:
        df_p = pd.DataFrame(profit_data)
        df_p.columns = ["তারিখ", "মোট বিক্রি (৳)", "নীট লাভ (৳)"]
        st.dataframe(df_p, use_container_width=True)
        
        # গ্রাফ চার্ট
        st.markdown("### 📈 বিক্রয় বনাম লাভ গ্রাফ চিত্র")
        st.line_chart(df_p.set_index("তারিখ"))
    else:
        st.info("হিসাব দেখানোর জন্য পর্যাপ্ত বিক্রয় ডাটা নেই।")
