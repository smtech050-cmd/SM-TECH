import streamlit as st

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH POS v2.0", layout="wide")

# সাইডবার থেকে রেডিও বাটন নিখুঁতভাবে লুকানোর জন্য সংশোধিত CSS
st.markdown("""
    <style>
        /* মূল ব্যাকগ্রাউন্ড ডার্ক নেভি ব্লু করা */
        .stApp {
            background-color: #0A192F;
            color: white;
        }
        /* সাইডবারের হালকা ব্যাকগ্রাউন্ড */
        [data-testid="stSidebar"] {
            background-color: #F0F2F5;
        }
        
        /* 🔥 রেডিও বাটন ডিজাইন ফিক্স (টেক্সট গায়েব হবে না এবার) */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 10px;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            background-color: #FFFFFF !important;
            border-radius: 6px !important;
            padding: 12px 20px !important;
            min-width: 100% !important;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.05) !important;
            cursor: pointer !important;
        }
        
        /* গোল বৃত্তটি গায়েব করা */
        [data-testid="stSidebar"] div[role="radiogroup"] label div:first-child:not([data-testid="stMarkdownContainer"]) {
            display: none !important;
        }
        
        /* লেখার রঙ ঠিক করা যাতে সাদা ব্যাকগ্রাউন্ডে পরিষ্কার কালো দেখায় */
        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #1E293B !important;
            font-size: 16px !important;
            font-weight: 500 !important;
        }
        
        /* মাউস হোভার ইফেক্ট */
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: #E2E8F0 !important;
        }
        
        /* ড্যাশবোর্ড কার্ডের কাস্টম ডিজাইন */
        .dashboard-card {
            background-color: #112240;
            border-left: 5px solid #00BCD4;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
            min-height: 160px;
        }
        .card-title {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 5px;
        }
        .card-value {
            font-size: 32px;
            font-weight: bold;
            color: #FFFFFF;
            margin-top: 15px;
        }
        /* লগইন ফর্মের স্টাইল */
        .login-box {
            background-color: #112240;
            padding: 40px;
            border-radius: 10px;
            max-width: 400px;
            margin: 50px auto;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# --- ২. লগইন স্টেট চেক করা ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- ③. লগইন স্ক্রিন ---
if not st.session_state['logged_in']:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("🔑 SM-TECH POS লগইন")
    
    username = st.text_input("ইউজারনেম")
    password = st.text_input("পাসওয়ার্ড", type="password")
    
    if st.button("লগইন করুন", use_container_width=True):
        if username == "admin" and password == "admin123":
            st.session_state['logged_in'] = True
            st.success("লগইন সফল হয়েছে!")
            st.rerun()
        else:
            st.error("ভুল ইউজারনেম অথবা পাসওয়ার্ড!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ৪. মূল অ্যাপ্লিকেশন ---
else:
    # --- সাইডবার মেনু ---
    with st.sidebar:
        st.markdown("<h3 style='color: #1E293B;'>💻 SM-TECH POS v2.0</h3>", unsafe_allow_html=True)
        st.write("---")
        
        menu_options = [
            "🏠 ড্যাশবোর্ড", 
            "📦 স্টক ম্যানেজমেন্ট", 
            "🔍 পণ্য সার্চ", 
            "🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট", 
            "👤 কাস্টমার ম্যানেজমেন্ট", 
            "📊 বিক্রয় রিপোর্ট", 
            "💰 লাভ-লোকসানের হিসাব"
        ]
        
        selected_menu = st.radio("", menu_options, label_visibility="collapsed")
        
        st.write("---")
        if st.button("🔓 লগআউট", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- ডান পাশের মূল কন্টেন্ট ---
    if "ড্যাশবোর্ড" in selected_menu:
        st.title("ড্যাশবোর্ড ওভারভিউ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="dashboard-card">
                    <div style="font-size: 30px;">💰</div>
                    <div class="card-title">মোট<br>বিক্রয়</div>
                    <div class="card-value">৳ 0.00</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="dashboard-card" style="border-left-color: #FF9800;">
                    <div style="font-size: 30px;">🛒</div>
                    <div class="card-title">মোট<br>ক্রয়</div>
                    <div class="card-value">৳ 0.00</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="dashboard-card" style="border-left-color: #4CAF50;">
                    <div style="font-size: 30px;">📈</div>
                    <div class="card-title">মোট<br>লাভ</div>
                    <div class="card-value">৳ 0.00</div>
                </div>
            """, unsafe_allow_html=True)

    elif "স্টক ম্যানেজমেন্ট" in selected_menu:
        st.title("📦 স্টক ম্যানেজমেন্ট")
        st.write("এখানে আপনার স্টকের পণ্যগুলো দেখা যাবে।")

    elif "পণ্য সার্চ" in selected_menu:
        st.title("🔍 পণ্য সার্চ")
        search_query = st.text_input("পণ্যের নাম লিখুন...")

    elif "ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট" in selected_menu:
        st.title("🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট")
        st.write("ইনভয়েস প্রিন্ট করার অপশন।")

    elif "কাস্টমার ম্যানেজমেন্ট" in selected_menu:
        st.title("👤 কাস্টমার ম্যানেজমেন্ট")
        st.write("কাস্টমার প্রোফাইল ও খতিয়ান।")

    elif "বিক্রয় রিপোর্ট" in selected_menu:
        st.title("📊 বিক্রয় রিপোর্ট")
        st.write("বিক্রয়ের সব রিপোর্ট এখানে পাবেন।")

    elif "লাভ-লোকসানের হিসাব" in selected_menu:
        st.title("💰 লাভ-লোকসানের হিসাব")
        st.write("লাভ ও ক্ষতির হিসাব।")
