import streamlit as st
import pandas as pd
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide", page_icon="💻")

# ==========================================
# 🔢 সংখ্যা থেকে কথায় (Amount in Words)
# ==========================================
def number_to_words_en(n):
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    if n == 0: return "Zero Taka Only"
    def convert_below_thousand(num):
        if num < 20: return units[num]
        elif num < 100: return tens[num // 10] + (" " + units[num % 10] if num % 10 != 0 else "")
        else: return units[num // 100] + " Hundred" + (" " + convert_below_thousand(num % 100) if num % 100 != 0 else "")

    def convert(num):
        if num < 1000: return convert_below_thousand(num)
        elif num < 100000: return convert_below_thousand(num // 1000) + " Thousand" + (" " + convert_below_thousand(num % 1000) if num % 1000 != 0 else "")
        elif num < 10000000: return convert_below_thousand(num // 100000) + " Lakh" + (" " + convert(num % 100000) if num % 100000 != 0 else "")
        else: return convert_below_thousand(num // 10000000) + " Crore" + (" " + convert(num % 10000000) if num % 10000000 != 0 else "")

    return convert(int(n)).strip() + " Taka Only"

def number_to_words_bn(n):
    if n == 0: return "শূন্য টাকা মাত্র"
    en_words = number_to_words_en(n)
    return f"{n:,} টাকা মাত্র ({en_words})"

# ==========================================
# 🔐 সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

if "language" not in st.session_state:
    st.session_state.language = "Bangla"

if "inv_language" not in st.session_state:
    st.session_state.inv_language = "Bangla"

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
# 🌐 ডিকশনারি (বাংলা ও ইংরেজি)
# ==========================================
t = {
    "Bangla": {
        "title_dash": "🖥️ ড্যাশবোর্ড",
        "title_cust": "👥 কাস্টমার বাকির হিসাব",
        "title_stock": "📦 স্টক পণ্য ম্যানেজমেন্ট",
        "title_pass": "🔐 পাসওয়ার্ড সংরক্ষণ",
        "title_inv": "🧾 ইনভয়েস জেনারেটর",
        "menu_dash": "⬜ ড্যাশবোর্ড",
        "menu_cust": "👥 কাস্টমার ও রিপেয়ার",
        "menu_stock": "📦 স্টক প্রোডাক্ট",
        "menu_inv": "💵 সেল ইনভয়েস",
        "menu_pass": "🔐 পাসওয়ার্ড সেভ",
        "total_cust": "মোট কাস্টমার",
        "total_due": "মোট বাকি টাকা",
        "stock_val": "স্টক পণ্যের মূল্য",
        "cust_dir": "কাস্টমার ডিরেক্টরি & রিসেন্ট এন্ট্রি",
        "logout": "🔒 লগআউট"
    },
    "English": {
        "title_dash": "🖥️ Dashboard",
        "title_cust": "👥 Customer & Repair Dues",
        "title_stock": "📦 Stock Product Management",
        "title_pass": "🔐 Password Manager",
        "title_inv": "🧾 Invoice Generator",
        "menu_dash": "⬜ Dashboard",
        "menu_cust": "👥 Customer & Repair",
        "menu_stock": "📦 Stock Product",
        "menu_inv": "💵 Sell Invoice",
        "menu_pass": "🔐 Password Save",
        "total_cust": "Total Customers",
        "total_due": "Total Due Amount",
        "stock_val": "Total Stock Value",
        "cust_dir": "Customer Directory & Recent Entries",
        "logout": "Logout"
    }
}

inv_labels = {
    "Bangla": {
        "bill_to": "বিল প্রাপক:",
        "address": "ঠিকানা:",
        "inv_title": "INVOICE",
        "inv_no": "ইনভয়েস নং:",
        "date": "তারিখ:",
        "sl": "ক্রঃ নং",
        "desc": "বিবরণ",
        "qty": "পরিমাণ",
        "price": "দর",
        "amount": "মোট টাকা",
        "words": "কথায়:",
        "subtotal": "মোট (SUB TOTAL)",
        "pay_meth": "PAYMENT METHODS",
        "auth_sig": "অনুমোদিত স্বাক্ষর (Authorised Signature)",
        "print_btn": "🖨️ প্রিন্ট করুন / Save as PDF (A5)"
    },
    "English": {
        "bill_to": "Bill To Name:",
        "address": "Address:",
        "inv_title": "INVOICE",
        "inv_no": "Invoice No:",
        "date": "Date:",
        "sl": "S.L",
        "desc": "DESCRIPTION",
        "qty": "QTY",
        "price": "U.PRICE",
        "amount": "AMOUNT",
        "words": "Amount In Words:",
        "subtotal": "SUB TOTAL",
        "pay_meth": "PAYMENT METHODS",
        "auth_sig": "Authorised Signature",
        "print_btn": "🖨️ Print / Save as PDF (A5)"
    }
}

lang = st.session_state.language
curr_t = t[lang]

# ==========================================
# 🛑 ১. লগইন UI
# ==========================================
if not st.session_state.logged_in:
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
            username = st.text_input("ইউজারনেম / Username", value="admin")
            password = st.text_input("পাসওয়ার্ড / Password", type="password", value="1234")
            submit = st.form_submit_button("[➔] Login / লগইন", use_container_width=True)

            if submit:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password!")

# ==========================================
# 🔓 ২. মূল অ্যাপ
# ==========================================
else:
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 15px;">
                <span style="font-size: 28px; margin-right: 10px; color: #38bdf8;">💻</span>
                <span style="font-size: 22px; font-weight: 900;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        selected_lang = st.selectbox("🌐 System Language / ভাষা", ["Bangla", "English"], index=0 if st.session_state.language == "Bangla" else 1)
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

        if st.button(curr_t["logout"], key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.write("### Menu / মেনু")
        
        if st.button(curr_t["menu_dash"], use_container_width=True):
            st.session_state.current_menu = "Dashboard"; st.rerun()
        if st.button(curr_t["menu_cust"], use_container_width=True):
            st.session_state.current_menu = "Customer & Repair"; st.rerun()
        if st.button(curr_t["menu_stock"], use_container_width=True):
            st.session_state.current_menu = "Stock product"; st.rerun()
        if st.button(curr_t["menu_inv"], use_container_width=True):
            st.session_state.current_menu = "Sell Invoice"; st.rerun()
        if st.button(curr_t["menu_pass"], use_container_width=True):
            st.session_state.current_menu = "Password Save"; st.rerun()

    # ১. ড্যাশবোর্ড
    if st.session_state.current_menu == "Dashboard":
        st.title(curr_t["title_dash"])
        st.write("---")
        col1, col2, col3 = st.columns(3)
        total_due = sum(item.get("বাকি", 0) for item in st.session_state.customer_dues)
        total_stock = sum(item.get("মোট টাকা", 0) for item in st.session_state.shop_stock)
        col1.metric(curr_t["total_cust"], f"{len(st.session_state.customer_dues)}")
        col2.metric(curr_t["total_due"], f"{total_due} BDT")
        col3.metric(curr_t["stock_val"], f"{total_stock} BDT")
        st.write("<br>", unsafe_allow_html=True)
        st.subheader(curr_t["cust_dir"])
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True)

    # ২. কাস্টমার ও রিপেয়ার
    elif st.session_state.current_menu == "Customer & Repair":
        st.title(curr_t["title_cust"])
        with st.form("Add Customer Due", clear_on_submit=True):
            c_name = st.text_input("কাস্টমার নাম / Name")
            c_desc = st.text_input("কাজের বিবরণ / Work Description")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1: c_qty = st.number_input("পরিমান / Qty", min_value=1, value=1)
            with col_c2: c_price = st.number_input("দর / Rate (TK)", min_value=0, value=0)
            with col_c3: c_paid = st.number_input("আদায় / Paid (TK)", min_value=0, value=0)
            if st.form_submit_button("💾 Save / সংরক্ষণ করুন") and c_name:
                st.session_state.customer_dues.append({
                    "ক্রমিক নং": len(st.session_state.customer_dues) + 1, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
                    "পরিমান": c_qty, "দর": c_price, "মোট টাকা": c_qty*c_price, "আদায়": c_paid, "বাকি": (c_qty*c_price)-c_paid
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.customer_dues), use_container_width=True)

    # ৩. স্টক পণ্য
    elif st.session_state.current_menu == "Stock product":
        st.title(curr_t["title_stock"])
        with st.form("Add Shop Stock", clear_on_submit=True):
            s_desc = st.text_input("পণ্যের বিবরণ / Item Name")
            col_s1, col_s2 = st.columns(2)
            with col_s1: s_qty = st.number_input("পরিমান / Qty", min_value=1, value=1)
            with col_s2: s_price = st.number_input("দর / Price", min_value=0, value=0)
            if st.form_submit_button("📥 Add / যোগ করুন") and s_desc:
                st.session_state.shop_stock.append({
                    "ক্রমিক নং": len(st.session_state.shop_stock) + 1, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": s_qty*s_price
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.shop_stock), use_container_width=True)

    # ৪. পাসওয়ার্ড সংরক্ষণ
    elif st.session_state.current_menu == "Password Save":
        st.title(curr_t["title_pass"])
        with st.form("Add Password", clear_on_submit=True):
            inst_name = st.text_input("প্রতিষ্ঠানের নাম / Institution Name")
            col_p1, col_p2 = st.columns(2)
            with col_p1: entry_pass = st.text_input("এন্ট্রি পাসওয়ার্ড / Entry Password")
            with col_p2: confirm_pass = st.text_input("কনফার্ম পাসওয়ার্ড / Confirm Password")
            if st.form_submit_button("💾 Save / সংরক্ষণ করুন") and inst_name:
                st.session_state.saved_passwords.append({
                    "ক্রমিক নং": len(st.session_state.saved_passwords) + 1, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True)

    # ৫. সেল ইনভয়েস
    elif st.session_state.current_menu == "Sell Invoice":
        st.title(curr_t["title_inv"])
        
        col_in1, col_in2, col_in3 = st.columns([1.5, 2, 2])
        with col_in1: inv_custom_num = st.text_input("Invoice No", value=f"SM-TECH/{datetime.datetime.now().strftime('%y/%m/%d')}")
        with col_in2: cust_name = st.text_input("Customer Name / কাস্টমারের নাম", value="Super, Kharamura Islamia Dakhil Madrasah")
        with col_in3: cust_address = st.text_input("Address / ঠিকানা", value="Sreebardi")
            
        col_item1, col_item2, col_item3 = st.columns([3, 1, 1.5])
        with col_item1: prod_desc = st.text_input("Product Name / Description", value="এসএসডি")
        with col_item2: prod_qty = st.number_input("QTY", min_value=1, value=1)
        with col_item3: prod_price = st.number_input("Unit Price", min_value=0, value=1500)
            
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("➕ আইটেম যুক্ত করুন / Add Item", use_container_width=True) and prod_desc:
                st.session_state.invoice_items.append({
                    "Description": prod_desc, "Qty": prod_qty, "Price": prod_price, "Amount": prod_qty * prod_price
                })
                st.rerun()
        with col_btn2:
            if st.session_state.invoice_items:
                if st.button("🗑️ সব মুছে ফেলুন / Clear All", use_container_width=True):
                    st.session_state.invoice_items = []
                    st.rerun()

        st.write("---")
        
        # 🔘 ইনভয়েসের ভাষা সিলেক্টর
        inv_lang_choice = st.radio(
            "🌐 **ইনভয়েসের ভাষা নির্বাচন করুন (Click to switch Invoice Language):**",
            ["🇧🇩 বাংলা (Bangla)", "🇬🇧 English"],
            horizontal=True,
            index=0 if st.session_state.inv_language == "Bangla" else 1
        )
        st.session_state.inv_language = "Bangla" if "🇧🇩" in inv_lang_choice else "English"
        
        i_lang = st.session_state.inv_language
        cur_inv = inv_labels[i_lang]

        sub_total = sum(item["Amount"] for item in st.session_state.invoice_items)
        amount_in_words = number_to_words_bn(sub_total) if i_lang == "Bangla" else number_to_words_en(sub_total)
        
        # ১০ লাইনের টেবিল
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

        # HTML ইনভয়েস লেআউট (রিয়েল-টাইম স্ক্রিপ্টসহ)
        invoice_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            @page {{
                size: A5 portrait;
                margin: 0;
            }}
            body {{
                font-family: 'Noto Sans Bengali', Arial, sans-serif;
                margin: 0;
                padding: 12px;
                background: #fff;
                color: #0d47a1;
            }}
            .invoice-box {{
                border: 2.5px solid #0d47a1;
                padding: 12px;
                border-radius: 8px;
                position: relative;
                box-sizing: border-box;
                min-height: 95vh;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2.5px solid #0d47a1;
                padding-bottom: 8px;
            }}
            .logo-section {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .logo-img {{
                width: 95px;
                height: 95px;
                border-radius: 50%;
                background: #ffffff;
                object-fit: contain;
                border: 2px solid #0d47a1;
                box-shadow: 0 2px 5px rgba(0,0,0,0.15);
            }}
            .logo-text {{
                font-size: 56px;
                font-weight: 900;
                color: #0d47a1;
                line-height: 0.85;
                transform: scaleX(1.15);
                transform-origin: left;
                display: inline-block;
                letter-spacing: 1px;
            }}
            .logo-sub {{
                font-size: 14px;
                font-weight: 800;
                color: #0d47a1;
                letter-spacing: 0.8px;
                margin-top: 5px;
            }}
            .owner-info {{
                text-align: right;
                color: #0d47a1;
            }}
            .owner-name {{
                font-size: 20px;
                font-weight: 900;
                margin-bottom: 1px;
            }}
            .owner-title {{
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 4px;
            }}
            .owner-phone {{
                font-size: 13px;
                font-weight: bold;
                line-height: 1.3;
            }}
            .bill-sec {{
                margin-top: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #0d47a1;
            }}
            .invoice-middle-badge {{
                text-align: center;
                flex-grow: 1;
            }}
            .invoice-title {{
                background: #0d47a1;
                color: white;
                padding: 4px 18px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
                display: inline-block;
                letter-spacing: 1px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 12px;
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
                color: #0d47a1;
            }}
            .footer-sec {{
                position: absolute;
                bottom: 28px;
                left: 12px;
                right: 12px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                font-size: 11px;
                color: #0d47a1;
            }}
            .payment-methods {{
                border: 1.5px solid #0d47a1;
                padding: 6px 10px;
                font-size: 11px;
                color: #0d47a1;
                border-radius: 4px;
                background: #ffffff;
                width: 280px;
            }}
            .pay-title {{
                font-size: 10.5px;
                font-weight: 800;
                text-transform: uppercase;
                margin-bottom: 5px;
                border-bottom: 1px dashed #0d47a1;
                padding-bottom: 3px;
                letter-spacing: 0.5px;
            }}
            .pay-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4px 10px;
                font-weight: bold;
                font-size: 11px;
            }}
            .pay-item {{
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .pay-logo-img {{
                height: 16px;
                width: auto;
                object-fit: contain;
            }}
            .print-btn-container {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .btn-print {{
                background: #0d47a1;
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
            <button class="btn-print" onclick="triggerPrint()">{cur_inv['print_btn']}</button>
        </div>

        <div class="invoice-box">
            <div class="header">
                <div class="logo-section">
                    <img class="logo-img" src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH Logo">
                    <div>
                        <div class="logo-text">SM-TECH</div>
                        <div class="logo-sub">COMPUTER & IT SOLUTION</div>
                        <div style="font-size: 10px; color: #0d47a1; font-weight: bold; margin-top: 2px;">Smart Technology-Trusted Service</div>
                    </div>
                </div>
                <div class="owner-info">
                    <div class="owner-name">S.m. Ibrahim</div>
                    <div class="owner-title">Owner</div>
                    <div class="owner-phone">💬 01940-556114</div>
                    <div class="owner-phone">💬 01810-499166</div>
                </div>
            </div>

            <div class="bill-sec">
                <div style="width: 38%;">
                    <b>{cur_inv['bill_to']}</b> {cust_name}<br>
                    <b>{cur_inv['address']}</b> {cust_address}
                </div>
                
                <div class="invoice-middle-badge">
                    <span class="invoice-title">{cur_inv['inv_title']}</span>
                </div>

                <div style="text-align: right; width: 32%;">
                    <b>{cur_inv['inv_no']}</b> {inv_custom_num}<br>
                    <b>{cur_inv['date']}</b> <span id="real-time-date"></span>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 8%;">{cur_inv['sl']}</th>
                        <th style="width: 48%;">{cur_inv['desc']}</th>
                        <th style="width: 10%;">{cur_inv['qty']}</th>
                        <th style="width: 17%;">{cur_inv['price']}</th>
                        <th style="width: 17%;">{cur_inv['amount']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr>
                        <td colspan="3" style="border:1px solid #0d47a1;"><b>{cur_inv['words']}</b> {amount_in_words}</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">{cur_inv['subtotal']}</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">{sub_total:,}</td>
                    </tr>
                </tbody>
            </table>

            <div class="footer-sec">
                <div>
                    <div class="payment-methods">
                        <div class="pay-title">{cur_inv['pay_meth']}</div>
                        <div class="pay-grid">
                            <div class="pay-item">1. 💵 Cash</div>
                            <div class="pay-item">
                                2. <img src="https://raw.githubusercontent.com/freelogovectors/bKash-Logo-PNG/main/bKash-Logo.png" class="pay-logo-img" alt="bKash"> Bkash
                            </div>
                            <div class="pay-item">
                                3. <img src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" class="pay-logo-img" alt="Nagad"> Nagad
                            </div>
                            <div class="pay-item">
                                4. <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/AB_Bank_Logo.svg/1200px-AB_Bank_Logo.svg.png" class="pay-logo-img" alt="AB Bank"> AB Bank
                            </div>
                        </div>
                    </div>
                </div>
                <div style="text-align: center;">
                    ------------------------------------------<br>
                    <b>{cur_inv['auth_sig']}</b><br>
                    <span style="font-size: 9px;">SM-TECH Computer & IT Solutions</span>
                </div>
            </div>

            <div style="position: absolute; bottom: 5px; left: 12px; right: 12px; display: flex; justify-content: space-between; font-size: 8px; color: #0d47a1; font-weight: bold;">
                <span>Print Date: <span id="real-time-stamp"></span></span>
                <span>Website: smtech.com.bd</span>
            </div>
        </div>

        <!-- Real-Time Date & Time JavaScript Script -->
        <script>
            function updateDateTime() {{
                const now = new Date();
                
                // ১. তারিখ জেনারেট (DD/MM/YYYY)
                const day = String(now.getDate()).padStart(2, '0');
                const month = String(now.getMonth() + 1).padStart(2, '0');
                const year = now.getFullYear();
                const formattedDate = `${{day}}/${{month}}/${{year}}`;
                
                // ২. রিয়েল টাইম স্ট্যাম্প জেনারেট (DD-MMM-YYYY HH:MM AM/PM)
                const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                const monthName = monthNames[now.getMonth()];
                let hours = now.getHours();
                const minutes = String(now.getMinutes()).padStart(2, '0');
                const ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // 0 কে 12 করা
                const formattedHours = String(hours).padStart(2, '0');
                
                const formattedTimeStamp = `${{day}}-${{monthName}}-${{year}} ${{formattedHours}}:${{minutes}} ${{ampm}}`;

                // HTML এ সেট করা
                document.getElementById('real-time-date').innerText = formattedDate;
                document.getElementById('real-time-stamp').innerText = formattedTimeStamp;
            }}

            // পেজ লোড হলে সময় সেট
            updateDateTime();

            // প্রিন্ট করার মুহূর্তে সময় তাজা রাখার জন্য
            function triggerPrint() {{
                updateDateTime();
                window.print();
            }}
        </script>

        </body>
        </html>
        """

        st.components.v1.html(invoice_template, height=780, scrolling=True)
