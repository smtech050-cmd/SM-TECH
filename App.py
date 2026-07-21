import streamlit as st
import pandas as pd
import datetime
import base64
import streamlit.components.v1 as components

# PWA elements injection
components.html(
    """
    <script>
        var link = document.createElement('link');
        link.rel = 'manifest';
        link.href = 'https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/manifest.json';
        document.head.appendChild(link);

        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/sw.js')
            .then(function(reg) { console.log('SW Registered'); })
            .catch(function(err) { console.log('SW Failed', err); });
        }
    </script>
    """,
    height=0,
)

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH | Admin System", layout="wide")

# ==========================================
# 🔢 সংখ্যাকে কথায় রূপান্তর করার ফাংশন
# ==========================================
def number_to_words(number):
    words = {
        0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
        10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen',
        17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50: 'Fifty',
        60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety'
    }
    if number == 0:
        return 'Zero'
    
    if number < 20:
        return words[number]
    elif number < 100:
        return words[number // 10 * 10] + (' ' + words[number % 10] if number % 10 > 0 else '')
    elif number < 1000:
        return words[number // 100] + ' Hundred' + (' and ' + number_to_words(number % 100) if number % 100 > 0 else '')
    elif number < 100000:
        return number_to_words(number // 1000) + ' Thousand' + (' ' + number_to_words(number % 1000) if number % 1000 > 0 else '')
    elif number < 10000000:
        return number_to_words(number // 100000) + ' Lakh' + (' ' + number_to_words(number % 100000) if number % 100000 > 0 else '')
    else:
        return str(number)

# ==========================================
# 🔐 লগইন ও সেশন স্টেট ইনিশিয়ালাইজেশন
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "lang" not in st.session_state:
    st.session_state.lang = "English"

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"ক্রমাঙ্ক নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200}
    ]

if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"ক্রমাঙ্ক নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000}
    ]

if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = [
        {"ক্রমাঙ্ক নং": 1, "শিক্ষা প্রতিষ্ঠানের নাম": "Sreebardi Govt. College", "এন্ট্রি পাসওয়ার্ড": "sreebardi@2026", "কনফার্ম পাসওয়ার্ড": "board@xyz2026"}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🌐 ভাষার অভিধান (Language Dictionary)
# ==========================================
text_translations = {
    "English": {
        "welcome": "WELCOME",
        "tagline": "Smart Technology, Trusted Service.",
        "signin_title": "Sign in",
        "signin_sub": "Please sign in to admin system",
        "user_label": "User Name",
        "user_place": "Username...",
        "pass_label": "Password",
        "pass_place": "Password...",
        "btn_login": "Sign in",
        "err_msg": "Invalid Username or Password!",
        "succ_msg": "Login Successful!"
    },
    "Bangla": {
        "welcome": "স্বাগতম",
        "tagline": "স্মার্ট টেকনোলজি, বিশ্বস্ত সেবা।",
        "signin_title": "সাইন-ইন করুন",
        "signin_sub": "এডমিন সিস্টেমে প্রবেশ করতে সাইন-ইন করুন",
        "user_label": "ব্যবহারকারীর নাম",
        "user_place": "ইউজারনেম লিখুন...",
        "pass_label": "পাসওয়ার্ড",
        "pass_place": "পাসওয়ার্ড লিখুন...",
        "btn_login": "লগইন করুন",
        "err_msg": "ভুল ইউজারনেম অথবা পাসওয়ার্ড!",
        "succ_msg": "লগইন সফল হয়েছে!"
    }
}

# ==========================================
# 🛑 ১. ইমেজ স্টাইল লগইন স্ক্রিন
# ==========================================
if not st.session_state.logged_in:
    login_css = """
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        [data-testid="stHeader"] {
            display: none;
        }
        .main .block-container {
            max-width: 950px !important;
            padding: 0rem !important;
            margin: auto;
        }
        
        /* কন্টেইনার কার্ড */
        .login-card {
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            overflow: hidden;
            display: flex;
            min-height: 520px;
        }

        /* বাম পাশের নীল ডিজাইন */
        .left-banner {
            background: linear-gradient(135deg, #024ebb 0%, #0072ff 100%);
            border-radius: 20px;
            padding: 45px 35px;
            color: white;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 500px;
        }

        /* ছবির মতো ব্যাকগ্রাউন্ড সার্কেল ডিজাইন */
        .circle-1 {
            position: absolute;
            width: 260px;
            height: 260px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 50%;
            top: -50px;
            left: -50px;
        }
        .circle-2 {
            position: absolute;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            bottom: -40px;
            right: 10px;
        }

        .welcome-text h2 {
            font-size: 38px;
            font-weight: 900;
            margin: 0;
            color: #ffffff !important;
            letter-spacing: 1px;
        }
        .welcome-text h4 {
            font-size: 16px;
            font-weight: 700;
            margin-top: 5px;
            color: #e0f2fe !important;
        }
        .welcome-text p {
            font-size: 13px;
            opacity: 0.85;
            margin-top: 10px;
            line-height: 1.5;
            color: #f0f9ff !important;
        }

        /* ডান পাশের ফর্মের টেক্সট ও ফিল্ড স্টাইলিং */
        .stSelectbox label, .stTextInput label {
            color: #334155 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }

        /* ইনপুট ফিল্ডকে ছবির মতো হালকা ধূসর করা */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: #f1f5f9 !important;
            border-radius: 10px !important;
            border: 1px solid #e2e8f0 !important;
        }
        .stTextInput input {
            color: #1e293b !important;
            background-color: transparent !important;
            font-size: 15px !important;
        }
        
        /* বাটন স্টাইলিং (গাঢ় নীল) */
        div.stButton > button {
            background-color: #0a47a3 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0px 4px 12px rgba(10, 71, 163, 0.3) !important;
        }
        div.stButton > button:hover {
            background-color: #083780 !important;
        }
        
        .form-title {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 2px;
        }
        .form-subtitle {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(login_css, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1.15])
    
    t = text_translations[st.session_state.lang]
    
    with col_left:
        st.markdown(
            f"""
            <div class="left-banner">
                <div class="circle-1"></div>
                <div class="circle-2"></div>
                <div class="welcome-text" style="position: relative; z-index: 2;">
                    <h2>{t['welcome']}</h2>
                    <h4>SM-TECH COMPUTER & IT</h4>
                    <p>{t['tagline']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            f"""
            <div style="padding: 10px 10px 0px 10px;">
                <div class="form-title">{t['signin_title']}</div>
                <div class="form-subtitle">{t['signin_sub']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # ভাষা পরিবর্তনের ড্রপডাউন
        selected_lang = st.selectbox(
            "🌐 Select Language / ভাষা নির্বাচন করুন",
            ["English", "Bangla"],
            index=0 if st.session_state.lang == "English" else 1,
            key="lang_select"
        )
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()

        username = st.text_input(t["user_label"], placeholder=t["user_place"], key="login_user")
        password = st.text_input(t["pass_label"], type="password", placeholder=t["pass_place"], key="login_pass")
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        if st.button(t["btn_login"], use_container_width=True):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success(t["succ_msg"])
                st.rerun()
            else:
                st.error(t["err_msg"])

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড স্ক্রিন
# ==========================================
else:
    # ড্যাশবোর্ডের ভিতরের স্টাইল (সবুজ থিম)
    dashboard_css = """
    <style>
        [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #f4f7fb !important;
            color: #111111 !important;
        }
        div.stButton > button {
            background-color: #1b5e20 !important;
            color: #ffffff !important;
        }
    </style>
    """
    st.markdown(dashboard_css, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 15px; margin-bottom: 15px; padding-left: 5px;">
                <span style="font-size: 32px; margin-right: 12px; color: #1b5e20;">⚙️</span>
                <span style="font-size: 30px; font-weight: 900; color: #1b5e20; letter-spacing: 0.5px;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h3 style='color:#1b5e20; font-size:20px; font-weight:bold; margin-left:5px; margin-bottom:15px;'>মেনু নির্বাচন করুন</h3>", unsafe_allow_html=True)
        
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
                    "ক্রমাঙ্ক নং": len(st.session_state.customer_dues) + 1, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
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
                    "ক্রমাঙ্ক নং": len(st.session_state.shop_stock) + 1, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": s_qty*s_price
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
                    "ক্রমাঙ্ক নং": len(st.session_state.saved_passwords) + 1, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True)

    # সেল ইনভয়েস
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 ইনভয়েস")
        col_in1, col_in2, col_in3 = st.columns([1.8, 2, 2])
        with col_in1: inv_custom_num = st.text_input("Invoice No", value="SM-TECH/2026/08/01")
        with col_in2: cust_name = st.text_input("কাস্টমারের নাম", value="Salman")
        with col_in3: cust_address = st.text_input("Address", value="Dhaka, Bangladesh")
            
        col_item1, col_item2, col_item3 = st.columns([3, 1, 1.5])
        with col_item1: prod_desc = st.text_input("Product Name / Description", value="SSD")
        with col_item2: prod_qty = st.number_input("QTY", min_value=1, value=1)
        with col_item3: prod_price = st.number_input("Unit Price", min_value=0, value=500)
            
        if st.button("➕ Add Item", use_container_width=True):
            if prod_desc:
                st.session_state.invoice_items.append({
                    "Description": prod_desc, "Qty": prod_qty, "Price": prod_price, "Amount": prod_qty * prod_price
                })
                st.rerun()
                
        if st.session_state.invoice_items:
            st.dataframe(pd.DataFrame(st.session_state.invoice_items), use_container_width=True)
            
            total_amt = sum(item["Amount"] for item in st.session_state.invoice_items)
            amount_in_words = number_to_words(total_amt) + " BDT Only."
            
            table_rows = ""
            max_rows = 12
            for idx in range(max_rows):
                if idx < len(st.session_state.invoice_items):
                    item = st.session_state.invoice_items[idx]
                    table_rows += f"""
                    <tr class="item-row">
                        <td style="text-align: center;">{idx + 1}</td>
                        <td>{item['Description']}</td>
                        <td style="text-align: center;">{item['Qty']}</td>
                        <td style="text-align: right; padding-right: 8px;">{item['Price']}/-</td>
                        <td style="text-align: right; padding-right: 8px;">{item['Amount']}/-</td>
                    </tr>
                    """
                else:
                    table_rows += """
                    <tr class="item-row blank-row">
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    """
            
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>SM-TECH Invoice - {inv_custom_num}</title>
                <style>
                    @page {{
                        size: A5 portrait;
                        margin: 5mm;
                    }}
                    body {{
                        font-family: 'Arial', sans-serif;
                        color: #1b5e20;
                        font-size: 11px;
                        margin: 0;
                        padding: 0;
                        background-color: #fff;
                    }}
                    .pad-container {{
                        width: 138mm;
                        height: 195mm;
                        padding: 5mm;
                        box-sizing: border-box;
                        position: relative;
                        border: 2px solid #1b5e20;
                        margin: auto;
                    }}
                    .header-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 8px;
                    }}
                    .logo-block {{
                        display: flex;
                        align-items: center;
                    }}
                    .logo-block img {{
                        max-height: 52px;
                        width: auto;
                        margin-right: 10px;
                    }}
                    .logo-text-box {{
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    }}
                    .brand-title {{
                        font-size: 26px;
                        font-weight: 900;
                        color: #1b5e20;
                        line-height: 1;
                        letter-spacing: 0.5px;
                        margin: 0;
                    }}
                    .brand-subtitle {{
                        font-size: 9px;
                        font-weight: bold;
                        color: #2e7d32;
                        letter-spacing: 0.3px;
                        margin-top: 2px;
                    }}
                    .brand-tagline {{
                        font-size: 10px;
                        font-weight: bold;
                        color: #2e7d32;
                        margin-top: 3px;
                    }}
                    .owner-info {{
                        text-align: right;
                        font-size: 11px;
                        color: #1b5e20;
                        line-height: 1.3;
                        vertical-align: top;
                    }}
                    .owner-name {{
                        font-size: 14px;
                        font-weight: bold;
                    }}
                    .bill-section {{
                        width: 100%;
                        margin-bottom: 10px;
                        margin-top: 5px;
                    }}
                    .bill-to-badge {{
                        background-color: #1b5e20;
                        color: white;
                        padding: 2px 6px;
                        font-weight: bold;
                        border-radius: 3px 3px 0 0;
                        display: inline-block;
                    }}
                    .invoice-badge {{
                        background-color: #1b5e20;
                        color: white;
                        padding: 3px 12px;
                        font-weight: bold;
                        letter-spacing: 1px;
                        font-size: 13px;
                        float: right;
                    }}
                    .customer-details {{
                        width: 100%;
                        margin-top: 4px;
                        border-collapse: collapse;
                    }}
                    .customer-details td {{
                        padding-bottom: 6px;
                        vertical-align: bottom;
                        font-size: 11px;
                        color: #1b5e20;
                    }}
                    .dot-line {{
                        border-bottom: 1px dotted #1b5e20;
                        padding-bottom: 1px;
                        color: #1b5e20;
                    }}
                    .main-table {{
                        width: 100%;
                        border-collapse: collapse;
                        border: 1px solid #1b5e20;
                    }}
                    .main-table th {{
                        background-color: #1b5e20;
                        color: white;
                        font-weight: bold;
                        text-align: center;
                        padding: 5px;
                        font-size: 11px;
                        border: 1px solid #1b5e20;
                    }}
                    .item-row td {{
                        border-left: 1px solid #1b5e20;
                        border-right: 1px solid #1b5e20;
                        border-bottom: 1px solid #e0e0e0;
                        padding: 5px;
                        height: 22px;
                        color: #1b5e20;
                    }}
                    .blank-row td {{
                        height: 22px;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    .subtotal-box {{
                        background-color: #1b5e20;
                        color: white;
                        font-weight: bold;
                        padding: 5px;
                        text-align: center;
                    }}
                    .amount-words {{
                        margin-top: 10px;
                        color: #1b5e20;
                        font-weight: bold;
                        font-size: 11px;
                    }}
                    .words-text {{
                        color: #1b5e20;
                        font-weight: bold;
                        border-bottom: 1px dotted #1b5e20;
                    }}
                    .footer-section {{
                        position: absolute;
                        bottom: 5mm;
                        left: 5mm;
                        right: 5mm;
                        width: 92%;
                    }}
                    .payment-methods-box {{
                        border: 1px solid #1b5e20;
                        display: inline-block;
                        width: 58%;
                        vertical-align: bottom;
                        border-radius: 4px;
                        overflow: hidden;
                    }}
                    .pm-title {{
                        background-color: #1b5e20;
                        color: white;
                        font-weight: bold;
                        padding: 4px;
                        font-size: 11px;
                        text-align: center;
                    }}
                    .pm-options-container {{
                        padding: 6px 4px;
                        text-align: center;
                        background-color: #ffffff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 10px;
                    }}
                    .method-item {{
                        display: flex;
                        align-items: center;
                        font-size: 10px;
                        font-weight: bold;
                        color: #1b5e20;
                    }}
                    .method-icon {{
                        height: 14px;
                        width: auto;
                        margin-right: 3px;
                        vertical-align: middle;
                    }}
                    .signature-block {{
                        float: right;
                        text-align: center;
                        width: 38%;
                        margin-top: 15px;
                        color: #1b5e20;
                    }}
                    .sig-line {{
                        border-top: 1px solid #1b5e20;
                        margin-bottom: 4px;
                    }}
                </style>
            </head>
            <body onload="window.print();">
                <div class="pad-container">
                    <table class="header-table">
                        <tr>
                            <td style="width: 65%; vertical-align: top;">
                                <div class="logo-block">
                                    <img src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH">
                                    <div class="logo-text-box">
                                        <div class="brand-title">SM-TECH</div>
                                        <div class="brand-subtitle">COMPUTER & IT SOLUTION</div>
                                        <div class="brand-tagline">Smart Technology-Trusted Service</div>
                                    </div>
                                </div>
                            </td>
                            <td class="owner-info">
                                <span class="owner-name">S.m. Ibrahim</span><br>
                                Owner<br>
                                01940-556114<br>
                                01810-499166
                            </td>
                        </tr>
                    </table>
                    
                    <div class="bill-section">
                        <span class="bill-to-badge">Bill To</span>
                        <span class="invoice-badge">INVOICE</span>
                        
                        <table class="customer-details">
                            <tr>
                                <td style="width: 52%;"><strong>Name:</strong> <span class="dot-line">{cust_name}</span></td>
                                <td style="width: 48%;"><strong>Invoice No:</strong> <span class="dot-line" style="font-size: 10px;">{inv_custom_num}</span></td>
                            </tr>
                            <tr>
                                <td><strong>Address:</strong> <span class="dot-line">{cust_address}</span></td>
                                <td><strong>Date:</strong> <span class="dot-line">{datetime.date.today().strftime('%d-%m-%Y')}</span></td>
                            </tr>
                        </table>
                    </div>
                    
                    <table class="main-table">
                        <thead>
                            <tr>
                                <th style="width: 8%;">S.L</th>
                                <th style="width: 50%;">DESCRIPTION</th>
                                <th style="width: 10%;">QTY</th>
                                <th style="width: 14%;">U.PRICE</th>
                                <th style="width: 18%;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td class="subtotal-box">SUB TOTAL</td>
                                <td style="text-align: right; padding-right: 8px; font-weight: bold; border: 1px solid #1b5e20; background-color: #e8f5e9; color:#1b5e20;">{total_amt}/-</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="amount-words">
                        Amount In Words: <span class="words-text">{amount_in_words}</span>
                    </div>
                    
                    <div class="footer-section">
                        <div class="payment-methods-box">
                            <div class="pm-title">Payment Methods</div>
                            <div class="pm-options-container">
                                <div class="method-item">
                                    <img class="method-icon" src="https://img.icons8.com/color/48/banknotes.png" alt="Cash"> Cash
                                </div>
                                <div class="method-item">
                                    <img class="method-icon" src="https://www.logo.wine/a/logo/BKash/BKash-Icon-Logo.wine.svg" alt="bKash"> Bkash
                                </div>
                                <div class="method-item">
                                    <img class="method-icon" src="https://www.logo.wine/a/logo/Nagad/Nagad-Vertical-Logo.wine.svg" alt="Nagad"> Nagad
                                </div>
                                <div class="method-item">
                                    <img class="method-icon" src="https://img.icons8.com/color/48/museum.png" alt="Bank"> Bank
                                </div>
                            </div>
                        </div>
                        
                        <div class="signature-block">
                            <div class="sig-line"></div>
                            <strong>Authorised Signature</strong><br>
                            <span style="font-size: 10px;">SM-TECH<br>Computer & IT Solutions</span>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            b64_html = base64.b64encode(invoice_html.encode('utf-8')).decode('utf-8')
            
            col_action1, col_action2 = st.columns(2)
            with col_action1:
                st.markdown(
                    f"""
                    <a href="data:text/html;base64,{b64_html}" target="_blank" style="text-decoration:none;">
                        <button style="
                            background-color: #1b5e20;
                            color: white;
                            padding: 12px 18px;
                            font-size: 16px;
                            font-weight: bold;
                            border: none;
                            border-radius: 8px;
                            width: 100%;
                            cursor: pointer;
                            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
                        ">
                            🖨️ Open & Print Invoice
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            with col_action2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.invoice_items = []
                    st.rerun()
