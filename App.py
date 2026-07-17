import streamlit as st
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH Management", page_icon="💻", layout="wide")

# সেশন স্টেট ইনিশিয়ালাইজেশন (স্টকের ডেটা ধরে রাখার জন্য)
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = [
        {"পণ্য": "SSD 120GB", "পরিমাণ": 10, "ক্রয় মূল্য": 1200},
        {"পণ্য": "RAM 4GB DDR4", "পরিমাণ": 15, "ক্রয় মূল্য": 1500},
        {"পণ্য": "Keyboard USB", "পরিমাণ": 8, "ক্রয় মূল্য": 350},
    ]

# সাইডবার মেনু
st.sidebar.title("💻 SM-TECH")
choice = st.sidebar.radio("মেনু সিলেক্ট করুন:", ["📄 Invoice Generator", "📦 Stock Management"])

# ==========================================
# ১. ইনভয়েস জেনারেটর (INVOICE GENERATOR)
# ==========================================
if choice == "📄 Invoice Generator":
    st.title("📄 ক্যাশ মেমো / ইনভয়েস জেনারেটর")
    
    # ইনপুট ফিল্ড
    customer_name = st.text_input("কাস্টমার আইডি/নাম")
    service_charge = st.number_input("সার্ভিস চার্জ / বিল", min_value=0, value=0)
    parts_cost = st.number_input("ব্যবহৃত পার্টসের মূল্য", min_value=0, value=0)
    discount = st.number_input("ডিসকাউন্ট (টাকা)", min_value=0, value=0)
    
    if st.button("ইনভয়েস প্রিন্ট/সেভ করুন"):
        if customer_name:
            total_bill = service_charge + parts_cost - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # আপনার আসল প্যাডের ডিজাইন অনুযায়ী টেক্সট ফরম্যাট
            invoice_text = (
                f"=========================================\n"
                f"               SM-TECH                   \n"
                f"       COMPUTER & IT SOLUTION            \n"
                f"   Smart Technology-Trusted Service      \n"
                f"=========================================\n"
                f" Owner: S.m. Ibrahim                     \n"
                f" Phone: 01940-556114, 01810-499166       \n"
                f"-----------------------------------------\n"
                f" Bill To: {customer_name}\n"
                f" Date: {current_date}\n"
                f"-----------------------------------------\n"
                f" S.L | DESCRIPTION          | QTY | AMOUNT\n"
                f"-----------------------------------------\n"
                f"  1. | Service Charge/Bill  |  1  | {service_charge} Tk\n"
                f"  2. | Used Parts Cost      |  -  | {parts_cost} Tk\n"
                f"-----------------------------------------\n"
                f" DISCOUNT:                        | {discount} Tk\n"
                f"-----------------------------------------\n"
                f" SUB TOTAL:                       | {total_bill} Tk\n"
                f"=========================================\n"
                f" Payment Methods:                        \n"
                f" [ ] Cash   [ ] Bkash   [ ] Nagad   [ ] Bank\n"
                f"-----------------------------------------\n"
                f" Authorised Signature:                   \n"
                f" SM-TECH Computer & IT Solutions         \n"
                f"=========================================\n"
            )
            
            st.success("ইনভয়েস তৈরি সম্পন্ন হয়েছে!")
            
            # ডাউনলোড বাটন
            st.download_button(
                label="📥 Download PDF/Invoice",
                data=invoice_text,
                file_name=f"Invoice_{customer_name}.txt",
                mime="text/plain"
            )
        else:
            st.error("অনুগ্রহ করে কাস্টমারের নাম লিখুন।")

# ==========================================
# ২. স্টক ম্যানেজমেন্ট (STOCK MANAGEMENT)
# ==========================================
elif choice == "📦 Stock Management":
    st.title("📦 স্টক মালের হিসাব")
    
    # নতুন স্টক যোগ করার ফর্ম
    st.subheader("➕ নতুন পণ্য স্টক করুন")
    col1, col2, col3 = st.columns(3)
    with col1:
        item_name = st.text_input("পণ্যের নাম (Item Name)")
    with col2:
        quantity = st.number_input("পরিমাণ (Quantity)", min_value=0, value=0)
    with col3:
        cost_price = st.number_input("ক্রয় মূল্য (Cost Price)", min_value=0, value=0)
        
    if st.button("স্টক আপডেট করুন"):
        if item_name and quantity > 0:
            # নতুন পণ্য যোগ করা
            st.session_state["stock_data"].append({
                "পণ্য": item_name,
                "পরিমাণ": quantity,
                "ক্রয় মূল্য": cost_price
            })
            st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
        else:
            st.error("দয়া করে পণ্যের নাম এবং সঠিক পরিমাণ লিখুন।")
            
    st.markdown("---")
    
    # বর্তমান স্টকের তালিকা দেখানো
    st.subheader("📋 বর্তমান স্টক তালিকা")
    if st.session_state["stock_data"]:
        # টেবিল আকারে সুন্দরভাবে স্টক ডাটা দেখানো
        st.table(st.session_state["stock_data"])
    else:
        st.info("স্টকে কোনো পণ্য নেই।")
