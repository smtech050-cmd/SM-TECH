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
# 🛑 ১. ১০০% ফুল স্ক্রিন লগইন UI (Pure HTML/CSS)
# ==========================================
if not st.session_state.logged_in:
    # Streamlit Header/Footer Hide
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer {visibility: hidden !important; height: 0px !important;}
            .main .block-container {padding: 0rem !important; max-width: 100% !important;}
            [data-testid="stAppViewContainer"] {background-color: #080d1a !important; padding: 0 !important;}
        </style>
    """, unsafe_allow_html=True)

    # HTML Login Form
    login_html = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body {
          background-color: #080d1a;
          background-image: radial-gradient(circle at 50% 20%, rgba(0, 102, 255, 0.2) 0%, transparent 60%), linear-gradient(to bottom, #080d1a 0%, #050811 100%);
          display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #ffffff; padding: 20px;
        }
        .login-card {
          width: 100%; max-width: 420px; padding: 35px 25px; background: rgba(13, 22, 41, 0.95);
          border-radius: 28px; box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 20px rgba(0, 102, 255, 0.2);
          border: 1px solid #1e2e4a; text-align: center; position: relative;
        }
        .logo-img-wrapper {
          width: 110px; height: 110px; border-radius: 50%; background: #ffffff; padding: 3px;
          box-shadow: 0 0 20px rgba(0, 102, 255, 0.5); border: 2px solid #0066ff; margin: 0 auto 15px auto;
          display: flex; align-items: center; justify-content: center; overflow: hidden;
        }
        .logo-img-wrapper img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
        .brand-title { font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 4px; }
        .brand-title span { color: #1e88e5; }
        .brand-subtitle { font-size: 11px; color: #94a3b8; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 25px; text-transform: uppercase; }
        
        .input-group { position: relative; margin-bottom: 15px; }
        .input-group i.left-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #38bdf8; font-size: 15px; }
        .input-group i.right-icon { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); color: #64748b; font-size: 15px; cursor: pointer; }
        .input-group input {
          width: 100%; padding: 14px 40px 14px 45px; background-color: #0b1528; border: 1.5px solid #1e3a5f;
          border-radius: 12px; color: #38bdf8; font-size: 14px; outline: none; transition: 0.3s;
        }
        .input-group input:focus { border-color: #0066ff; box-shadow: 0 0 12px rgba(0, 102, 255, 0.3); }
        .options-row { display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 22px; }
        .options-row a { color: #38bdf8; text-decoration: none; }
        
        .btn-submit {
          width: 100%; padding: 14px; background: linear-gradient(90deg, #0052cc 0%, #0066ff 100%);
          color: #ffffff; border: none; border-radius: 25px; font-size: 16px; font-weight: 700; cursor: pointer;
          box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4); display: flex; align-items: center; justify-content: center; gap: 8px;
        }
        .divider { position: relative; text-align: center; font-size: 12px; color: #64748b; margin: 22px 0; }
        .divider::before, .divider::after { content: ""; position: absolute; top: 50%; width: 22%; height: 1px; background-color: #1e293b; }
        .divider::before { left: 0; } .divider::after { right: 0; }
        
        .social-login { display: flex; gap: 8px; justify-content: center; margin-bottom: 22px; }
        .social-btn {
          flex: 1; padding: 10px 6px; background-color: #0b1528; border: 1px solid #1e3a5f; border-radius: 10px;
          color: #e2e8f0; font-size: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;
        }
        .signup-text { font-size: 13px; color: #94a3b8; }
        .signup-text a { color: #38bdf8; text-decoration: none; font-weight: 700; }
      </style>
    </head>
    <body>
      <div class="login-card">
        <div class="logo-img-wrapper">
          <img src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH Logo">
        </div>
        <h2 class="brand-title">Welcome to <span>SM-TECH</span></h2>
        <p class="brand-subtitle">COMPUTER & IT SOLUTIONS</p>

        <form id="loginForm">
          <div class="input-group">
            <i class="fa-solid fa-user left-icon"></i>
            <input type="text" id="username" placeholder="আপনার মোবাইল নম্বর / ইমেইল" required>
          </div>
          <div class="input-group">
            <i class="fa-solid fa-lock left-icon"></i>
            <input type="password" id="password" placeholder="পাসওয়ার্ড" required>
            <i class="fa-solid fa-eye-slash right-icon"></i>
          </div>
          <div class="options-row">
            <label><input type="checkbox"> আমাকে মনে রাখুন</label>
            <a href="#">পাসওয়ার্ড ভুলে গেছেন?</a>
          </div>
          <button type="button" onclick="submitLogin()" class="btn-submit">
            [➔] লগইন করুন
          </button>
        </form>

        <div class="divider">অথবা ওটিপি দিয়ে লগইন</div>
        <div class="social-login">
          <button class="social-btn"><i class="fa-brands fa-google" style="color:#ea4335;"></i> Google</button>
          <button class="social-btn"><i class="fa-brands fa-facebook" style="color:#1877f2;"></i> Facebook</button>
          <button class="social-btn"><i class="fa-solid fa-envelope-open-text" style="color:#38bdf8;"></i> ওটিপি</button>
        </div>
        <p class="signup-text">একাউন্ট নেই? <a href="#">নিবন্ধন করুন (Sign Up)</a></p>
      </div>

      <script>
        function submitLogin() {
          // Streamlit-এ ইউজারনেম পাসওয়ার্ড চেক করার ট্রিক
          const u = document.getElementById("username").value;
          const p = document.getElementById("password").value;
          if(u === "admin" && p === "1234"){
             window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
          } else {
             alert("ভুল ইউজারনেম অথবা পাসওয়ার্ড! (ইউজারনেম: admin, পাসওয়ার্ড: 1234)");
          }
        }
      </script>
    </body>
    </html>
    """
    
    # HTML রেন্ডারিং
    st.components.v1.html(login_html, height=750, scrolling=False)

    # ব্যাকএন্ড লগইন বাইপাস বোতাম (বিকল্প লগইন)
    with st.expander("🔑 ডাইরেক্ট সিস্টেম প্রবেশ (Developer Option)"):
        dev_u = st.text_input("ইউজারনেম", value="admin", key="dev_u")
        dev_p = st.text_input("পাসওয়ার্ড", type="password", value="1234", key="dev_p")
        if st.button("লগইন ড্যাশবোর্ড"):
            if dev_u == "admin" and dev_p == "1234":
                st.session_state.logged_in = True
                st.rerun()

# ==========================================
# 🔓 ২. মূল ড্যাশবোর্ড
# ==========================================
else:
    # ড্যাশবোর্ড থিম CSS
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { background-color: #080d1a !important; color: white !important; }
            [data-testid="stSidebar"] { background-color: #0b1426 !important; }
            .stTextInput input, .stNumberInput input { background-color: #0b1528 !important; color: #38bdf8 !important; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 15px;">
                <span style="font-size: 28px; margin-right: 10px; color: #38bdf8;">💻</span>
                <span style="font-size: 22px; font-weight: 900; color: #ffffff;">SM-TECH</span>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔒 Logout / লগআউট", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("<h4 style='color:#38bdf8; margin-bottom:15px;'>মেনু নির্বাচন করুন</h4>", unsafe_allow_html=True)
        
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

    # ড্যাশবোর্ড মডিউল
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
                    "ক্রমিক নং": len(st.session_state.customer_dues) + 1, "কাস্টমার নাম": c_name, "কাজের বিবরণ": c_desc,
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
                    "ক্রমিক নং": len(st.session_state.shop_stock) + 1, "পণ্যের বিবরণ": s_desc, "পরিমান": s_qty, "দর": s_price, "মোট টাকা": s_qty*s_price
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
                    "ক্রমিক নং": len(st.session_state.saved_passwords) + 1, "শিক্ষা প্রতিষ্ঠানের নাম": inst_name, "এন্ট্রি পাসওয়ার্ড": entry_pass, "কনফার্ম পাসওয়ার্ড": confirm_pass
                })
                st.rerun()
        st.dataframe(pd.DataFrame(st.session_state.saved_passwords), use_container_width=True)

    # সেল ইনভয়েস
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 পয়েন্ট অব সেল ও ইনভয়েস")
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
            if st.button("🗑️ Clear All"):
                st.session_state.invoice_items = []
                st.rerun()
