import streamlit as st
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH Management", page_icon="💻", layout="wide")

# সেশন স্টেট ইনিশিয়ালাইজেশন (স্টকের ডাটা ধরে রাখার জন্য)
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = [
        {"পণ্য": "SSD 120GB", "পরিমাণ": 10, "ক্রয় মূল্য": 1200},
        {"পণ্য": "RAM 4GB DDR4", "পরিমাণ": 15, "ক্রয় মূল্য": 1500},
    ]

# ইনভয়েসের ডাইনামিক আইটেম লিস্টের জন্য সেশন স্টেট
if "invoice_items" not in st.session_state:
    st.session_state["invoice_items"] = [{"description": "", "qty": 1, "uprice": 0}]

# সাইডবার মেনু
st.sidebar.title("💻 SM-TECH")
choice = st.sidebar.radio("মেনু সিলেক্ট করুন:", ["📄 Invoice Generator", "📦 Stock Management"])

# ==========================================
# ১. ইনভয়েস জেনারেটর (INVOICE GENERATOR)
# ==========================================
if choice == "📄 Invoice Generator":
    st.title("📄 ক্যাশ মেমো / ইনভয়েস জেনারেটর")
    
    # ইনপুট ফিল্ডসমূহ
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Name (কাস্টমারের নাম)")
        customer_address = st.text_input("Address (ঠিকানা)")
    with col_b:
        invoice_no = st.text_input("Invoice No (মেমো নম্বর)", value="SMTECH/2026/01")
    
    st.markdown("---")
    st.subheader("🛒 বিলের বিবরণ")
    
    # ডাইনামিক আইটেম ইনপুট রো তৈরি
    updated_items = []
    for i, item in enumerate(st.session_state["invoice_items"]):
        st.markdown(f"**আইটেম নম্বর: {i+1}**")
        col_desc, col_qty, col_uprice = st.columns([5, 2, 3])
        
        with col_desc:
            desc = st.text_input(f"DESCRIPTION (কাজের বিবরণ/পণ্যের নাম)", value=item["description"], key=f"desc_{i}")
        with col_qty:
            qty = st.number_input(f"QTY (পরিমাণ)", min_value=1, value=item["qty"], key=f"qty_{i}")
        with col_uprice:
            uprice = st.number_input(f"U.PRICE (একক মূল্য)", min_value=0, value=item["uprice"], key=f"uprice_{i}")
            
        updated_items.append({"description": desc, "qty": qty, "uprice": uprice})
    
    st.session_state["invoice_items"] = updated_items
    
    # বাটনসমূহ
    col_btn1, col_btn2, _ = st.columns([2, 2, 6])
    with col_btn1:
        if st.button("➕ নতুন আইটেম যোগ করুন"):
            st.session_state["invoice_items"].append({"description": "", "qty": 1, "uprice": 0})
            st.rerun()
    with col_btn2:
        if st.button("❌ শেষ আইটেমটি বাদ দিন") and len(st.session_state["invoice_items"]) > 1:
            st.session_state["invoice_items"].pop()
            st.rerun()
            
    st.markdown("---")
    discount = st.number_input("DISCOUNT (ডিসকাউন্ট টাকা)", min_value=0, value=0)
    
    # লোগো ইমেজের ইউআরএল (এখানে আপনার আপলোড করা লোগোর লিংক বসাতে পারবেন)
    logo_url = "https://i.ibb.co/v4v8WbZ/sm-tech-logo.png" 
    
    if st.button("ইনভয়েস পিডিএফ তৈরি করুন"):
        if customer_name:
            sub_total = 0
            table_rows_html = ""
            
            for index, item in enumerate(st.session_state["invoice_items"]):
                if item["description"].strip() != "":
                    amount = item["qty"] * item["uprice"]
                    sub_total += amount
                    
                    table_rows_html += f"""
                    <tr>
                        <td style="text-align: center;">{index + 1}</td>
                        <td>{item["description"]}</td>
                        <td style="text-align: center;">{item["qty"]}</td>
                        <td style="text-align: right;">{item["uprice"]}</td>
                        <td style="text-align: right; font-weight: bold;">{amount}</td>
                    </tr>
                    """
            
            total_bill = sub_total - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # হুবহু H7" W5" সাইজের পেপার এবং নতুন লোগো লেআউট সহ HTML
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    /* মেমোর সাইজ ঠিক করার মূল CSS (H 7in, W 5in) */
                    @page {{
                        size: 5in 7in;
                        margin: 0;
                    }}
                    body {{ 
                        font-family: 'Arial', sans-serif; 
                        background-color: #fff; 
                        padding: 0; 
                        margin: 0; 
                        width: 5in; 
                        height: 7in;
                        box-sizing: border-box;
                    }}
                    .main-pad {{ 
                        width: 100%; 
                        height: 100%; 
                        padding: 15px 12px; 
                        border: 1px solid #0a4da2; 
                        box-sizing: border-box;
                        background-color: #fff;
                        position: relative;
                    }}
                    
                    /* হেডার লেআউট - ডানে লোগো */
                    .header-table {{ width: 100%; border-collapse: collapse; }}
                    .logo-main {{ font-size: 32px; font-weight: 900; font-style: italic; color: #e63946; margin: 0; line-height: 0.9; font-family: 'Impact', sans-serif; }}
                    .logo-main span {{ color: #0a4da2; }}
                    .sub-title {{ font-size: 10px; font-weight: bold; color: #2a9d8f; letter-spacing: 0.5px; margin: 2px 0; }}
                    .tagline {{ font-size: 8px; font-weight: bold; color: #333; margin: 0; }}
                    
                    .logo-img-container {{ text-align: right; vertical-align: top; width: 65px; }}
                    .logo-img {{ width: 60px; height: 60px; object-fit: contain; background: #fff; border-radius: 50%; }}
                    
                    .owner-info-block {{ font-size: 8px; color: #0a4da2; font-weight: bold; line-height: 1.3; text-align: left; margin-top: 3px; }}
                    .owner-name {{ font-size: 10px; color: #0a4da2; }}
                    
                    /* ইনভয়েস বার ও কাস্টমার ইনফো */
                    .invoice-bar-table {{ width: 100%; margin-top: 10px; border-collapse: collapse; }}
                    .bill-to {{ font-size: 9px; font-weight: bold; color: white; background-color: #0a4da2; padding: 1px 4px; border-radius: 1px; }}
                    .invoice-badge {{ background-color: #0a4da2; color: white; font-size: 12px; font-weight: bold; text-align: center; padding: 2px 12px; letter-spacing: 1px; border-radius: 2px; display: inline-block; }}
                    
                    .info-lines {{ font-size: 9px; line-height: 1.8; }}
                    .dot-line {{ border-bottom: 1px dotted #555; display: inline-block; padding-left: 3px; font-weight: bold; color: #000; }}
                    
                    /* টেবিল ডিজাইন */
                    .item-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; border: 1.5px solid #0a4da2; }}
                    .item-table th {{ background-color: #0a4da2; color: white; padding: 5px 3px; font-size: 9px; font-weight: bold; border: 1px solid #fff; text-align: center; }}
                    .item-table td {{ padding: 6px 4px; border-left: 1.5px solid #0a4da2; border-right: 1.5px solid #0a4da2; border-bottom: 1px solid #e0e0e0; font-size: 9px; }}
                    
                    /* সাবটোটাল বক্স */
                    .subtotal-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 4px; text-align: center; font-size: 9px; }}
                    .subtotal-val {{ text-align: right; font-weight: bold; border: 1.5px solid #0a4da2; background-color: #f8f9fa; font-size: 10px; color: #0a4da2; padding: 4px; }}
                    
                    /* পেমেন্ট ও সিগনেচার */
                    .bottom-area {{ width: 100%; border-collapse: collapse; position: absolute; bottom: 15px; left: 12px; right: 12px; width: calc(100% - 24px); }}
                    .pay-method-box {{ border: 1.5px solid #0a4da2; border-radius: 3px; padding: 6px; width: 180px; font-size: 8px; font-weight: bold; color: #0a4da2; }}
                    .pay-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 1px 4px; display: inline-block; margin-bottom: 4px; }}
                    
                    .signature-area {{ text-align: right; font-size: 8px; font-weight: bold; color: #333; vertical-align: bottom; }}
                    .sig-line {{ border-top: 1px solid #333; width: 110px; display: inline-block; margin-bottom: 3px; }}
                    
                    @media print {{
                        body {{ background-color: #fff; }}
                    }}
                </style>
            </head>
            <body>
                <div class="main-pad">
                    <!-- হেডার অংশ - ডানে লোগো সেট করা হয়েছে -->
                    <table class="header-table">
                        <tr>
                            <td style="vertical-align: top;">
                                <p class="logo-main">SM-<span>TECH</span></p>
                                <p class="sub-title">COMPUTER & IT SOLUTION</p>
                                <p class="tagline">Smart Technology-Trusted Service</p>
                                <div class="owner-info-block">
                                    <span class="owner-name">S.m. Ibrahim</span> (Owner)<br>
                                    📞 01940-556114, 01810-499166
                                </div>
                            </td>
                            <td class="logo-img-container">
                                <!-- সাদা ব্যাকগ্রাউন্ডে আপনার গোল লোগো ইমেজ -->
                                <img src="{logo_url}" class="logo-img" alt="Logo">
                            </td>
                        </tr>
                    </table>
                    
                    <!-- কাস্টমার ও মেমো ইনফো -->
                    <table class="invoice-bar-table">
                        <tr>
                            <td style="width: 55%; vertical-align: top;">
                                <div class="info-lines">
                                    <span class="bill-to">Bill To</span> Name: <span class="dot-line" style="width: 140px;">{customer_name}</span><br>
                                    Address: <span class="dot-line" style="width: 160px;">{customer_address}</span>
                                </div>
                            </td>
                            <td style="width: 45%; text-align: right; vertical-align: top;">
                                <div class="invoice-badge" style="margin-bottom: 4px;">INVOICE</div>
                                <div class="info-lines">
                                    Invoice No: <span class="dot-line" style="width: 80px; text-align: left;">{invoice_no}</span><br>
                                    Date: <span class="dot-line" style="width: 80px; text-align: left;">{current_date}</span>
                                </div>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- ডাইনামিক টেবিল -->
                    <table class="item-table">
                        <thead>
                            <tr>
                                <th style="width: 10%;">S.L</th>
                                <th style="width: 50%;">DESCRIPTION</th>
                                <th style="width: 10%;">QTY</th>
                                <th style="width: 15%;">U.PRICE</th>
                                <th style="width: 15%;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows_html}
                            
                            <!-- ডিসকাউন্ট ও সাবটোটাল -->
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td style="text-align: right; font-weight: bold; border-top: 1.5px solid #0a4da2; padding: 4px; font-size: 8px;">Discount:</td>
                                <td style="text-align: right; font-weight: bold; color: red; border-top: 1.5px solid #0a4da2; padding: 4px; font-size: 8px;">{discount} Tk</td>
                            </tr>
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td class="subtotal-title">SUB TOTAL</td>
                                <td class="subtotal-val">{total_bill} Tk</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <!-- পেমেন্ট এবং সিগনেচার (৭ ইঞ্চি হাইটের নিচে ফিক্সড থাকবে) -->
                    <table class="bottom-area">
                        <tr>
                            <td>
                                <div class="pay-method-box">
                                    <div class="pay-title">Payment Methods</div><br>
                                    <input type="checkbox"> Cash &nbsp;
                                    <input type="checkbox"> Bkash &nbsp;
                                    <input type="checkbox"> Nagad &nbsp;
                                    <input type="checkbox"> Bank
                                </div>
                            </td>
                            <td class="signature-area">
                                <div class="sig-line"></div><br>
                                Authorised Signature<br>
                                <span style="font-size: 7px; font-weight: normal; color: #666;">SM-TECH Computer & IT Solutions</span>
                            </td>
                        </tr>
                    </table>
                </div>
                <script>
                    window.onload = function() {{ window.print(); }}
                </script>
            </body>
            </html>
            """
            
            st.success("ইনভয়েস PDF সফলভাবে তৈরি হয়েছে!")
            st.download_button(
                label="📥 Download & Print PDF Invoice",
                data=invoice_html,
                file_name=f"Invoice_{customer_name}.html",
                mime="text/html"
            )
        else:
            st.error("অনুগ্রহ করে কাস্টমারের নাম লিখুন।")

# ==========================================
# ২. স্টক ম্যানেজমেন্ট (STOCK MANAGEMENT)
# ==========================================
elif choice == "📦 Stock Management":
    st.title("📦 স্টক মালের হিসাব")
    
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
            st.session_state["stock_data"].append({
                "পণ্য": item_name,
                "পরিমাণ": quantity,
                "ক্রয় মূল্য": cost_price
            })
            st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
        else:
            st.error("দয়া করে পণ্যের নাম এবং সঠিক পরিমাণ লিখুন।")
            
    st.markdown("---")
    st.subheader("📋 বর্তমান স্টক তালিকা")
    if st.session_state["stock_data"]:
        st.table(st.session_state["stock_data"])
    else:
        st.info("স্টকে কোনো পণ্য নেই।")
