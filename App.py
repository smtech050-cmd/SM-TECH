import streamlit as st
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH Management", page_icon="💻", layout="wide")

# সেশন স্টেট ইনিশিয়ালাইজেশন
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = [
       
       
    ]

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
    
    col_c, col_d = st.columns(2)
    with col_c:
        service_charge = st.number_input("Service Charge / Repair Bill", min_value=0, value=0)
        parts_qty = st.number_input("Used Parts QTY (পার্টসের সংখ্যা)", min_value=0, value=0)
    with col_d:
        parts_uprice = st.number_input("Used Parts U.PRICE (পার্টসের একক মূল্য)", min_value=0, value=0)
        discount = st.number_input("DISCOUNT (ডিসকাউন্ট টাকা)", min_value=0, value=0)
    
    if st.button("ইনভয়েস পিডিএফ তৈরি করুন"):
        if customer_name:
            # সঠিক হিসাব-নিকাশ
            if parts_qty > 0:
                actual_parts_uprice = parts_uprice
                parts_total = parts_qty * parts_uprice
                display_qty = str(parts_qty)
            else:
                actual_parts_uprice = 0
                parts_total = 0
                display_qty = "-"
                
            sub_total = service_charge + parts_total
            total_bill = sub_total - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # হেডারের ফন্ট বড় এবং ডানপাশের ফাঁকা অংশ ভরাট করা পরিমার্জিত HTML ডিজাইন
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Arial', sans-serif; background-color: #f0f0f0; padding: 5px; margin: 0; }}
                    .main-pad {{ max-width: 800px; margin: auto; padding: 30px; border: 2px solid #0a4da2; background-color: #fff; box-sizing: border-box; }}
                    
                    /* হেডার অংশ - সাইজ ও গ্যাপ ফিক্স */
                    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
                    .logo-main {{ font-size: 64px; font-weight: 900; font-style: italic; color: #e63946; margin: 0; line-height: 0.85; font-family: 'Impact', 'Arial Black', sans-serif; letter-spacing: -1px; }}
                    .logo-main span {{ color: #0a4da2; }}
                    .sub-title {{ font-size: 18px; font-weight: bold; color: #2a9d8f; letter-spacing: 1.5px; margin: 5px 0 3px 0; font-family: 'Arial Black', sans-serif; }}
                    .tagline {{ font-size: 14px; font-weight: bold; color: #333; margin: 0; }}
                    
                    .owner-side {{ text-align: right; font-size: 16px; color: #0a4da2; font-weight: bold; line-height: 1.4; vertical-align: top; padding-top: 5px; padding-right: 5px; }}
                    .owner-name {{ font-size: 22px; font-weight: bold; color: #0a4da2; display: inline-block; margin-bottom: 4px; }}
                    
                    /* ইনভয়েস বার */
                    .invoice-bar-table {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
                    .bill-to {{ font-size: 15px; font-weight: bold; color: white; background-color: #0a4da2; padding: 4px 10px; border-radius: 2px; }}
                    .invoice-badge {{ background-color: #0a4da2; color: white; font-size: 22px; font-weight: bold; text-align: center; padding: 5px 30px; letter-spacing: 2px; border-radius: 3px; display: inline-block; }}
                    
                    .info-lines {{ font-size: 15px; line-height: 2.2; }}
                    .dot-line {{ border-bottom: 1px dotted #555; display: inline-block; padding-left: 5px; font-weight: bold; color: #000; }}
                    
                    /* টেবিল ডিজাইন */
                    .item-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; border: 2px solid #0a4da2; }}
                    .item-table th {{ background-color: #0a4da2; color: white; padding: 10px; font-size: 15px; font-weight: bold; border: 1px solid #fff; text-align: center; }}
                    .item-table td {{ padding: 14px 10px; border-left: 2px solid #0a4da2; border-right: 2px solid #0a4da2; border-bottom: 1px solid #e0e0e0; font-size: 15px; }}
                    
                    /* সাবটোটাল বক্স */
                    .subtotal-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 8px; text-align: center; font-size: 15px; }}
                    .subtotal-val {{ text-align: right; font-weight: bold; border: 2px solid #0a4da2; background-color: #f8f9fa; font-size: 16px; color: #0a4da2; padding: 8px 10px; }}
                    
                    /* পেমেন্ট ও সিগনেচার */
                    .bottom-area {{ width: 100%; border-collapse: collapse; margin-top: 40px; }}
                    .pay-method-box {{ border: 2px solid #0a4da2; border-radius: 4px; padding: 12px; width: 310px; font-size: 14px; font-weight: bold; color: #0a4da2; }}
                    .pay-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 2px 8px; display: inline-block; margin-bottom: 10px; }}
                    
                    .signature-area {{ text-align: right; font-size: 14px; font-weight: bold; color: #333; vertical-align: bottom; }}
                    .sig-line {{ border-top: 1px solid #333; width: 190px; display: inline-block; margin-bottom: 5px; }}
                    
                    @media print {{
                        body {{ background-color: #fff; padding: 0; }}
                        .main-pad {{ border: none; padding: 15px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="main-pad">
                    <!-- হেডার অংশ (সাইজ বড় ও ফাঁকা কমানো হয়েছে) -->
                    <table class="header-table">
                        <tr>
                            <td style="width: 60%;">
                                <p class="logo-main">SM-<span>TECH</span></p>
                                <p class="sub-title">COMPUTER & IT SOLUTION</p>
                                <p class="tagline">Smart Technology-Trusted Service</p>
                            </td>
                            <td class="owner-side" style="width: 40%;">
                                <span class="owner-name">S.m. Ibrahim</span><br>
                                Owner<br>
                                📞 01940-556114<br>
                                📞 01810-499166
                            </td>
                        </tr>
                    </table>
                    
                    <!-- কাস্টমার ও মেমো ইনফো -->
                    <table class="invoice-bar-table">
                        <tr>
                            <td style="width: 55%; vertical-align: top;">
                                <div class="info-lines">
                                    <span class="bill-to">Bill To</span> Name: <span class="dot-line" style="width: 260px;">{customer_name}</span><br>
                                    Address: <span class="dot-line" style="width: 293px;">{customer_address}</span>
                                </div>
                            </td>
                            <td style="width: 45%; text-align: right; vertical-align: top;">
                                <div class="invoice-badge" style="margin-bottom: 10px;">INVOICE</div>
                                <div class="info-lines">
                                    Invoice No: <span class="dot-line" style="width: 150px; text-align: left;">{invoice_no}</span><br>
                                    Date: <span class="dot-line" style="width: 150px; text-align: left;">{current_date}</span>
                                </div>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- আইটেম টেবিল -->
                    <table class="item-table">
                        <thead>
                            <tr>
                                <th style="width: 8%;">S.L</th>
                                <th style="width: 52%;">DESCRIPTION</th>
                                <th style="width: 10%;">QTY</th>
                                <th style="width: 15%;">U.PRICE</th>
                                <th style="width: 15%;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="text-align: center;">1</td>
                                <td>Service Charge / Repair Bill</td>
                                <td style="text-align: center;">1</td>
                                <td style="text-align: right;">{service_charge} Tk</td>
                                <td style="text-align: right; font-weight: bold;">{service_charge} Tk</td>
                            </tr>
                            <tr>
                                <td style="text-align: center;">2</td>
                                <td>Used Parts Cost</td>
                                <td style="text-align: center;">{display_qty}</td>
                                <td style="text-align: right;">{f"{actual_parts_uprice} Tk" if actual_parts_uprice > 0 else "-"}</td>
                                <td style="text-align: right; font-weight: bold;">{parts_total} Tk</td>
                            </tr>
                            <!-- ডামি রো গ্যাপ ঠিক রাখার জন্য -->
                            <tr><td style="height:30px;"></td><td></td><td></td><td></td><td></td></tr>
                            <tr><td style="height:30px;"></td><td></td><td></td><td></td><td></td></tr>
                            
                            <!-- ডিসকাউন্ট ও সাবটোটাল -->
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td style="text-align: right; font-weight: bold; border-top: 2px solid #0a4da2; padding: 8px;">Discount:</td>
                                <td style="text-align: right; font-weight: bold; color: red; border-top: 2px solid #0a4da2; padding: 8px;">{discount} Tk</td>
                            </tr>
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td class="subtotal-title">SUB TOTAL</td>
                                <td class="subtotal-val">{total_bill} Tk</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <!-- পেমেন্ট এবং সিগনেচার -->
                    <table class="bottom-area">
                        <tr>
                            <td>
                                <div class="pay-method-box">
                                    <div class="pay-title">Payment Methods</div><br>
                                    <input type="checkbox"> Cash &nbsp;&nbsp;
                                    <input type="checkbox"> Bkash &nbsp;&nbsp;
                                    <input type="checkbox"> Nagad &nbsp;&nbsp;
                                    <input type="checkbox"> Bank
                                </div>
                            </td>
                            <td class="signature-area">
                                <div class="sig-line"></div><br>
                                Authorised Signature<br>
                                <span style="font-size: 12px; font-weight: normal; color: #666;">SM-TECH Computer & IT Solutions</span>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <script>
                    window.onload = function() {{
                        window.print();
                    }}
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
