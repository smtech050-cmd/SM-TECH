# --- 🧾 POS ও ইনভয়েস মডিউল (আপডেটেড ডিজাইন) ---
    elif menu_choice == t["menu"][3]:
        st.title(t["pos_title"])
        
        # ইনপুট ফিল্ডসমূহ
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            cust_name = st.text_input(t["c_name"], value=t["walking"])
            cust_address = st.text_input("Address (ঠিকানা)", value="Dhaka, Bangladesh")
        with col_in2:
            item_desc = st.text_input("Description (বিবরণ)", value="Computer Parts / Service")
            total_bill = st.number_input(t["total_bill"], min_value=0, value=1500)
            
        st.write("---")
        
        # ইনভয়েস জেনারেট বাটন
        if st.button(t["btn_inv"]):
            inv_num = f"SM-{int(datetime.datetime.now().timestamp())}"
            current_date = datetime.datetime.now().strftime('%d-%m-%Y')
            
            # হুবহু আপনার ছবির মতো ডিজাইন (HTML/CSS)
            invoice_html = f"""
            <div style="border: 4px solid #1a365d; padding: 25px; border-radius: 5px; background-color: white; color: black; font-family: Arial, sans-serif; max-width: 750px; margin: auto;">
                
                <!-- হেডার সেকশন -->
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 65%;">
                            <span style="font-size: 45px; font-weight: bold; color: #1e3a8a;">SM-TECH</span><br>
                            <span style="font-size: 14px; font-weight: bold; color: #10b981; letter-spacing: 2px;">COMPUTER & IT SOLUTION</span><br>
                            <span style="font-size: 12px; font-style: italic; color: #333;">Smart Technology-Trusted Service</span>
                        </td>
                        <td style="width: 35%; text-align: right; font-size: 13px; line-height: 1.4;">
                            <strong style="font-size: 16px; color: #1e3a8a;">S.m. Ibrahim</strong><br>
                            Owner<br>
                            01940-556114<br>
                            01810-499166
                        </td>
                    </tr>
                </table>
                
                <hr style="border: 1px solid #1a365d; margin-top: 10px; margin-bottom: 15px;">
                
                <!-- কাস্টমার ও ইনভয়েস ইনফো -->
                <table style="width: 100%; font-size: 14px; margin-bottom: 15px;">
                    <tr>
                        <td style="width: 60%; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 8px; font-weight: bold; border-radius: 3px;">Bill To</span>
                            <span style="margin-left: 5px;"><b>Name:</b> {cust_name}</span><br>
                            <span style="margin-left: 53px; display: inline-block; margin-top: 5px;"><b>Address:</b> {cust_address}</span>
                        </td>
                        <td style="width: 40%; text-align: right; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 15px; font-weight: bold; border-radius: 3px; font-size: 16px;">INVOICE</span><br>
                            <span style="display: inline-block; margin-top: 8px;"><b>Invoice No:</b> {inv_num}</span><br>
                            <span><b>Date:</b> {current_date}</span>
                        </td>
                    </tr>
                </table>
                
                <!-- মেইন প্রোডাক্ট টেবিল -->
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px;">
                    <thead>
                        <tr style="background-color: #1e3a8a; color: white; text-align: center;">
                            <th style="border: 1px solid #1a365d; padding: 8px; width: 8%;">S.L</th>
                            <th style="border: 1px solid #1a365d; padding: 8px; width: 52%;">DESCRIPTION</th>
                            <th style="border: 1px solid #1a365d; padding: 8px; width: 10%;">QTY</th>
                            <th style="border: 1px solid #1a365d; padding: 8px; width: 15%;">U.PRICE</th>
                            <th style="border: 1px solid #1a365d; padding: 8px; width: 15%;">AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="text-align: center;">
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d; padding: 12px;">1</td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d; padding: 12px; text-align: left;">{item_desc}</td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d; padding: 12px;">1</td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d; padding: 12px;">{total_bill}</td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d; padding: 12px; font-weight: bold;">{total_bill}</td>
                        </tr>
                        <!-- ফাকা ঘরের জন্য ডামি রো -->
                        <tr style="height: 120px;">
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d;"></td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d;"></td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d;"></td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d;"></td>
                            <td style="border-left: 1px solid #1a365d; border-right: 1px solid #1a365d;"></td>
                        </tr>
                        <!-- সাব টোটাল অংশ -->
                        <tr style="background-color: #fafafa;">
                            <td colspan="3" style="border: 1px solid #1a365d; border-top: 2px solid #1a365d;"></td>
                            <td style="border: 1px solid #1a365d; border-top: 2px solid #1a365d; padding: 8px; text-align: center; font-weight: bold; background-color: #1e3a8a; color: white;">SUB TOTAL</td>
                            <td style="border: 1px solid #1a365d; border-top: 2px solid #1a365d; padding: 8px; text-align: center; font-weight: bold;">{total_bill} BDT</td>
                        </tr>
                    </tbody>
                </table>
                
                <!-- পেমেন্ট মেথড ও সিগনেচার -->
                <table style="width: 100%; margin-top: 35px; font-size: 13px;">
                    <tr>
                        <td style="width: 50%; vertical-align: bottom;">
                            <div style="border: 1px solid #1a365d; display: inline-block; border-radius: 3px;">
                                <div style="background-color: #1e3a8a; color: white; padding: 3px 10px; font-weight: bold; font-size: 11px;">Payment Methods</div>
                                <div style="padding: 5px 10px; font-weight: bold; color: #333;">Cash | Bkash | Nagad | Bank</div>
                            </div>
                        </td>
                        <td style="width: 50%; text-align: right; vertical-align: bottom;">
                            <div style="display: inline-block; text-align: center; width: 180px;">
                                <hr style="border: 0; border-top: 1px solid #333; margin-bottom: 5px;">
                                <b>Authorised Signature</b><br>
                                <span style="font-size: 11px; color: #555;">SM-TECH<br>Computer & IT Solutions</span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            """
            
            # স্ক্রিনে ইনভয়েস শো করা
            st.markdown(invoice_html, unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allowed_html=False) # standard spacing
            
            # 📥 ডাউনলোড ও প্রিন্ট করার বাটন
            # ব্রাউজারের প্রিন্ট ডায়ালগ ওপেন করার জন্য ছোট একটি জাভাস্ক্রিপ্ট হ্যাক
            st.components.v1.html(f"""
                <script>
                function printInv() {{
                    var printWindow = window.open('', '_blank');
                    printWindow.document.write(`<html><head><title>Print Invoice</title></head><body>${`{invoice_html}`}</body></html>`);
                    printWindow.document.close();
                    printWindow.print();
                }}
                </script>
                <div style="text-align: center;">
                    <button onclick="printInv()" style="background-color: #10b981; color: white; padding: 10px 25px; font-size: 16px; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        📥 Download PDF / Print Invoice
                    </button>
                </div>
            """, height=60)
