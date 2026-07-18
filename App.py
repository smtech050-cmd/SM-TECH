import streamlit as st
import pandas as pd
import datetime
import base64

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# কাস্টমার বাকির হিসাব সেশন স্টেট
if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"ক্রমিক নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup & Cleaning", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200},
        {"ক্রমিক নং": 2, "কাস্টমার নাম": "Sristi", "কাজের বিবরণ": "Asus Motherboard Repair", "পরিমান": 1, "দর": 2500, "মোট টাকা": 2500, "আদায়": 1500, "বাকি": 1000}
    ]

# স্টক পণ্যের হিসাব সেশন স্টেট
if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"ক্রমিক নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000},
        {"ক্রমিক নং": 2, "পণ্যের বিবরণ": "DDR4 8GB RAM", "পরিমান": 15, "দর": 2400, "মোট টাকা": 36000}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🎨 ডার্ক ব্লু নিয়ন থিম সিএসএস
# ==========================================
login_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #001f4d 0%, #000a1a 100%);
        color: white;
    }
    [data-testid="stHeader"] {
        background: transparent;
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
</style>
"""

# ==========================================
# 🌐 ভাষা ডিকশনারি
# ==========================================
LANG = {
    "বাংলা": {
        "nav_title": "⚙️ SM-TECH",
        "go_to": "মেনু সিলেক্ট করুন",
        "menu": ["ড্যাশবোর্ড", "কাস্টমার ও রিপেয়ার", "স্টক / ইনভেন্টরি", "POS ও ইনভয়েস"],
        "dash_title": "🖥️ রিপেয়ার ও POS ড্যাশবোর্ড",
        "sub_title": "এসএম-টেক কম্পিউটার ও আইটি সリューション",
        "btn_inv": "📄 ইনভয়েস প্রিভিউ দেখুন"
    }
}

t = LANG["বাংলা"]

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং
# ==========================================
if not st.session_state.logged_in:
    st.markdown(login_css, unsafe_allow_html=True)
    
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
    st.sidebar.title(t["nav_title"])
    if st.sidebar.button("🔒 Logout / লগআউট"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.write("---")
    st.sidebar.markdown(f"**{t['go_to']}**")
    menu_choice = st.sidebar.radio("", t["menu"], label_visibility="collapsed")

    # --- 📊 ড্যাশবোর্ড মডিউল ---
    if menu_choice == t["menu"][0]:
        st.title(t["dash_title"])
        st.subheader(t["sub_title"])
        
        col1, col2, col3 = st.columns(3)
        total_due_amount = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock_value = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        
        col1.metric("कुल বাকির হিসাব (কাস্টমার)", f"{len(st.session_state.customer_dues)} জন")
        col2.metric("মোট বাকি টাকা", f"{total_due_amount} BDT")
        col3.metric("স্টক পণ্যের মোট মূল্য", f"{total_stock_value} BDT")
        
        st.write("### 📑 কাস্টমার বাকির সংক্ষিপ্ত বিবরণ")
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True, hide_index=True)

    # --- 🔧 কাস্টমার বাকির হিসাব) ---
    elif menu_choice == t["menu"][1]:
        st.title("💸 কাস্টমার বাকির হিসাব")
        
        with st.form("Add Customer Due"):
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
                st.session_state.customer_dues = [item for idx, item in enumerate(st.session_state.customer_dues) if (idx + 1) != delete_id]
                for idx, item in enumerate(st.session_state.customer_dues):
                    item["ক্রমিক নং"] = idx + 1
                st.toast("তালিকা সফলভাবে আপডেট করা হয়েছে।")
                st.rerun()
        else:
            st.info("কোনো বাকির হিসাব পাওয়া যায়নি।")

    # --- 📦 স্টক / ইনভেন্টরি (সংশোধিত: দোকানের স্টক পণ্য) ---
    elif menu_choice == t["menu"][2]:
        st.title("📦 দোকানের স্টক পণ্য ম্যানেজমেন্ট")
        
        with st.form("Add Shop Stock"):
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
                st.session_state.shop_stock = [item for idx, item in enumerate(st.session_state.shop_stock) if (idx + 1) != delete_stock_id]
                for idx, item in enumerate(st.session_state.shop_stock):
                    item["क्रमिक নং"] = idx + 1
                st.toast("পণ্যটি স্টক থেকে মুছে ফেলা হয়েছে।")
                st.rerun()
        else:
            st.info("স্টকে কোনো পণ্য নেই।")

    # --- 🧾 POS ও ইনভয়েস মডিউল ---
    elif menu_choice == t["menu"][3]:
        st.title("🧾 পয়েন্ট অব সেল ও ইনভয়েস")
        
        uploaded_logo = st.file_uploader("Upload Shop Logo / দোকানের লোগো আপলোড করুন (Optional)", type=["png", "jpg", "jpeg"])
        logo_base64 = ""
        if uploaded_logo is not None:
            bytes_data = uploaded_logo.read()
            logo_base64 = f"data:image/png;base64,{base64.b64encode(bytes_data).decode()}"
        
        st.markdown("### 👤 Customer Info")
        col_in1, col_in2, col_in3 = st.columns([1.5, 2, 2])
        with col_in1:
            # ম্যানুয়াল ইনভয়েস নম্বর বসানোর ইনপুট বক্স
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
        
        if st.button(t["btn_inv"], type="primary", use_container_width=True):
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
                
                invoice_html = f"""
                <div style="background-color: #f0f2f5; padding: 20px; display: flex; justify-content: center;">
                <div id="print-area" style="
                    border: 3px solid #1e3a8a; 
                    padding: 18px; 
                    background-color: white; 
                    color: black; 
                    font-family: 'Arial', sans-serif; 
                    width: 5in; 
                    height: 7in; 
                    border-radius: 4px;
                    box-sizing: border-box;
                    position: relative;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                ">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 5px;">
                        <tr>
                            <td style="width: 20%; vertical-align: middle; text-align: left;">
                                {'<img src="' + logo_base64 + '" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover;">' if logo_base64 else '<div style="width: 60px; height: 60px; background: #e2e8f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #777;">No Logo</div>'}
                            </td>
                            <td style="width: 48%; vertical-align: middle; padding-left: 8px;">
                                <span style="font-size: 30px; font-weight: 900; color: #1e3a8a; font-family: 'Arial Black', Impact, sans-serif; line-height: 1.1; display: block; letter-spacing: -0.5px;">SM-TECH</span>
                                <span style="font-size: 8.5px; font-weight: 800; color: #059669; letter-spacing: 0.8px; display: block; margin-top: 2px;">COMPUTER & IT SOLUTION</span>
                                <span style="font-size: 8px; font-style: italic; color: #555; display: block; margin-top: 2px;">Smart Technology-Trusted Service</span>
                            </td>
                            <td style="width: 32%; text-align: right; font-size: 11px; line-height: 1.4; vertical-align: middle; font-weight: bold; color: #111;">
                                <span style="font-size: 14px; font-weight: 900; color: #1e3a8a; display: block; margin-bottom: 2px;">S.m. Ibrahim</span>
                                <span style="font-size: 10px; color: #555; display: block; margin-top: -3px; margin-bottom: 2px; font-weight: normal;">Owner</span>
                                <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01940-556114</span>
                                <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01810-499166</span>
                            </td>
                        </tr>
                    </table>
                    
                    <div style="border-top: 2.5px solid #1e3a8a; margin-top: 8px; margin-bottom: 12px;"></div>
                    
                    <table style="width: 100%; font-size: 11px; margin-bottom: 12px; line-height: 1.4;">
                        <tr>
                            <td style="width: 55%; vertical-align: top;">
                                <span style="background-color: #1e3a8a; color: white; padding: 3px 7px; font-weight: bold; font-size: 9.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">Bill To</span>
                                <div style="margin-top: 4px;"><b>Name:</b> {cust_name}</div>
                                <div style="margin-top: 2px;"><b>Address:</b> {cust_address}</div>
                            </td>
                            <td style="width: 45%; text-align: right; vertical-align: top;">
                                <span style="background-color: #1e3a8a; color: white; padding: 3px 12px; font-weight: bold; font-size: 10.5px; letter-spacing: 0.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">INVOICE</span>
                                <div style="margin-top: 4px;"><b>Invoice No:</b> # {inv_custom_num}</div>
                                <div style="margin-top: 2px;"><b>Date:</b> {current_date}</div>
                            </td>
                        </tr>
                    </table>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px; border: 1px solid #1e3a8a;">
                        <thead>
                            <tr style="background-color: #1e3a8a; color: white; text-align: center; font-weight: bold; font-size: 10px;">
                                <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 8%;">S.L</th>
                                <th style="border: 1px solid #1e3a8a; padding: 6px 6px; width: 52%;">DESCRIPTION</th>
                                <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 10%;">QTY</th>
                                <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 14%;">U.PRICE</th>
                                <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 16%;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                            <tr>
                                <td colspan="3" style="border: 1px solid #1e3a8a;"></td>
                                <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #1e3a8a; color: white; font-size: 10px;">SUB TOTAL</td>
                                <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #f3f4f6; font-size: 11px;">{total_calculated} BDT</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <table style="width: 100%; position: absolute; bottom: 18px; left: 18px; width: calc(100% - 36px); font-size: 10px;">
                        <tr>
                            <td style="width: 50%; vertical-align: bottom;">
                                <div style="border: 1px solid #1e3a8a; display: inline-block; border-radius: 2px; background-color: white;">
                                    <div style="background-color: #1e3a8a; color: white; padding: 2px 6px; font-weight: bold; font-size: 8.5px;">Payment Methods</div>
                                    <div style="padding: 3px 6px; font-weight: bold; color: #222; font-size: 9.5px;">Cash | Bkash | Nagad | Bank</div>
                                </div>
                            </td>
                            <td style="width: 50%; text-align: right; vertical-align: bottom;">
                                <div style="display: inline-block; text-align: center; width: 150px;">
                                    <div style="border-top: 1px solid #000; margin-bottom: 3px;"></div>
                                    <b>Authorised Signature</b><br>
                                    <span style="font-size: 8.5px; color: #444;">SM-TECH Computer & IT Solutions</span>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
                </div>
                """
                
                # ফিক্সড: এখানে unsafe_allow_html=True যোগ করা হয়েছে, যাতে কোড না এসে সরাসরি ভিজ্যুয়াল মেমো আসে
                st.markdown(invoice_html, unsafe_allow_html=True)
                
                b64_invoice = base64.b64encode(invoice_html.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64_invoice}" download="Invoice_{inv_custom_num}.html" style="display: block; text-align: center; background-color: #059669; color: white; padding: 12px; font-weight: bold; text-decoration: none; border-radius: 6px; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📥 Download 5"x7" Invoice File</a>'
                st.markdown(href, unsafe_allow_html=True)
