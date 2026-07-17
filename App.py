import streamlit as st
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(page_title="Sristi Computer Repair Management", page_icon="💻", layout="wide")

# Session State Initialization for Login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 1. LOGIN MODULE ---
def login():
    st.subheader("🔑 সিসটেম লগইন")
    username = st.text_input("ইউজারনেম (Username)")
    password = st.text_input("পাসওয়ার্ড (Password)", type="password")
    
    if st.button("লগইন করুন"):
        if username == "admin" and password == "admin123": # আপনার সুবিধামত পরিবর্তন করে নেবেন
            st.session_state['logged_in'] = True
            st.success("লগইন সফল হয়েছে!")
            st.rerun()
        else:
            st.error("ভুল ইউজারনেম বা পাসওয়ার্ড। আবার চেষ্টা করুন।")

# --- MAIN APPLICATION ---
if not st.session_state['logged_in']:
    login()
else:
    # Sidebar Navigation with your 9 checked modules
    st.sidebar.title("💻 Sristi Repair Sys")
    menu = ["📊 Dashboard", "👥 Customer", "🔧 Repair", "📦 Stock", "🧾 Invoice", "📈 Reports", "⚙️ Settings", "💾 Backup"]
    choice = st.sidebar.radio("মেনু সিলেক্ট করুন:", menu)
    
    # Logout Button in Sidebar
    if st.sidebar.button("🚪 লগআউট"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- 2. DASHBOARD ---
    if choice == "📊 Dashboard":
        st.title("📊 ড্যাশবোর্ড ওভারভিউ")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("আজকের মোট মেরামত", "১২ টি", "+২")
        col2.metric("চলতি মেরামত (Pending)", "৫ টি", "-১")
        col3.metric("আজকের আয়", "৪,৫০০ টাকা", "+১৫%")
        col4.metric("স্টকে কম থাকা মালামাল", "৩ টি", "⚠️")
        
        st.markdown("---")
        st.subheader("🔔 সাম্প্রতিক অ্যাক্টিভিটি")
        st.info("🔧 কাস্টমার 'কামাল হোসেন' এর ল্যাপটপ ডেলিভারির জন্য প্রস্তুত।")
        st.warning("📦 স্টকে '500GB SSD' এর পরিমাণ কমে এসেছে!")

    # --- 3. CUSTOMER ---
    elif choice == "👥 Customer":
        st.title("👥 কাস্টমার ম্যানেজমেন্ট")
        tab1, tab2 = st.tabs(["নতুন কাস্টমার যোগ করুন", "কাস্টমার তালিকা"])
        
        with tab1:
            name = st.text_input("কাস্টমারের নাম")
            phone = st.text_input("মোবাইল নম্বর")
            address = st.text_area("ঠিকানা")
            if st.button("কাস্টমার সংরক্ষণ করুন"):
                st.success(f"কাস্টমার '{name}' সফলভাবে যুক্ত হয়েছে!")
                
        with tab2:
            # ডেমো ডাটা
            data = {"নাম": ["আব্দুর রহমান", "সোহেল রানা"], "মোবাইল": ["01711223344", "01999887766"], "ঠিকানা": ["ঢাকা", "ময়মনসিংহ"]}
            st.dataframe(pd.DataFrame(data), use_container_width=True)

    # --- 4. REPAIR ---
    elif choice == "🔧 Repair":
        st.title("🔧 মেরামত (Repair Job) ট্র্যাকিং")
        st.date_input("তারিখ", datetime.date.today())
        st.text_input("ডিভাইসের নাম/মডেল (যেমন: HP ProBook 450 G8)")
        st.text_area("সমস্যার বিবরণ (Problem Description)")
        st.text_input("আনুমানিক খরচ (Estimated Cost)")
        st.selectbox("কাজের বর্তমান অবস্থা (Status)", ["Pending", "In Progress", "Completed", "Delivered"])
        if st.button("জব কার্ড তৈরি করুন"):
            st.success("নতুন মেরামত টাস্ক রেজিস্টার্ড হয়েছে।")

    # --- 5. STOCK ---
    elif choice == "📦 Stock":
        st.title("📦 ইনভেন্টরি ও স্টক")
        st.subheader("পণ্য সার্চ বা নতুন এন্ট্রি")
        st.text_input("পণ্যের নাম (Item Name)")
        st.number_input("পরিমাণ (Quantity)", min_value=0)
        st.number_input("ক্রয় মূল্য (Cost Price)", min_value=0)
        if st.button("স্টক আপডেট করুন"):
            st.success("স্টক সফলভাবে আপডেট হয়েছে।")

    # --- 6. INVOICE ---
    elif choice == "🧾 Invoice":
        st.title("🧾 ক্যাশ মেমো / ইনভয়েস জেনারেটর")
        st.text_input("কাস্টমার আইডি/নাম")
        st.text_input("সার্ভিস চার্জ / বিল")
        st.text_input("ব্যবহৃত পার্টসের মূল্য")
        st.number_input("ডিসকাউন্ট (টাকা)", min_value=0)
        if st.button("ইনভয়েস প্রিন্ট/সেভ করুন"):
            st.success("ইনভয়েস PDF তৈরি সম্পন্ন হয়েছে! (ডেমো)")

    # --- 7. REPORTS ---
    elif choice == "📈 Reports":
        st.title("📈 রিপোর্ট ও অ্যানালিটিক্স")
        st.selectbox("রিপোর্টের ধরন", ["দৈনিক আয়-ব্যয়", "মাসিক প্রফিট", "সবচেয়ে বেশি মেরামত হওয়া পার্টস"])
        st.button("রিপোর্ট ডাউনলোড করুন (Excel)")

    # --- 8. SETTINGS ---
    elif choice == "⚙️ Settings":
        st.title("⚙️ সিসটেম সেটিংস")
        st.text_input("দোকানের নাম", "Sristi Computer Repair")
        st.text_input("ঠিকানা", "দোকানের ঠিকানা এখানে লিখুন")
        st.text_input("ট্যাক্স/ভ্যাট নম্বর (ঐচ্ছিক)")
        st.button("কনফিগারেশন সেভ করুন")

    # --- 9. BACKUP ---
    elif choice == "💾 Backup":
        st.title("💾 ডাটা ব্যাকআপ ও রিসেট")
        st.info("আপনার ডাটাবেজের নিরাপত্তা নিশ্চিত করতে নিয়মিত ব্যাকআপ নিন।")
        if st.button("📥 ক্লাউড ব্যাকআপ নিন"):
            st.success("সম্পূর্ণ ডাটাবেজ সফলভাবে ব্যাকআপ নেওয়া হয়েছে!")
