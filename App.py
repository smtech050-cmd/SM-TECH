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
# 🔢 সংখ্যাকে কথায় রূপান্তর করার ফাংশন (ইংরেজিতে)
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

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

if "customer_dues" not in st.session_state:
    st.session_state.customer_dues = [
        {"क्रमिक নং": 1, "কাস্টমার নাম": "Abir Rahman", "কাজের বিবরণ": "Windows Setup", "পরিমান": 1, "দর": 500, "মোট টাকা": 500, "আদায়": 300, "বাকি": 200}
    ]

if "shop_stock" not in st.session_state:
    st.session_state.shop_stock = [
        {"क्रमिक নং": 1, "পণ্যের বিবরণ": "512GB NVMe SSD", "পরিমান": 10, "দর": 4200, "মোট টাকা": 42000}
    ]

if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = [
        {"क्रमिक নং": 1, "শিক্ষা প্রতিষ্ঠানের নাম": "Sreebardi Govt. College", "এন্ট্রি পাসওয়ার্ড": "sreebardi@2026", "কনফার্ম পাসওয়ার্ড": "board@xyz2026"}
    ]

if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

# ==========================================
# 🎨 গ্লোবাল থিম: CSS
# ==========================================
custom_css = """
<style>
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }
    .stTextInput div[data-baseweb="input"] {
        border: 1px solid #cccccc !important;
    }
    .stTextInput input, .stNumberInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #000000 !important;
    }
    input::placeholder {
        color: #777777 !important;
        -webkit-text-fill-color: #777777 !important;
    }
    div[data-baseweb="input"] svg {
        fill: #333333 !important;
        color: #333333 !important;
    }
    .stTextInput label, .stNumberInput label {
        color: #222222 !important;
        font-weight: bold !important;
    }
    div.stButton > button {
        background-color: #d60000 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #bd0000 !important;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.2) !important;
    }
    div.stButton p {
        color: #ffffff !important; 
    }
    div.stSidebar div.stButton > button {
        text-align: left !important;
        margin-bottom: 12px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🛑 ১. লগইন স্ক্রিন রেন্ডারিং
# ==========================================
if not st.session_state.logged_in:
    _, col_center, _ = st.columns([0.5, 2.4, 0.5])
    with col_center:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(
            """
            <style>
                div[data-testid="stImage"] img {
                    width: 85% !important;
                    max-width: 550px !important;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.image("https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png", use_container_width=True)
        
        with st.container(border=False):
            st.markdown('<div style="font-size: 22px; font-weight: bold; text-align: center; color: #d60000; margin-top: 15px; margin-bottom: 25px;">অ্যাডমিন প্যানেল প্রবেশ করুন</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username (ইউজারনেম)", placeholder="ইউজারনেম লিখুন...")
            password = st.text_input("Password (পাসওয়ার্ড)", type="password", placeholder="পাসওয়ার্ড লিখুন...")
            st.markdown('<br>', unsafe_allow_html=True)
            
            login_btn = st.button("🔒 লগইন করুন", use_container_width=True)
            if login_btn:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("লগইন সফল হয়েছে!")
                    st.rerun()
                else:
                    st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড স্ক্রিন
# ==========================================
else:
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 15px; margin-bottom: 15px; padding-left: 5px;">
                <span style="font-size: 32px; margin-right: 12px; color: #d60000;">⚙️</span>
                <span style="font-size: 30px; font-weight: 900; color: #d60000; letter-spacing: 0.5px;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h3 style='color:#d60000; font-size:20px; font-weight:bold; margin-left:5px; margin-bottom:15px;'>মেনু নির্বাচন করুন</h3>", unsafe_allow_html=True)
        
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
                    "क्रमिक নং": len(st.session_state.customer_dues) + 1, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
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
                    "क्रमिक নং": len(st.session_state.shop_stock) + 1, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": s_qty*s_price
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
                    "क्रमिक নং": len(st.session_state.saved_passwords) + 1, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True)

    # সেল ইনভয়েস (লোগোর সাথে বড় SM-TECH লেখা যুক্ত করা হয়েছে)
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 ইনভয়েস")
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
            st.dataframe(pd.DataFrame(st.session_state.invoice_items), use_container_width=True)
            
            # মোট হিসাব বের করা
            total_amt = sum(item["Amount"] for item in st.session_state.invoice_items)
            amount_in_words = number_to_words(total_amt) + " BDT Only."
            
            # ১২টি রো গ্রিড মেইনটেইন করা
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
            <html>
            <head>
                <style>
                    @page {{
                        size: A5 portrait;
                        margin: 0;
                    }}
                    body {{
                        font-family: 'Arial', sans-serif;
                        color: #1a237e;
                        font-size: 11px;
                        margin: 0;
                        padding: 0;
                        background-color: #fff;
                    }}
                    .pad-container {{
                        width: 140mm;
                        height: 202mm;
                        padding: 8mm;
                        box-sizing: border-box;
                        position: relative;
                        border: 2px solid #1a237e;
                        margin: auto;
                    }}
                    .header-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 2px;
                    }}
                    .logo-block {{
                        display: flex;
                        align-items: center;
                    }}
                    .logo-block img {{
                        max-height: 48px;
                        width: auto;
                        margin-right: 8px;
                    }}
                    .logo-text-box {{
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    }}
                    .brand-title {{
                        font-size: 26px;
                        font-weight: 900;
                        color: #1a237e;
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
                    .owner-info {{
                        text-align: right;
                        font-size: 11px;
                        color: #1a237e;
                        line-height: 1.3;
                    }}
                    .owner-name {{
                        font-size: 14px;
                        font-weight: bold;
                    }}
                    .tagline {{
                        text-align: center;
                        font-size: 11px;
                        font-weight: bold;
                        color: #000;
                        margin-top: 2px;
                        margin-bottom: 12px;
                    }}
                    .bill-section {{
                        width: 100%;
                        margin-bottom: 10px;
                    }}
                    .bill-to-badge {{
                        background-color: #1a237e;
                        color: white;
                        padding: 2px 6px;
                        font-weight: bold;
                        border-radius: 3px 3px 0 0;
                        display: inline-block;
                    }}
                    .invoice-badge {{
                        background-color: #1a237e;
                        color: white;
                        padding: 3px 12px;
                        font-weight: bold;
                        letter-spacing: 1px;
                        font-size: 13px;
                        float: right;
                    }}
                    .customer-details {{
                        width: 100%;
                        margin-top: 2px;
                    }}
                    .dot-line {{
                        border-bottom: 1px dotted #1a237e;
                        padding-bottom: 2px;
                        color: #000;
                    }}
                    .main-table {{
                        width: 100%;
                        border-collapse: collapse;
                        border: 1px solid #1a237e;
                    }}
                    .main-table th {{
                        background-color: #1a237e;
                        color: white;
                        font-weight: bold;
                        text-align: center;
                        padding: 5px;
                        font-size: 11px;
                        border: 1px solid #1a237e;
                    }}
                    .item-row td {{
                        border-left: 1px solid #1a237e;
                        border-right: 1px solid #1a237e;
                        border-bottom: 1px solid #e0e0e0;
                        padding: 5px;
                        height: 22px;
                        color: #000;
                    }}
                    .blank-row td {{
                        height: 22px;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    .subtotal-box {{
                        background-color: #1a237e;
                        color: white;
                        font-weight: bold;
                        padding: 5px;
                        text-align: center;
                    }}
                    .amount-words {{
                        margin-top: 10px;
                        color: #1a237e;
                        font-weight: bold;
                        font-size: 11px;
                    }}
                    .words-text {{
                        color: #000;
                        font-weight: normal;
                        border-bottom: 1px dotted #1a237e;
                    }}
                    .footer-section {{
                        position: absolute;
                        bottom: 8mm;
                        left: 8mm;
                        right: 8mm;
                        width: 88%;
                    }}
                    .payment-methods-box {{
                        border: 1px solid #1a237e;
                        display: inline-block;
                        width: 58%;
                        vertical-align: bottom;
                        border-radius: 4px;
                        overflow: hidden;
                    }}
                    .pm-title {{
                        background-color: #1a237e;
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
                        color: #000;
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
                        color: #1a237e;
                    }}
                    .sig-line {{
                        border-top: 1px solid #1a237e;
                        margin-bottom: 4px;
                    }}
                </style>
            </head>
            <body>
                <div class="pad-container">
                    <table class="header-table">
                        <tr>
                            <td style="width: 65%; vertical-align: middle;">
                                <div class="logo-block">
                                    <img src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH">
                                    <div class="logo-text-box">
                                        <div class="brand-title">SM-TECH</div>
                                        <div class="brand-subtitle">COMPUTER & IT SOLUTION</div>
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
                    
                    <div class="tagline">Smart Technology-Trusted Service</div>
                    
                    <div class="bill-section">
                        <span class="bill-to-badge">Bill To</span>
                        <span class="invoice-badge">INVOICE</span>
                        
                        <table class="customer-details">
                            <tr>
                                <td style="width: 65%;"><strong>Name:</strong> <span class="dot-line">{cust_name}</span></td>
                                <td><strong>Invoice No:</strong> <span class="dot-line">{inv_custom_num}</span></td>
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
                                <td style="text-align: right; padding-right: 8px; font-weight: bold; border: 1px solid #1a237e; background-color: #f5f5f5; color:#000;">{total_amt}/-</td>
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
                
                <script>
                    window.onload = function() {{
                        window.print();
                    }}
                </script>
            </body>
            </html>
            """
            
            # HTML ডেটা এনকোড করা
            b64_html = base64.b64encode(invoice_html.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{b64_html}"
            
            col_action1, col_action2 = st.columns(2)
            with col_action1:
                if st.button("🖨️ Print PDF (A5)", use_container_width=True):
                    components.html(
                        f"""
                        <iframe src="{iframe_src}" style="display:none;" id="printFrame"></iframe>
                        <script>
                            var frame = document.getElementById('printFrame');
                            frame.onload = function() {{
                                frame.contentWindow.focus();
                                frame.contentWindow.print();
                            }};
                        </script>
                        """,
                        height=0,
                    )
                    st.success("প্রিন্ট কমান্ড পাঠানো হয়েছে!")
            with col_action2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.invoice_items = []
                    st.rerun()
