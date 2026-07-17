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

# সাইডবার মেনু
st.sidebar.title("💻 SM-TECH")
choice = st.sidebar.radio("মেনু সিলেক্ট করুন:", ["📄 Invoice Generator", "📦 Stock Management"])

# ==========================================
# ১. ইনভয়েস জেনারেটর (INVOICE GENERATOR)
# ==========================================
if choice == "📄 Invoice Generator":
    st.title("📄 ক্যাশ মেমো / ইনভয়েস জেনারেটর")
    
    # আপনার প্যাড অনুযায়ী ইনপুট ফিল্ডসমূহ
    col_a, col_b = st.columns(2)
    with col_a:
        customer_name = st.text_input("Name (কাস্টমারের নাম)")
        customer_address = st.text_input("Address (ঠিকানা)")
    with col_b:
        invoice_no = st.text_input("Invoice No (মেমো নম্বর)", value="101")
    
    st.markdown("---")
    st.subheader("🛒 বিলের বিবরণ")
    
    # সার্ভিস ও পার্টসের হিসাব (প্যাডের কলাম অনুযায়ী)
    col_c, col_d = st.columns(2)
    with col_c:
        service_charge = st.number_input("Service Charge / Repair Bill", min_value=0, value=0)
        parts_qty = st.number_input("Used Parts QTY (পার্টসের সংখ্যা)", min_value=0, value=0)
    with col_d:
        parts_uprice = st.number_input("Used Parts U.PRICE (পার্টসের একক মূল্য)", min_value=0, value=0)
        discount = st.number_input("DISCOUNT (ডিসকাউন্ট টাকা)", min_value=0, value=0)
    
    if st.button("ইনভয়েস পিডিএফ তৈরি করুন"):
        if customer_name:
            # হিসাব-নিকাশ
            parts_total = parts_qty * parts_uprice
            sub_total = service_charge + parts_total
            total_bill = sub_total - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # আপনার আসল প্যাডের হুবহু ক্লোন করা HTML ডিজাইন
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Arial', sans-serif; background-color: #f0f0f0; padding: 10px; }}
                    .main-pad {{ max-width: 750px; margin: auto; padding: 25px; border: 3px double #0a4da2; background-color: #fff; position: relative; min-height: 950px; }}
                    
                    /* হেডার অংশ */
                    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
                    .logo-side {{ width: 65%; }}
                    .logo-main {{ font-size: 52px; font-weight: bold; font-style: italic; color: #e63946; margin: 0; line-height: 0.9; font-family: 'Impact', sans-serif; }}
                    .logo-main span {{ color: #0a4da2; }}
                    .sub-title {{ font-size: 15px; font-weight: bold; color: #2a9d8f; letter-spacing: 1px; margin: 2px 0; }}
                    .tagline {{ font-size: 13px; font-weight: 500; color: #333; margin: 0; }}
                    
                    .owner-side {{ width: 35%; text-align: right; font-size: 14px; color: #0a4da2; font-weight: bold; line-height: 1.3; }}
                    .owner-name {{ font-size: 18px; color: #0a4da2; margin-bottom: 2px; }}
                    
                    /* ইনভয়েস বার */
                    .invoice-bar-table {{ width: 100%; margin-top: 15px; border-collapse: collapse; }}
                    .bill-to {{ font-size: 16px; font-weight: bold; color: white; background-color: #0a4da2; padding: 4px 10px; border-radius: 3px 0 0 3px; display: inline-block; }}
                    .invoice-badge {{ background-color: #0a4da2; color: white; font-size: 22px; font-weight: bold; text-align: center; padding: 3px 20px; letter-spacing: 2px; border-radius: 3px; }}
                    
                    .info-lines {{ font-size: 15px; padding: 5px 0; line-height: 1.8; }}
                    .dot-line {{ border-bottom: 1px dotted #555; display: inline-block; min-width: 250px; padding-left: 5px; font-weight: bold; color: #000; }}
                    
                    /* মেইন টেবিল ডিজাইন (হুবহু প্যাডের মতো) */
                    .item-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; border: 2px solid #0a4da2; }}
                    .item-table th {{ background-color: #0a4da2; color: white; padding: 8px; font-size: 14px; font-weight: bold; border: 1px solid #fff; text-align: center; }}
                    .item-table td {{ padding: 10px 8px; border-left: 2px solid #0a4da2; border-right: 2px solid #0a4da2; border-bottom: 1px solid #ddd; font-size: 14px; height: 35px; }}
                    
                    /* সাবটোটাল এরিয়া */
                    .subtotal-box {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 8px; text-align: center; font-size: 15px; }}
                    
                    /* পেমেন্ট ও সিগনেচার */
                    .bottom-area {{ width: 100%; border-collapse: collapse; margin-top: 40px; }}
                    .pay-method-box {{ border: 2px solid #0a4da2; border-radius: 5px; padding: 8px; width: 280px; font-size: 14px; }}
                    .pay-title {{ background-color: #0a4da2; color: white; font-weight: bold; padding: 2px 8px; display: inline-block; margin-bottom: 8px; transform: skew(-10deg); }}
                    
                    .signature-area {{ text-align: right; font-size: 14px; font-weight: bold; color: #333; line-height: 1.3; vertical-align: bottom; padding-bottom: 10px; }}
                    .sig-line {{ border-top: 1px solid #333; width: 200px; display: inline-block; margin-bottom: 3px; }}
                    
                    @media print {{
                        body {{ background-color: #fff; padding: 0; }}
                        .main-pad {{ border: none; padding: 0; min-height: auto; }}
                    }}
                </style>
            </head>
            <body>
                <div class="main-pad">
                    <!-- টপ হেডার -->
                    <table class="header-table">
                        <tr>
                            <td class="logo-side">
                                <p class="logo-main">SM-<span>TECH</span></p>
                                <p class="sub-title">COMPUTER & IT SOLUTION</p>
                                <p class="tagline">Smart Technology-Trusted Service</p>
                            </td>
                            <td class="owner-side">
                                <span class="owner-name">S.m. Ibrahim</span><br>
                                Owner<br>
                                01940-556114<br>
                                01810-499166
                            </td>
                        </tr>
                    </table>
                    
                    <!-- ইনভয়েস বার ও কাস্টমার ইনফো -->
                    <table class="invoice-bar-table">
                        <tr>
                            <td style="width: 60%; vertical-align: top;">
                                <div class="info-lines">
                                    <span class="bill-to">Bill To</span> Name: <span class="dot-line" style="min-width: 320px;">{customer_name}</span><br>
                                    Address: <span class="dot-line" style="min-width: 343px;">{customer_address}</span>
                                </div>
                            </td>
                            <td style="width: 40%; text-align: right; vertical-align: top;">
                                <div class="invoice-badge" style="float: right; margin-bottom: 10px;">INVOICE</div>
                                <div style="clear: both;"></div>
                                <div class="info-lines">
                                    Invoice No: <span class="dot-line" style="min-width: 120px;">{invoice_no}</span><br>
                                    Date: <span class="dot-line" style="min-width: 120px;">{current_date}</span>
                                </div>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- মেইন আইটেম টেবিল -->
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
                            <!-- প্রথম রো: সার্ভিস চার্জ -->
                            <tr>
                                <td style="text-align: center;">1</td>
                                <td>Service Charge / Repair Bill</td>
                                <td style="text-align: center;">1</td>
                                <td style="text-align: right;">{service_charge} Tk</td>
                                <td style="text-align: right; font-weight: bold;">{service_charge} Tk</td>
                            </tr>
                            <!-- দ্বিতীয় রো: পার্টস খরচ (যদি থাকে) -->
                            <tr>
                                <td style="text-align: center;">2</td>
                                <td>Used Parts Cost</td>
                                <td style="text-align: center;">{parts_qty if parts_qty > 0 else '-'}</td>
                                <td style="text-align: right;">{parts_uprice if parts_uprice > 0 else '-'} Tk</td>
                                <td style="text-align: right; font-weight: bold;">{parts_total} Tk</td>
                            </tr>
                            <!-- ডামি ফাঁকা রো (প্যাডের মতো লুক আনার জন্য) -->
                            <tr><td></td><td></td><td></td><td></td><td></td></tr>
                            <tr><td></td><td></td><td></td><td></td><td></td></tr>
                            <tr><td></td><td></td><td></td><td></td><td></td></tr>
                            
                            <!-- সাবটোটাল ও ডিসকাউন্ট অংশ -->
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td style="text-align: right; font-weight: bold; border-top: 2px solid #0a4da2;">Discount:</td>
                                <td style="text-align: right; font-weight: bold; color: red; border-top: 2px solid #0a4da2;">{discount} Tk</td>
                            </tr>
                            <tr>
                                <td colspan="3" style="border: none;"></td>
                                <td class="subtotal-box">SUB TOTAL</td>
                                <td style="text-align: right; font-weight: bold; border: 2px solid #0a4da2; background-color: #f8f9fa; font-size: 16px; color: #0a4da2;">{total_bill} Tk</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <!-- নিচের পেমেন্ট ও সিগনেচার এরিয়া -->
                    <table class="bottom-area">
                        <tr>
                            <td style="width: 50%;">
                                <div class="pay-method-box">
                                    <div class="pay-title">Payment Methods</div><br>
                                    <input type="checkbox"> Cash &nbsp;&nbsp;
                                    <input type="checkbox"> Bkash &nbsp;&nbsp;
                                    <input type="checkbox"> Nagad &nbsp;&nbsp;
                                    <input type="checkbox"> Bank
                                </div>
                            </td>
                            <td class="signature-area" style="width: 50%;">
                                <div class="sig-line"></div><br>
                                Authorised Signature<br>
                                <span style="font-size: 12px; font-weight: normal; color: #555;">SM-TECH Computer & IT Solutions</span>
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
