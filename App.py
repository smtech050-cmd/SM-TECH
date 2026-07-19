import streamlit as st
import pandas as pd
import datetime
import base64
from weasyprint import HTML

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ইনিশিয়ালাইজেশন (স্থায়ী ডাটা সংরক্ষণ)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# মেনু নেভিগেশনের জন্য সেশন স্টেট (ডিফল্ট: Dashboard)
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

# কাস্টমার বাকির হিসাব সেশন স্টেট (স্থায়ী সংরক্ষণ)
if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"ক্রমিক নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup & Cleaning", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200},
        {"ক্রমিক নং": 2, "কাস্টমার নাম": "Sristi", "কাজের বিবরণ": "Asus Motherboard Repair", "পরিমান": 1, "দর": 2500, "মোট টাকা": 2500, "আদায়": 1500, "বাকি": 1000}
    ]

# স্টক পণ্যের হিসাব সেশন স্টেট (স্থায়ী সংরক্ষণ)
if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"ক্রমিক নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000},
        {"ক্রমিক নং": 2, "পণ্যের বিবরণ": "DDR4 8GB RAM", "পরিমান": 15, "দর": 2400, "মোট টাকা": 36000}
    ]

# পাসওয়ার্ড সংরক্ষণের জন্য সেশন স্টেট
if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = [
        {"ক্রমিক নং": 1, "শিক্ষা প্রতিষ্ঠানের নাম": "Sreebardi Govt. College", "এন্ট্রি পাসওয়ার্ড": "sreebardi@2026", "কনফার্ম পাসওয়ার্ড": "sreebardi@2026"}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🎨 গ্লোবাল থিম ও সাইডবার প্রিমিয়াম বাটন CSS
# ==========================================
custom_css = """
<style>
    /* মেইন ব্যাকগ্রাউন্ড */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #001f4d 0%, #000a1a 100%);
        color: white;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] {
        background-color: #030f26 !important;
        border-right: 1px solid #002b80;
    }
    
    .panel-header {
        font-size: 20px;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #0055ff;
        padding-bottom: 10px;
    }
    .stTextInput label, .stNumberInput label, .stFileUploader label {
        color: #a0c0ff !important;
        font-weight: bold;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
    }
    
    /* স্টাইলিশ বাটন মেনুর সিএসএস */
    div.stButton > button {
        background-color: #0b3c95 !important;
        color: white !important;
        border: none !important;
        border-left: 5px solid #00a2ff !important;
        padding: 15px 20px !important;
        text-align: left !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
    }
    
    /* বাটন হোভার */
    div.stButton > button:hover {
        background-color: #0044cc !important;
        border-left: 5px solid #00ffcc !important;
        box-shadow: 0px 4px 15px rgba(0, 162, 255, 0.4);
        transform: scale(1.02);
    }
    
    /* একটিভ বাটন */
    div.stButton > button:focus, div.stButton > button:active {
        background-color: #0044cc !important;
        border-left: 5px solid #00ffcc !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং
# ==========================================
if not st.session_state.logged_in:
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
    # --- 🛠️ কাস্টম স্টাইলিশ সাইডবার মেনু তৈরি ---
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 32px; margin-right: 10px;">⚙️</span>
                <span style="font-size: 28px; font-weight: bold; color: white;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h3 style='color:#a0c0ff; font-size:18px;'>Select Menu</h3>", unsafe_allow_html=True)
        
        if st.button("⬜  Dashboard", use_container_width=True):
            st.session_state.current_menu = "Dashboard"
            st.rerun()
            
        if st.button("👥  Customer & Repair", use_container_width=True):
            st.session_state.current_menu = "Customer & Repair"
            st.rerun()
            
        if st.button("📦  Stock product", use_container_width=True):
            st.session_state.current_menu = "Stock product"
            st.rerun()
            
        if st.button("💵  Sell Invoice", use_container_width=True):
            st.session_state.current_menu = "Sell Invoice"
            st.rerun()

        if st.button("🔐  Password Save", use_container_width=True):
            st.session_state.current_menu = "Password Save"
            st.rerun()

    # --- 📊 ড্যাশবোর্ড মডিউল (Dashboard) ---
    if st.session_state.current_menu == "Dashboard":
        st.title("🖥️ রিপেয়ার ও POS ড্যাশবোর্ড")
        st.subheader("এসএম-টেক কম্পিউটার ও আইটি সল্যুশন")
        
        col1, col2, col3 = st.columns(3)
        total_due_amount = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock_value = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        
        col1.metric("মোট বাকির হিসাব (কাস্টমার)", f"{len(st.session_state.customer_dues)} জন")
        col2.metric("মোট বাকি টাকা", f"{total_due_amount} BDT")
        col3.metric("স্টক পণ্যের মোট মূল্য", f"{total_stock_value} BDT")
        
        st.write("### 📑 কাস্টমার বাকির সংক্ষিপ্ত বিবরণ")
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True, hide_index=True)

    # --- 🔧 কাস্টমার ও রিপেয়ার (Customer & Repair) ---
    elif st.session_state.current_menu == "Customer & Repair":
        st.title("💸 কাস্টমার বাকির হিসাব ও রিপেয়ার")
        
        with st.form("Add Customer Due", clear_on_submit=True):
            st.write("### ➕ নতুন বাকির হিসাব যুক্ত করুন")
            c_name = st.text_input("কাস্টমার নাম")
            c_desc = st.text_input("কাজের বিবরণ")
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                c_qty = st.number_input("পরিমান", min_value=1, value=1, step=1)
            with col_c2:
                c_price = st.number_input("দর (টাকা)", min_value=0, value=0, step=50)
            with col_c3:
                c_paid = st.number_input("আদায় (টাকা)", min_value=0, value=0, step=50)
                
            submitted = st.form_submit_button(label="💾 লিস্টে যুক্ত করুন")
            
            if submitted and c_name and c_desc:
                total_amt = c_qty * c_price
                due_amt = total_amt - c_paid
                new_sl = len(st.session_state.customer_dues) + 1 if st.session_state.customer_dues else 1
                
                st.session_state.customer_dues.append({
                    "ক্রমিক নং": new_sl,
                    "কাস্টমার নাম": c_name,
                    "কাজের বিবরণ": c_desc,
                    "পরিমান": c_qty,
                    "দর": c_price,
                    "মোট টাকা": total_amt,
                    "আদায়": c_paid,
                    "বাকি": due_amt
                })
                st.success(f"সফলভাবে {c_name} এর বাকির হিসাব যুক্ত হয়েছে!")
                st.rerun()

        st.write("### 📋 বর্তমান কাস্টমার বাকির তালিকা")
        if st.session_state.customer_dues:
            df_dues = pd.DataFrame(st.session_state.customer_dues)
            st.dataframe(df_dues, use_container_width=True, hide_index=True)
            
            st.write("### 🗑️ এন্ট্রি ডিলিট করুন")
            col_del1, col_del2 = st.columns([2, 1])
            with col_del1:
                delete_id = st.number_input("ডিলিট করার জন্য ক্রমিক নং লিখুন:", min_value=1, max_value=200, step=1)
            with col_del2:
                st.markdown("<br>", unsafe_allow_html=True)
                delete_btn = st.button("❌ এন্ট্রি মুছুন", type="primary", use_container_width=True)
            
            if delete_btn:
                st.session_state.customer_dues = [item for idx, item in enumerate(st.session_state.customer_dues) if item["ক্রমিক নং"] != delete_id]
                for idx, item in enumerate(st.session_state.customer_dues):
                    item["ক্রমিক নং"] = idx + 1
                st.toast("তালিকা সফলভাবে আপডেট করা হয়েছে।")
                st.rerun()
        else:
            st.info("কোনো বাকির হিসাব পাওয়া যায়নি।")

    # --- 📦 স্টক পণ্য (Stock product) ---
    elif st.session_state.current_menu == "Stock product":
        st.title("📦 দোকানের স্টক পণ্য ম্যানেজমেন্ট")
        
        with st.form("Add Shop Stock", clear_on_submit=True):
            st.write("### ➕ নতুন স্টক পণ্য যুক্ত করুন")
            s_desc = st.text_input("পণ্যের বিবরণ / নাম")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                s_qty = st.number_input("পরিমান", min_value=1, value=1, step=1)
            with col_s2:
                s_price = st.number_input("দর (টাকা)", min_value=0, value=0, step=50)
                
            submitted_stock = st.form_submit_button(label="📥 স্টকে যুক্ত করুন")
            
            if submitted_stock and s_desc:
                total_stock_amt = s_qty * s_price
                new_sl_stock = len(st.session_state.shop_stock) + 1 if st.session_state.shop_stock else 1
                
                st.session_state.shop_stock.append({
                    "ক্রমিক নং": new_sl_stock,
                    "পণ্যের বিবরণ": s_desc,
                    "পরিমান": s_qty,
                    "দর": s_price,
                    "মোট টাকা": total_stock_amt
                })
                st.success(f"স্টকে সফলভাবে {s_desc} যুক্ত হয়েছে!")
                st.rerun()

        st.write("### 📋 বর্তমানে মজুদ মালামালের তালিকা")
        if st.session_state.shop_stock:
            df_stock = pd.DataFrame(st.session_state.shop_stock)
            st.dataframe(df_stock, use_container_width=True, hide_index=True)
            
            st.write("### 🗑️ স্টক পণ্য ডিলিট করুন")
            col_sdel1, col_sdel2 = st.columns([2, 1])
            with col_sdel1:
                delete_stock_id = st.number_input("ডিলিট করার জন্য পণ্যের ক্রমিক নং লিখুন:", min_value=1, max_value=200, step=1, key="stock_del_id")
            with col_sdel2:
                st.markdown("<br>", unsafe_allow_html=True)
                delete_stock_btn = st.button("❌ পণ্য মুছুন", type="primary", use_container_width=True, key="stock_del_btn")
            
            if delete_stock_btn:
                st.session_state.shop_stock = [item for idx, item in enumerate(st.session_state.shop_stock) if item["ক্রমিক নং"] != delete_stock_id]
                for idx, item in enumerate(st.session_state.shop_stock):
                    item["ক্রমিক নং"] = idx + 1
                st.toast("পণ্যটি স্টক থেকে মুছে ফেলা হয়েছে।")
                st.rerun()
        else:
            st.info("স্টকে কোনো পণ্য নেই।")

    # --- 🔐 পাসওয়ার্ড সংরক্ষণ (Password Save) ---
    elif st.session_state.current_menu == "Password Save":
        st.title("🔐 শিক্ষা প্রতিষ্ঠানের পাসওয়ার্ড সংরক্ষণ ব্যবস্থা")
        
        with st.form("Add Institution Password", clear_on_submit=True):
            st.write("### ➕ নতুন শিক্ষা প্রতিষ্ঠানের পাসওয়ার্ড যুক্ত করুন")
            inst_name = st.text_input("শিক্ষা প্রতিষ্ঠানের নাম", placeholder="প্রতিষ্ঠানের নাম লিখুন...")
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                entry_pass = st.text_input("এন্ট্রি পাসওয়ার্ড", type="password", placeholder="পাসওয়ার্ড দিন...")
            with col_p2:
                confirm_pass = st.text_input("কনফার্ম পাসওয়ার্ড", type="password", placeholder="পাসওয়ার্ড নিশ্চিত করুন...")
                
            submitted_pass = st.form_submit_button(label="💾 পাসওয়ার্ড সংরক্ষণ করুন")
            
            if submitted_pass:
                if not inst_name or not entry_pass or not confirm_pass:
                    st.error("অনুগ্রহ করে সবকটি ঘর পূরণ করুন।")
                elif entry_pass != confirm_pass:
                    st.error("এন্ট্রি পাসওয়ার্ড এবং কনফার্ম পাসওয়ার্ড মেলেনি!")
                else:
                    new_sl_pass = len(st.session_state.saved_passwords) + 1 if st.session_state.saved_passwords else 1
                    st.session_state.saved_passwords.append({
                        "ক্রমিক নং": new_sl_pass,
                        "শিক্ষা প্রতিষ্ঠানের নাম": inst_name,
                        "এন্ট্রি পাসওয়ার্ড": entry_pass,
                        "কনফার্ম পাসওয়ার্ড": confirm_pass
                    })
                    st.success(f"সফলভাবে {inst_name} এর পাসওয়ার্ড সংরক্ষিত হয়েছে!")
                    st.rerun()

        st.write("### 📋 সংরক্ষিত পাসওয়ার্ডের তালিকা")
        if st.session_state.saved_passwords:
            df_passwords = pd.DataFrame(st.session_state.saved_passwords)
            st.dataframe(df_passwords, use_container_width=True, hide_index=True)
            
            st.write("### 🗑️ পাসওয়ার্ড মুছুন")
            col_pdel1, col_pdel2 = st.columns([2, 1])
            with col_pdel1:
                delete_pass_id = st.number_input("ডিলিট করার জন্য ক্রমিক নং লিখুন:", min_value=1, max_value=500, step=1, key="pass_del_id")
            with col_pdel2:
                st.markdown("<br>", unsafe_allow_html=True)
                delete_pass_btn = st.button("❌ ডাটা মুছুন", type="primary", use_container_width=True, key="pass_del_btn")
            
            if delete_pass_btn:
                st.session_state.saved_passwords = [item for idx, item in enumerate(st.session_state.saved_passwords) if item["क्रमিক নং"] != delete_pass_id]
                for idx, item in enumerate(st.session_state.saved_passwords):
                    item["ক্রমিক নং"] = idx + 1
                st.toast("তালিকা থেকে সফলভাবে মুছে ফেলা হয়েছে।")
                st.rerun()
        else:
            st.info("কোনো পাসওয়ার্ড সংরক্ষিত নেই।")

    # --- 🧾 সেল ইনভয়েস (Sell Invoice) ---
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 পয়েন্ট অব সেল ও ইনভয়েস")
        
        uploaded_logo = st.file_uploader("Upload Shop Logo / দোকানের লোগো আপলোড করুন (Optional)", type=["png", "jpg", "jpeg"])
        logo_base64 = ""
        if uploaded_logo is not None:
            bytes_data = uploaded_logo.read()
            logo_base64 = f"data:image/png;base64,{base64.b64encode(bytes_data).decode()}"
        
        st.markdown("### 👤 Customer Info")
        col_in1, col_in2, col_in3 = st.columns([1.5, 2, 2])
        with col_in1:
            inv_custom_num = st.text_input("Invoice No (ইনভয়েস নং)", value="1001")
        with col_in2:
            cust_name = st.text_input("কাস্টমারের নাম", value="খুচরা কাস্টমার")
        with col_in3:
            cust_address = st.text_input("Address (ঠিকানা)", value="Dhaka, Bangladesh")
            
        st.write("---")
        st.markdown("### 🛒 Add Items to Invoice (পণ্য যোগ করুন)")
        
        col_item1, col_item2, col_item3 = st.columns([3, 1, 1.5])
        with col_item1:
            prod_desc = st.text_input("Product Name / Description (পণ্যের নাম বা বিবরণ)", placeholder="যেমন: DDR4 8GB RAM, Motherboard Repairing")
        with col_item2:
            prod_qty = st.number_input("QTY (পরিমাণ)", min_value=1, value=1, step=1)
        with col_item3:
            prod_price = st.number_input("Unit Price (BDT)", min_value=0, value=500, step=50)
            
        if st.button("➕ Add Item to List (কলামে যুক্ত করুন)", use_container_width=True):
            if prod_desc:
                st.session_state.invoice_items.append({
                    "Description": prod_desc,
                    "Qty": prod_qty,
                    "Price": prod_price,
                    "Amount": prod_qty * prod_price
                })
                st.toast("Item added successfully!")
            else:
                st.error("Please enter item description first.")
                
        if st.session_state.invoice_items:
            st.write("#### Added Items Summary:")
            df_invoice = pd.DataFrame(st.session_state.invoice_items)
            st.dataframe(df_invoice, use_container_width=True)
            if st.button("🗑️ Clear All Items (সব মুছুন)"):
                st.session_state.invoice_items = []
                st.rerun()
        
        st.write("---")
        
        if st.button("📄 ইনভয়েস প্রিভিউ ও PDF ডাউনলোড করুন", type="primary", use_container_width=True):
            if not st.session_state.invoice_items:
                st.warning("Please add at least one item first! আগে লিস্টে পণ্য যোগ করুন।")
            else:
                current_date = datetime.datetime.now().strftime('%d-%m-%Y')
                
                rows_html = ""
                total_calculated = 0
                for index, item in enumerate(st.session_state.invoice_items):
                    sl = index + 1
                    total_calculated += item["Amount"]
                    rows_html += f"""
                    <tr style="text-align: center; height: 26px;">
                        <td style="border: 1px solid #1e3a8a; padding: 4px;">{sl}</td>
                        <td style="border: 1px solid #1e3a8a; padding: 4px 6px; text-align: left;">{item['Description']}</td>
                        <td style="border: 1px solid #1e3a8a; padding: 4px;">{item['Qty']}</td>
                        <td style="border: 1px solid #1e3a8a; padding: 4px;">{item['Price']}/-</td>
                        <td style="border: 1px solid #1e3a8a; padding: 4px; font-weight: bold;">{item['Amount']}/-</td>
                    </tr>
                    """
                
                remaining_rows = 10 - len(st.session_state.invoice_items)
                for i in range(max(0, remaining_rows)):
                    sl_blank = len(st.session_state.invoice_items) + i + 1
                    rows_html += f"""
                    <tr style="height: 24px;">
                        <td style="border: 1px solid #1e3a8a; padding: 4px; text-align: center; color: #777;">{sl_blank}</td>
                        <td style="border: 1px solid #1e3a8a;"></td>
                        <td style="border: 1px solid #1e3a8a;"></td>
                        <td style="border: 1px solid #1e3a8a;"></td>
                        <td style="border: 1px solid #1e3a8a;"></td>
                    </tr>
                    """
                
                # WeasyPrint সমর্থিত নিখুঁত HTML ফরম্যাট (৫"x৭" সাইজ পেজ মিডিয়াসহ)
                invoice_html_for_pdf = f"""
                <html>
                <head>
                <style>
                    @page {{
                        size: 5in 7in;
                        margin: 0.25in;
                    }}
                    body {{
                        font-family: 'Arial', sans-serif;
                        color: black;
                        margin: 0;
                        padding: 0;
                    }}
                    .invoice-box {{
                        border: 3px solid #1e3a8a; 
                        padding: 10px; 
                        background-color: white; 
                        box-sizing: border-box;
                        height: 100%;
                        position: relative;
                    }}
                </style>
                </head>
                <body>
                <div class="invoice-box">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 5px;">
                        <tr>
                            <td style="width: 20%; vertical-align: middle; text-align: left;">
                                {'<img src="' + logo_base64 + '" style="width: 55px; height: 55px; border-radius: 50%;">' if logo_base64 else '<div style="width: 55px; height: 55px; background: #e2e8f0; border-radius: 50%; text-align: center; line-height: 55px; font-size: 9px; color: #777;">No Logo</div>'}
                            </td>
                            <td style="width: 48%; vertical-align: middle; padding-left: 5px;">
                                <span style="font-size: 26px; font-weight: 900; color: #1e3a8a; font-family: sans-serif; line-height: 1.1; display: block;">SM-TECH</span>
                                <span style="font-size: 8px; font-weight: 800; color: #059669; letter-spacing: 0.5px; display: block; margin-top: 2px;">COMPUTER & IT SOLUTION</span>
                            </td>
                            <td style="width: 32%; text-align: right; font-size: 10px; line-height: 1.3; vertical-align: middle; font-weight: bold; color: #111;">
                                <span style="font-size: 13px; font-weight: 900; color: #1e3a8a; display: block;">S.m. Ibrahim</span>
                                <span style="font-size: 9px; color: #555; display: block; font-weight: normal;">Owner</span>
                                <span style="font-size: 10.5px; font-weight: 800; display: block;">01940-556114</span>
                                <span style="font-size: 10.5px; font-weight: 800; display: block;">01810-499166</span>
                            </td>
                        </tr>
                    </table>
                    
                    <div style="border-top: 2.5px solid #1e3a8a; margin-top: 5px; margin-bottom: 8px;"></div>
                    
                    <table style="width: 100%; font-size: 10px; margin-bottom: 10px; line-height: 1.3;">
                        <tr>
                            <td style="width: 55%; vertical-align: top;">
                                <span style="background-color: #1e3a8a; color: white; padding: 2px 5px; font-weight: bold; font-size: 9px; border-radius: 2px; display: inline-block;">Bill To</span>
                                <div style="margin-top: 4px;"><b>Name:</b> {cust_name}</div>
                                <div style="margin-top: 2px;"><b>Address:</b> {cust_address}</div>
                            </td>
                            <td style="width: 45%; text-align: right; vertical-align: top;">
                                <span style="background-color: #1e3a8a; color: white; padding: 2px 10px; font-weight: bold; font-size: 10px; border-radius: 2px; display: inline-block;">INVOICE</span>
                                <div style="margin-top: 4px;"><b>Invoice No:</b> # {inv_custom_num}</div>
                                <div style="margin-top: 2px;"><b>Date:</b> {current_date}</div>
                            </td>
                        </tr>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 10px; border: 1px solid #1e3a8a;">
                        <thead>
                            <tr style="background-color: #1e3a8a; color: white; text-align: center; font-weight: bold; font-size: 9px;">
                                <th style="border: 1px solid #1e3a8a; padding: 5px 3px; width: 8%;">S.L</th>
                                <th style="border: 1px solid #1e3a8a; padding: 5px 5px; width: 52%;">DESCRIPTION</th>
                                <th style="border: 1px solid #1e3a8a; padding: 5px 3px; width: 10%;">QTY</th>
                                <th style="border: 1px solid #1e3a8a; padding: 5px 3px; width: 14%;">U.PRICE</th>
                                <th style="border: 1px solid #1e3a8a; padding: 5px 3px; width: 16%;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                            <tr>
                                <td colspan="3" style="border: 1px solid #1e3a8a;"></td>
                                <td style="border: 1px solid #1e3a8a; padding: 5px; text-align: center; font-weight: bold; background-color: #1e3a8a; color: white; font-size: 9px;">SUB TOTAL</td>
                                <td style="border: 1px solid #1e3a8a; padding: 5px; text-align: center; font-weight: bold; background-color: #f3f4f6; font-size: 10px;">{total_calculated} BDT</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <table style="width: 100%; margin-top: 35px; font-size: 9px;">
                        <tr>
                            <td style="width: 50%; vertical-align: bottom;">
                                <div style="border: 1px solid #1e3a8a; display: inline-block; border-radius: 2px; background-color: white;">
                                    <div style="background-color: #1e3a8a; color: white; padding: 1px 4px; font-weight: bold; font-size: 8px;">Payment Methods</div>
                                    <div style="padding: 2px 4px; font-weight: bold; color: #222; font-size: 9px;">Cash | Bkash | Nagad | Bank</div>
                                </div>
                            </td>
                            <td style="width: 50%; text-align: right; vertical-align: bottom;">
                                <div style="display: inline-block; text-align: center; width: 130px;">
                                    <div style="border-top: 1px solid #000; margin-bottom: 2px;"></div>
                                    <b>Authorised Signature</b>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
                </body>
                </html>
                """
                
                # ওয়েব ইন্টারফেসে প্রিভিউ দেখানোর জন্য
                st.markdown("#### 📄 Invoice Preview (প্রিভিউ):")
                st.markdown(f"""
                <div style="background-color: #f0f2f5; padding: 15px; display: flex; justify-content: center;">
                    <iframe srcdoc='{invoice_html_for_pdf}' style="width: 5.2in; height: 7.2in; border: none; background: white;"></iframe>
                </div>
                """, unsafe_allow_html=True)
                
                # HTML থেকে WeasyPrint ব্যবহার করে সরাসরি PDF জেনারেট করা হচ্ছে
                pdf_bytes = HTML(string=invoice_html_for_pdf).write_pdf()
                
                # স্ট্রিমলিটের নেটিভ ডাউনলোড বাটন যুক্ত করা হলো
                st.download_button(
                    label="📥 Download 5\"x7\" Invoice PDF",
                    data=pdf_bytes,
                    file_name=f"Invoice_{inv_custom_num}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
