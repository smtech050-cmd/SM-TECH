# ৫. সেল ইনভয়েস (হুবহু ডিজাইনার ক্যাশ মেমোর মতো A5 প্রিন্ট)
    elif st.session_state.current_menu == "Sell Invoice":
        st.title("🧾 ইনভয়েস জেনারেটর")
        
        # ইনপুট ফিল্ডসমূহ
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

        # ক্লিয়ার বাটন
        if st.session_state.invoice_items:
            if st.button("🗑️ Clear All Items"):
                st.session_state.invoice_items = []
                st.rerun()

        # আইটেম টেবিল হিসাব
        sub_total = sum(item["Amount"] for item in st.session_state.invoice_items)
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        current_time_stamp = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
        
        # টেবিল রিকর্ড জেনারেট (সর্বমোট ১০ সারি ফিলআপ রাখার জন্য)
        rows_html = ""
        max_rows = 10
        for i in range(max_rows):
            if i < len(st.session_state.invoice_items):
                item = st.session_state.invoice_items[i]
                rows_html += f"""
                <tr>
                    <td style="text-align:center;">{i+1}</td>
                    <td>{item['Description']}</td>
                    <td style="text-align:center;">{item['Qty']}</td>
                    <td style="text-align:right;">{item['Price']:,}</td>
                    <td style="text-align:right;">{item['Amount']:,}</td>
                </tr>
                """
            else:
                rows_html += """
                <tr>
                    <td>&nbsp;</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                """

        # সম্পূর্ণ A5 ইনভয়েস টেমপ্লেট
        invoice_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @page {{
                size: A5 portrait;
                margin: 5mm;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 10px;
                color: #000;
                background: #fff;
            }}
            .invoice-box {{
                border: 2px solid #1a365d;
                padding: 12px;
                border-radius: 8px;
                position: relative;
                min-height: 94vh;
                box-sizing: border-box;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #1a365d;
                padding-bottom: 8px;
            }}
            .logo-text {{
                font-size: 26px;
                font-weight: 900;
                color: #0d47a1;
                line-height: 1;
            }}
            .logo-sub {{
                font-size: 10px;
                font-weight: 700;
                color: #2e7d32;
                letter-spacing: 0.5px;
            }}
            .owner-info {{
                text-align: right;
                font-size: 11px;
                font-weight: 600;
                color: #1a365d;
            }}
            .bill-sec {{
                margin-top: 10px;
                display: flex;
                justify-content: space-between;
                font-size: 12px;
            }}
            .invoice-title {{
                background: #1a365d;
                color: white;
                padding: 2px 10px;
                font-weight: bold;
                border-radius: 3px;
                display: inline-block;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 11px;
            }}
            th {{
                background-color: #1a365d;
                color: white;
                border: 1px solid #1a365d;
                padding: 5px;
            }}
            td {{
                border: 1px solid #1a365d;
                padding: 5px;
                height: 18px;
            }}
            .subtotal-box {{
                background: #1a365d;
                color: white;
                font-weight: bold;
                text-align: right;
                padding: 5px 10px;
            }}
            .footer-sec {{
                margin-top: 25px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                font-size: 11px;
            }}
            .payment-methods {{
                border: 1px solid #1a365d;
                padding: 4px;
                font-weight: bold;
                font-size: 10px;
            }}
            .print-btn-container {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .btn-print {{
                background: #0066ff;
                color: white;
                border: none;
                padding: 10px 25px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }}
            @media print {{
                .print-btn-container {{ display: none !important; }}
                body {{ padding: 0; }}
            }}
        </style>
        </head>
        <body>

        <div class="print-btn-container">
            <button class="btn-print" onclick="window.print()">🖨️ প্রিন্ট করুন / Save as PDF (A5)</button>
        </div>

        <div class="invoice-box">
            <div class="header">
                <div>
                    <div class="logo-text">SM-TECH</div>
                    <div class="logo-sub">COMPUTER & IT SOLUTION</div>
                    <div style="font-size: 9px; color: #555;">Smart Technology-Trusted Service</div>
                </div>
                <div class="owner-info">
                    <div style="font-size: 13px; font-weight: bold;">S.m. Ibrahim</div>
                    <div>Owner</div>
                    <div>01940-556114</div>
                    <div>01810-499166</div>
                </div>
            </div>

            <div class="bill-sec">
                <div>
                    <b>Bill To:</b> {cust_name}<br>
                    <b>Address:</b> {cust_address}
                </div>
                <div style="text-align: right;">
                    <span class="invoice-title">INVOICE</span><br>
                    <b>Invoice No:</b> {inv_custom_num}<br>
                    <b>Date:</b> {current_date}
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 8%;">S.L</th>
                        <th style="width: 48%;">DESCRIPTION</th>
                        <th style="width: 10%;">QTY</th>
                        <th style="width: 17%;">U.PRICE</th>
                        <th style="width: 17%;">AMOUNT</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr>
                        <td colspan="3" style="border:none;"><b>Amount In Words:</b> ..................................................</td>
                        <td style="font-weight:bold; text-align:right; background:#f0f0f0;">SUB TOTAL</td>
                        <td style="font-weight:bold; text-align:right; background:#f0f0f0;">{sub_total:,}</td>
                    </tr>
                </tbody>
            </table>

            <div class="footer-sec">
                <div>
                    <div class="payment-methods">
                        Payment Methods:<br>
                        Cash | Bkash | Nagad | Bank
                    </div>
                </div>
                <div style="text-align: center;">
                    ------------------------------------------<br>
                    <b>Authorised Signature</b><br>
                    <span style="font-size: 9px;">SM-TECH Computer & IT Solutions</span>
                </div>
            </div>

            <div style="position: absolute; bottom: 3px; left: 12px; right: 12px; display: flex; justify-content: space-between; font-size: 8px; color: #777;">
                <span>Print Date: {current_time_stamp}</span>
                <span>Website: smtech.com.bd</span>
            </div>
        </div>

        </body>
        </html>
        """

        # অন-স্ক্রিন প্রিভিউ এবং সরাসরি প্রিন্ট অপশন
        st.components.v1.html(invoice_template, height=750, scrolling=True)
