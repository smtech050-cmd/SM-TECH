import streamlit as st
import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="SM-TECH Management", page_icon="💻", layout="wide")

# সেশন স্টেট ইনিশিয়ালাইজেশন (স্টকের ডাটা ধরে রাখার জন্য)
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
    
    if st.button("ইনভয়েস পিডিএফ তৈরি করুন"):
        if customer_name:
            total_bill = service_charge + parts_cost - discount
            current_date = datetime.date.today().strftime("%d-%m-%Y")
            
            # আপনার আসল প্যাডের ডিজাইন অনুযায়ী প্রফেশনাল HTML/PDF ফরম্যাট
            invoice_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Arial', sans-serif; color: #333; padding: 20px; }}
                    .invoice-box {{ max-width: 600px; margin: auto; padding: 30px; border: 2px solid #0056b3; border-radius: 10px; background-color: #fff; }}
                    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                    .logo-title {{ font-size: 32px; font-weight: bold; color: #e63946; margin: 0; line-height: 1; }}
                    .sub-title {{ font-size: 14px; color: #0056b3; font-weight: bold; margin: 5px 0 0 0; }}
                    .tagline {{ font-size: 12px; font-style: italic; color: #555; margin: 2px 0 0 0; }}
                    .owner-info {{ text-align: right; font-size: 13px; line-height: 1.4; }}
                    .bill-section {{ width: 100%; margin-bottom: 20px; font-size: 14px; border-bottom: 2px dashed #0056b3; padding-bottom: 10px; }}
                    .invoice-title {{ text-align: center; font-size: 22px; font-weight: bold; color: #fff; background-color: #0056b3; padding: 5px; margin: 10px 0; border-radius: 5px; letter-spacing: 2px; }}
                    .data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    .data-table th {{ background-color: #0056b3; color: white; text-align: left; padding: 8px; font-size: 14px; }}
                    .data-table td {{ padding: 10px 8px; border-bottom: 1px solid #ddd; font-size: 14px; }}
                    .total-row td {{ font-weight: bold; border-top: 2px solid #0056b3; background-color: #f8f9fa; }}
                    .payment-methods {{ margin-top: 25px; font-size: 13px; border: 1px solid #0056b3; padding: 10px; border-radius: 5px; display: inline-block; width: 50%; }}
                    .footer-section {{ margin-top: 50px; width: 100%; font-size: 13px; }}
                    .signature {{ text-align: right; border-top: 1px solid #333; display: inline-block; float: right; padding-top: 5px; font-weight: bold; }}
                    @media print {{
                        body {{ padding: 0; }}
                        .invoice-box {{ border: none; padding: 0; }}
                    }}
                </style>
            </head>
            <body>
                <div class="invoice-box">
                    <table class="header-table">
                        <tr>
                            <td>
                                <p class="logo-title">SM-TECH</p>
                                <p class="sub-title">COMPUTER & IT SOLUTION</p>
                                <p class="tagline">Smart Technology-Trusted Service</p>
                            </td>
                            <td class="owner-info">
                                <strong>S.m. Ibrahim</strong><br>
                                Owner<br>
                                📞 01940-556114<br>
                                📞 01810-499166
                            </td>
                        </tr>
                    </table>
                    
                    <div class="invoice-title">INVOICE / CASH MEMO</div>
                    
                    <table class="bill-section">
                        <tr>
                            <td><strong>Bill To Name:</strong> {customer_name}</td>
                            <td style="text-align: right;"><strong>Date:</strong> {current_date}</td>
                        </tr>
                    </table>
                    
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 10%;">S.L</th>
                                <th style="width: 55%;">DESCRIPTION</th>
                                <th style="width: 15%; text-align: center;">QTY</th>
                                <th style="width: 20%; text-align: right;">AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>Service Charge / Repair Bill</td>
                                <td style="text-align: center;">1</td>
                                <td style="text-align: right;">{service_charge} Tk</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>Used Parts Cost</td>
                                <td style="text-align: center;">-</td>
                                <td style="text-align: right;">{parts_cost} Tk</td>
                            </tr>
                            <tr class="total-row">
                                <td colspan="3" style="text-align: right;">DISCOUNT:</td>
                                <td style="text-align: right; color: red;">{discount} Tk</td>
                            </tr>
                            <tr class="total-row" style="background-color: #e2eafc;">
                                <td colspan="3" style="text-align: right; font-size: 16px; color: #0056b3;">SUB TOTAL:</td>
                                <td style="text-align: right; font-size: 16px; color: #0056b3;">{total_bill} Tk</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div style="margin-top: 20px;">
                        <div class="payment-methods">
                            <strong>Payment Methods:</strong><br>
                            <span style="margin-right: 10px;">[ ] Cash</span> 
                            <span style="margin-right: 10px;">[ ] Bkash</span> 
                            <span style="margin-right: 10px;">[ ] Nagad</span> 
                            <span>[ ] Bank</span>
                        </div>
                    </div>
                    
                    <div class="footer-section">
                        <div class="signature">
                            Authorised Signature<br>
                            <span style="font-size: 11px; color: #555;">SM-TECH Computer & IT Solutions</span>
                        </div>
                        <div style="clear: both;"></div>
                    </div>
                </div>
                
                <!-- স্বয়ংক্রিয়ভাবে প্রিন্ট/পিডিএফ সেভ ডায়ালগ ওপেন করার স্ক্রিপ্ট -->
                <script>
                    window.onload = function() {{
                        window.print();
                    }}
                </script>
            </body>
            </html>
            """
            
            st.success("ইনভয়েস PDF সফলভাবে তৈরি হয়েছে!")
            
            # ডাউনলোড বাটন (ডাউনলোড করার সাথে সাথে এটি প্রিন্ট রেডি ডিরেক্ট পিডিএফ ফরম্যাটে নামবে)
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
