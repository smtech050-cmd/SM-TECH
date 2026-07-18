import streamlit as st

# ১. পেজ কনফিগারেশন এবং ডার্ক থিম স্টাইল
st.set_page_config(page_title="SM-TECH POS v2.0", layout="wide")

# স্ক্রিনশটের মতো ডার্ক ব্লু ড্যাশবোর্ড এবং সাদা সাইডবারের জন্য কাস্টম CSS
st.markdown("""
    <style>
        /* মূল ব্যাকগ্রাউন্ড ডার্ক নেভি ব্লু করা */
        .stApp {
            background-color: #0A192F;
            color: white;
        }
        /* সাইডবারের স্টাইল (হালকা ব্যাকগ্রাউন্ড) */
        [data-testid="stSidebar"] {
            background-color: #F0F2F5;
        }
        [data-testid="stSidebar"] * {
            color: #1E293B !important;
        }
        /* ড্যাশবোর্ড কার্ডের কাস্টম ডিজাইন */
        .dashboard-card {
            background-color: #112240;
            border-left: 5px solid #00BCD4; /* সায়ান বর্ডার */
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
    </style>
""", unsafe_allow_html=True)

# --- ২. বাম পাশের সাইডবার (Sidebar Menu) ---
with st.sidebar:
    st.subheader("💻 SM-TECH POS v2.0")
    st.write("---")
    
    # মেনু বাটনসমূহ (রেডিও বাটন দিলে সিলেক্টেড মেনু বোঝা সহজ হয়)
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
    
    # নিচের দিকে লগআউট বাটন
    st.write("---")
    if st.button("🔓 লগআউট", use_container_width=True):
        st.info("লগআউট করা হচ্ছে...")

# --- ৩. ডান পাশের ড্যাশবোর্ড এরিয়া (Main Content) ---
if "ড্যাশবোর্ড" in selected_menu:
    st.title("ড্যাশবোর্ড ওভারভিউ")
    
    # ৩টি কলামে কার্ডগুলো সাজানো (স্ক্রিনশটের ডানের অংশের মতো)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # মোট বিক্রয় কার্ড (আপনার স্ক্রিনশটের হুবহু লুক)
        st.markdown("""
            <div class="dashboard-card">
                <div style="font-size: 30px;">💰</div>
                <div class="card-title">মোট<br>বিক্রয়</div>
                <div class="card-value">৳ 0.00</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # মোট ক্রয় কার্ড
        st.markdown("""
            <div class="dashboard-card" style="border-left-color: #FF9800;">
                <div style="font-size: 30px;">🛒</div>
                <div class="card-title">মোট<br>ক্রয়</div>
                <div class="card-value">৳ 0.00</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # মোট লাভ কার্ড
        st.markdown("""
            <div class="dashboard-card" style="border-left-color: #4CAF50;">
                <div style="font-size: 30px;">📈</div>
                <div class="card-title">মোট<br>লাভ</div>
                <div class="card-value">৳ 0.00</div>
            </div>
        """, unsafe_allow_html=True)

else:
    # অন্যান্য মেনুর জন্য ফাঁকা পেজ
    st.title(selected_menu)
    st.write(f"এখানে {selected_menu} এর কন্টেন্ট থাকবে।")
