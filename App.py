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
# 🛑 ১. কাস্টম সুন্দর লগইন UI
# ==========================================
if not st.session_state.logged_in:
    # Header/Footer Hide & Login Styling
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer {visibility: hidden !important; height: 0px !important;}
            .main .block-container {padding: 0rem !important; max-width: 100% !important;}
            [data-testid="stAppViewContainer"] {
                background-color: #080d1a !important; 
                background-image: radial-gradient(circle at 50% 20%, rgba(0, 102, 255, 0.2) 0%, transparent 60%);
                padding: 0 !important;
            }
            
            div[data-testid="stForm"] {
                background: rgba(13, 22, 41, 0.95) !important;
                border: 1px solid #1e2e4a !important;
                border-radius: 28px !important;
                padding: 35px 25px !important;
                box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 20px rgba(0, 102, 255, 0.2) !important;
            }
            .stTextInput input {
                background-color: #0b1528 !important;
                border: 1.5px solid #1e3a5f !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                padding: 12px !important;
            }
            .stButton > button {
                background: linear-gradient(90deg, #0052cc 0%, #0066ff 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 25px !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 100px; height: 100px; border-radius: 50%; background: #ffffff; padding: 3px; 
                            box-shadow: 0 0 20px rgba(0, 102, 255, 0.5); border: 2px solid #0066ff; margin: 0 auto 15px auto;">
                    <img src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" 
                         style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">
                </div>
                <h2 style="color: #ffffff; font-size: 22px; font-weight: 800; margin: 0;">Welcome to <span style="color: #1e88e5;">SM-TECH</span></h2>
                <p style="color: #94a3b8; font-size: 11px; letter-spacing: 1.2px; font-weight: 600; text-transform: uppercase; margin-top: 4px;">COMPUTER & IT SOLUTIONS</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("main_login_form"):
            username = st.text_input("ইউজারনেম", value="admin", placeholder="আপনার ইউজারনেম")
            password = st.text_input("পাসওয়ার্ড", type="password", value="1234", placeholder="আপনার পাসওয়ার্ড")
            
            submit = st.form_submit_button("[➔] লগইন করুন", use_container_width=True)

            if submit:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! (ডিফল্ট: admin / 1234)")

        st.markdown("""
            <div style="text-align: center; font-size: 12px; color: #64748b; margin: 15px 0;">অথবা ওটিপি দিয়ে লগইন</div>
            <div style="display: flex; gap: 8px; justify-content: center; margin-bottom: 15px;">
                <div style="flex:1; padding: 8px; background: #0b1528; border: 1px solid #1e3a5f; border-radius: 10px; text-align: center; color: white; font-size: 12px;">🔴 Google</div>
                <div style="flex:1; padding: 8px; background: #0b1528; border: 1px solid #1e3a5f; border-radius: 10px; text-align: center; color: white; font-size: 12px;">🔵 Facebook</div>
                <div style="flex:1; padding: 8px; background: #0b1528; border: 1px solid #1e3a5f; border-radius: 10px; text-align: center; color: white; font-size: 12px;">✉️ ওটিপি</div>
            </div>
            <p style="text-align: center; font-size: 13px; color: #94a3b8;">একাউন্ট নেই? <a href="#" style="color: #38bdf8; font-weight: bold; text-decoration: none;">নিবন্ধন করুন (Sign Up)</a></p>
        """, unsafe_allow_html=True)

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড
# ==========================================
else:
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 15px;">
                <span style="font-size: 28px; margin-right: 10px; color: #38bdf8;">💻</span>
                <span style="font-size: 22px; font-weight: 900;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.write("### মেনু নির্বাচন করুন")
        
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

    # ১. ড্যাশবোর্ড
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

    # ২. কাস্টমার ও রিপেয়ার
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

    # ৩. স্টক পণ্য
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

    # ৪. পাসওয়ার্ড সংরক্ষণ
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

    # ৫. সেল ইনভয়েস (A5 পারফেক্ট ডিজাইনার ক্যাশ মেমো প্রিন্ট)
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 ইনভয়েস জেনারেটর")
        
        # ইনপুট ফিল্ড
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
            if st.button("🗑️ Clear All Items"):
                st.session_state.invoice_items = []
                st.rerun()

        sub_total = sum(item["Amount"] for item in st.session_state.invoice_items)
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        current_time_stamp = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
        
        # ১০ লাইনের গ্রিড টেবিল জেনারেট
        rows_html = ""
        max_rows = 10
        for i in range(max_rows):
            if i < len(st.session_state.invoice_items):
                item = st.session_state.invoice_items[i]
                rows_html += f"""
                <tr>
                    <td style="text-align:center;">{i+1}</td>
                    <td>{item['Description']}</td>
                    <td style="text-align:center;">{item['Qty']}</td>
                    <td style="text-align:right;">{item['Price']:,}</td>
                    <td style="text-align:right;">{item['Amount']:,}</td>
                </tr>
                """
            else:
                rows_html += """
                <tr>
                    <td>&nbsp;</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                """

        # সম্পূর্ণ ছবি সংসংক্রান্ত HTML+CSS A5 লেআউট
        invoice_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @page {{
                size: A5 portrait;
                margin: 0;
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 15px;
                background: #fff;
            }}
            .invoice-box {{
                border: 2px solid #0d47a1;
                padding: 12px;
                border-radius: 8px;
                position: relative;
                box-sizing: border-box;
                min-height: 94vh;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                border-bottom: 2px solid #0d47a1;
                padding-bottom: 8px;
            }}
            .logo-text {{
                font-size: 28px;
                font-weight: 900;
                color: #0d47a1;
                line-height: 1;
            }}
            .logo-sub {{
                font-size: 11px;
                font-weight: bold;
                color: #2e7d32;
                letter-spacing: 0.5px;
            }}
            .owner-info {{
                text-align: right;
                font-size: 11px;
                font-weight: bold;
                color: #0d47a1;
            }}
            .bill-sec {{
                margin-top: 10px;
                display: flex;
                justify-content: space-between;
                font-size: 12px;
            }}
            .invoice-title {{
                background: #0d47a1;
                color: white;
                padding: 2px 10px;
                font-weight: bold;
                border-radius: 3px;
                display: inline-block;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 11px;
            }}
            th {{
                background-color: #0d47a1;
                color: white;
                border: 1px solid #0d47a1;
                padding: 6px;
            }}
            td {{
                border: 1px solid #0d47a1;
                padding: 5px;
                height: 18px;
            }}
            .footer-sec {{
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                font-size: 11px;
            }}
            .payment-methods {{
                border: 1px solid #0d47a1;
                padding: 4px 8px;
                font-weight: bold;
                font-size: 10px;
            }}
            .print-btn-container {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .btn-print {{
                background: #0066ff;
                color: white;
                border: none;
                padding: 10px 25px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }}
            @media print {{
                .print-btn-container {{ display: none !important; }}
                body {{ padding: 0; }}
            }}
        </style>
        </head>
        <body>

        <div class="print-btn-container">
            <button class="btn-print" onclick="window.print()">🖨️ প্রিন্ট করুন / Save as PDF (A5)</button>
        </div>

        <div class="invoice-box">
            <div class="header">
                <div>
                    <div class="logo-text">SM-TECH</div>
                    <div class="logo-sub">COMPUTER & IT SOLUTION</div>
                    <div style="font-size: 9px; color: #333;">Smart Technology-Trusted Service</div>
                </div>
                <div class="owner-info">
                    <div style="font-size: 13px; font-weight: bold;">S.m. Ibrahim</div>
                    <div>Owner</div>
                    <div>01940-556114</div>
                    <div>01810-499166</div>
                </div>
            </div>

            <div class="bill-sec">
                <div>
                    <b>Bill To Name:</b> {cust_name}<br>
                    <b>Address:</b> {cust_address}
                </div>
                <div style="text-align: right;">
                    <span class="invoice-title">INVOICE</span><br>
                    <b>Invoice No:</b> {inv_custom_num}<br>
                    <b>Date:</b> {current_date}
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 8%;">S.L</th>
                        <th style="width: 48%;">DESCRIPTION</th>
                        <th style="width: 10%;">QTY</th>
                        <th style="width: 17%;">U.PRICE</th>
                        <th style="width: 17%;">AMOUNT</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr>
                        <td colspan="3" style="border:none;"><b>Amount In Words:</b> ..................................................</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">SUB TOTAL</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">{sub_total:,}</td>
                    </tr>
                </tbody>
            </table>

            <div class="footer-sec">
                <div>
                    <div class="payment-methods">
                        Payment Methods<br>
                        Cash | Bkash | Nagad | Bank
                    </div>
                </div>
                <div style="text-align: center;">
                    ------------------------------------------<br>
                    <b>Authorised Signature</b><br>
                    <span style="font-size: 9px;">SM-TECH Computer & IT Solutions</span>
                </div>
            </div>

            <div style="position: absolute; bottom: 5px; left: 12px; right: 12px; display: flex; justify-content: space-between; font-size: 8px; color: #555;">
                <span>Print Date: {current_time_stamp}</span>
                <span>Website: smtech.com.bd</span>
            </div>
        </div>

        </body>
        </html>
        """

        st.components.v1.html(invoice_template, height=750, scrolling=True)
