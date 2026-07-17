import streamlit as st
import datetime
import base64

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH Management", page_icon="💻", layout="wide")

# সেশন স্টেট ইনিশিয়ালাইজেশন
if "stock_data" not in st.session_state:
    # ডামি ডাটা (অ্যাপ প্রথমবার ওপেন হলে দেখাবে)
    st.session_state["stock_data"] = [
        {"Date": "18-07-2026", "New Products": "SSD 120GB", "Quantity": 10, "Cost Price": 1200, "Sell Rate": 1500},
        {"Date": "18-07-2026", "New Products": "RAM 4GB DDR4", "Quantity": 15, "Cost Price": 1500, "Sell Rate": 1800},
    ]

if "invoice_items" not in st.session_state:
    st.session_state["invoice_items"] = [{"description": "", "qty": 1, "uprice": 0}]

# সাইডবার মেনু
st.sidebar.title("💻 SM-TECH")
choice = st.sidebar.radio("মেনু সিলেক্ট করুন:", ["📄 Invoice Generator", "📦 Stock Management"])

# ==========================================
# ১. ইনভয়েস জেনারেটর (INVOICE GENERATOR)
# ==========================================
if choice == "📄 Invoice Generator":
    st.title("📄 ক্যাশ মেমো / ইনভয়েস জেনারেটর (5\"x7\")")
    
    st.subheader("🖼️ মেমোর লোগো সেট করুন")
    logo_file = st.file_uploader("আপনার গোল লোগোটি এখানে আপলোড করুন (PNG/JPG)", type=["png", "jpg", "jpeg"])
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Name (কাস্টমারের নাম)")
        customer_address = st.text_input("Address (ঠিকানা)")
    with col_b:
        invoice_no = st.text_input("Invoice No (মেমো নম্বর)", value="SMTECH/2026/01")
    
    st.markdown("---")
    st.subheader("🛒 বিলের বিবরণ")
    
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
    
    if st.button("ইনভয়েস পিডিএফ তৈরি করুন"):
        if customer_name:
            sub_total = 0
            table_rows_html = ""
            active_rows_count = 0
            
            for index, item in enumerate(st.session_state["invoice_items"]):
                if item["description"].strip() != "":
                    amount = item["qty"] * item["uprice"]
                    sub_total += amount
                    active_rows_count += 1
                    
                    table_rows_html += f"""
                    <tr>
                        <td style="text-align: center; padding: 5px; font-size: 11px; height: 18px;">{active_rows_count}</td>
                        <td style="padding: 5px; font-size: 11px; font-weight: bold;">{item["description"]}</td>
                        <td style="text-align: center; padding: 5px; font-size: 11px;">{item["qty"]}</td>
                        <td style="text-align: right; padding: 5px; font-size: 11px;">{item["uprice"]}</td>
                        <td style="text-align: right; padding: 5px; font-size: 11px; font-weight: bold;">{amount}</td>
                    </tr>
                    """
            
            total_required_rows = 10
            blank_rows_to_add = max(0, total_required_rows - active_rows_count)
            
            for b in range(blank_rows_to_add):
                row_num = active_rows_count + b + 1
                table_rows_html += f"""
                <tr>
                    <td style="text-align: center; padding: 5px; font-size: 11px; color: #ccc; height: 18px;">{row_num}</td>
                    <td style="padding: 5px;"></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                """
            
            total_bill = sub_total - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            logo_html_tag = '<div class="logo-placeholder">SM</div>'
            if logo_file is not None:
                file_bytes = logo_file.read()
                base64_image = base64.b64encode(file_bytes).decode("utf-8")
                logo_html_tag = f'<img src="data:image/png;base64,{base64_image}" class="logo-img">'
            
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{ size: 5in 7in; margin: 0; }}
                    body {{ font-family: 'Arial', sans-serif; background-color: #fff; margin: 0; padding: 0; -webkit-print-color-adjust: exact; }}
                    .main-pad {{ width: 5in; height: 7in; padding: 0.2in 0.2in 0.15in 0.2in; box-sizing: border-box; border: 1px solid #0a4da2; display: flex; flex-direction: column; }}
                    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 3px; }}
                    .logo-td {{ width: 62px; vertical-align: middle; text-align: left; }}
                    .logo-img {{ width: 55px; height: 55px; border-radius: 50%; object-fit: cover; border: 1.5px solid #0a4da2; }}
                    .logo-placeholder {{ width: 55px; height: 55px; border-radius: 50%; background: #0a4da2; color: #fff; text-align: center; line-height: 55px; font-weight: bold; font-size: 18px; }}
                    .text-td {{ vertical-align: top; padding-left: 6px; }}
                    .logo-main {{ font-size: 26px; font-weight: 900; font-style: italic; color: #e63946; margin: 0; line-height: 0.9; font-family: 'Impact', Arial, sans-serif; }}
                    .logo-main span {{ color: #0a4da2; }}
                    .sub-title {{ font-size: 9.5px; font-weight: bold; color: #2a9d8f; letter-spacing: 0.5px; margin: 3px 0 1px 0; font-family: 'Arial Black', sans-serif; }}
                    .tagline {{ font-size: 8px; font-weight: bold; color: #555; margin: 0; }}
                    .owner-td {{ text-align: right; font-size: 8.5px; color: #0a4da2; font-weight: bold; line-height: 1.3; vertical-align: top; width: 105px; padding-top: 2px; }}
                    .owner-name {{ font-size: 11px; color: #0a4da2; font-weight: bold; }}
                    .invoice-bar-table {{ width: 100%; margin-top: 5px; border-collapse: collapse; }}
                    .bill-to {{ font-size: 9.5px; font-weight: bold; color: white; background-color: #0a4da2; padding: 1px 4px; border-radius: 1px; }}
                    .invoice-badge {{ background-color: #0a4da2; color: white; font-size: 12px; font-weight: bold; text-align: center; padding: 2px 14px; letter-spacing: 1px; border-radius: 2px; display: inline-block; }}
                    .info-lines {{ font-size: 10px; line-height: 1.8; }}
                    .dot-line {{ border-bottom: 1px dotted #555; display: inline-block; padding-left: 3px; font-weight: bold; color: #000; }}
                    .item-table {{ width: 100%; border-collapse: collapse; margin-top: 6px; border: 1.5px solid #0a4da2; }}
                    .item-table th {{ background-color: #0a4da2; color: white; padding: 4px; font-size: 10px; font-weight: bold; border: 1px solid #fff; text-align: center; }}
                    .item-table td {{ border-left: 1.5px solid #0a4da2; border-right: 1.5px solid #0a4da2; border-bottom: 1px solid #e0e0e0; }}
                    .subtotal-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 4px; text-align: center; font-size: 10px; }}
                    .subtotal-val {{ text-align: right; font-weight: bold; border: 1.5px solid #0a4da2; background-color: #f8f9fa; font-size: 11px; color: #0a4da2; padding: 4px; }}
                    .bottom-area {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
                    .pay-method-box {{ border: 1.5px solid #0a4da2; border-radius: 3px; padding: 4px; width: 175px; font-size: 9px; font-weight: bold; color: #0a4da2; line-height: 1.3; }}
                    .pay-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 1px 3px; display: inline-block; margin-bottom: 3px; }}
                    .signature-area {{ text-align: right; font-size: 9px; font-weight: bold; color: #333; vertical-align: bottom; }}
                    .sig-line {{ border-top: 1px solid #333; width: 105px; display: inline-block; margin-bottom: 3px; }}
                    @media print {{ .main-pad {{ border: none; padding: 0.2in 0.2in 0.15in 0.2in; width: 5in; height: 7in; }} }}
                </style>
            </head>
            <body>
                <div class="main-pad">
                    <table class="header-table">
                        <tr>
                            <td class="logo-td">{logo_html_tag}</td>
                            <td class="text-td">
                                <p class="logo-main">SM-<span>TECH</span></p>
                                <p class="sub-title">COMPUTER & IT SOLUTION</p>
                                <p class="tagline">Smart Technology-Trusted Service</p>
                            </td>
                            <td class="owner-td">
                                <span class="owner-name">S.m. Ibrahim</span><br>Owner<br>01940-556114<br>01810-499166
                            </td>
                        </tr>
                    </table>
                    <table class="invoice-bar-table">
                        <tr>
                            <td style="width: 55%; vertical-align: top;">
                                <div class="info-lines">
                                    <span class="bill-to">Bill To</span> Name: <span class="dot-line" style="width: 130px;">{customer_name}</span><br>
                                    Address: <span class="dot-line" style="width: 150px;">{customer_address}</span>
                                </div>
                            </td>
                            <td style="width: 45%; text-align: right; vertical-align: top;">
                                <div class="invoice-badge" style="margin-bottom: 3px;">INVOICE</div>
                                <div class="info-lines">
                                    Invoice No: <span class="dot-line" style="width: 85px; text-align: left;">{invoice_no}</span><br>
                                    Date: <span class="dot-line" style="width: 85px; text-align: left;">{current_date}</span>
                                </div>
                            </td>
                        </tr>
                    </table>
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
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td style="text-align: right; font-weight: bold; border-top: 1.5px solid #0a4da2; padding: 4px; font-size: 10px;">Discount:</td>
                                <td style="text-align: right; font-weight: bold; color: red; border-top: 1.5px solid #0a4da2; padding: 4px; font-size: 10px;">{discount}</td>
                            </tr>
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td class="subtotal-title">SUB TOTAL</td>
                                <td class="subtotal-val">{total_bill}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="bottom-area">
                        <tr>
                            <td>
                                <div class="pay-method-box">
                                    <div class="pay-title">Payment Methods</div><br>
                                    <input type="checkbox"> Cash &nbsp; <input type="checkbox"> Bkash &nbsp; <input type="checkbox"> Nagad &nbsp; <input type="checkbox"> Bank
                                </div>
                            </td>
                            <td class="signature-area">
                                <div class="sig-line"></div><br>Authorised Signature<br><span style="font-size: 8px; font-weight: normal; color: #666;">SM-TECH Computer & IT Solutions</span>
                            </td>
                        </tr>
                    </table>
                </div>
                <script>window.onload = function() {{ window.print(); }}</script>
            </body>
            </html>
            """
            
            st.success("১০টি রো বিশিষ্ট ৫\"x৭\" মেমো সফলভাবে তৈরি হয়েছে!")
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
    
    # নতুন ৪টি কলাম তৈরি করা হলো
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        item_name = st.text_input("New Products (পণ্যের নাম)")
    with col2:
        quantity = st.number_input("Quantity (পরিমাণ)", min_value=0, value=0)
    with col3:
        cost_price = st.number_input("Cost Price (ক্রয় মূল্য)", min_value=0, value=0)
    with col4:
        sell_rate = st.number_input("Sell Rate (বিক্রয় মূল্য)", min_value=0, value=0)
        
    if st.button("স্টক আপডেট করুন"):
        if item_name and quantity > 0:
            # স্বয়ংক্রিয়ভাবে আজকের তারিখ নিয়ে নিবে
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            st.session_state["stock_data"].append({
                "Date": current_date,
                "New Products": item_name,
                "Quantity": quantity,
                "Cost Price": cost_price,
                "Sell Rate": sell_rate
            })
            st.success(f"সফলভাবে '{item_name}' স্টকে যোগ করা হয়েছে!")
        else:
            st.error("দয়া করে পণ্যের নাম এবং সঠিক পরিমাণ লিখুন।")
            
    st.markdown("---")
    st.subheader("📋 বর্তমান স্টক তালিকা")
    
    # টেবিলে ডাটা দেখানোর জন্য অটোমেটিক Sl. (সিরিয়াল নম্বর) তৈরি
    if st.session_state["stock_data"]:
        display_data = []
        for idx, item in enumerate(st.session_state["stock_data"]):
            display_data.append({
                "Sl.": idx + 1,
                "Date": item["Date"],
                "New Products": item["New Products"],
                "Quantity": item["Quantity"],
                "Cost Price": item["Cost Price"],
                "Sell Rate": item["Sell Rate"]
            })
        st.table(display_data)
    else:
        st.info("স্টকে কোনো পণ্য নেই।")
