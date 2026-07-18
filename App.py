if st.button(t["btn_inv"]):
            inv_num = f"{int(datetime.datetime.now().timestamp()) % 100000}"
            current_date = datetime.datetime.now().strftime('%d-%m-%Y')
            
            logo_path = "logo.png" 
            
            # 📐 H 7" এবং W 5" সাইজের আপগ্রেডেড ক্যাশ মেমো থিম
            invoice_html = f"""
            <div id="print-area" style="
                border: 3px solid #1e3a8a; 
                padding: 18px; 
                background-color: white; 
                color: black; 
                font-family: 'Arial', sans-serif; 
                width: 5in; 
                height: 7in; 
                margin: auto; 
                border-radius: 4px;
                box-sizing: border-box;
                position: relative;
            ">
                
                <!-- টপ ব্র্যান্ডিং হেডার উইথ লোগো (স্পেসিং ও সাইজ বৃদ্ধি করা হয়েছে) -->
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 5px;">
                    <tr>
                        <td style="width: 20%; vertical-align: middle; text-align: left;">
                            <img src="{logo_path}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover;" onerror="this.style.display='none';">
                        </td>
                        <td style="width: 48%; vertical-align: middle; padding-left: 8px;">
                            <span style="font-size: 30px; font-weight: 900; color: #1e3a8a; font-family: 'Arial Black', Impact, sans-serif; line-height: 1.1; display: block; letter-spacing: -0.5px;">SM-TECH</span>
                            <span style="font-size: 8.5px; font-weight: 800; color: #059669; letter-spacing: 0.8px; display: block; margin-top: 2px;">COMPUTER & IT SOLUTION</span>
                            <span style="font-size: 8px; font-style: italic; color: #555; display: block; margin-top: 2px;">Smart Technology-Trusted Service</span>
                        </td>
                        <td style="width: 32%; text-align: right; font-size: 11px; line-height: 1.4; vertical-align: middle; font-weight: bold; color: #111;">
                            <span style="font-size: 14px; font-weight: 900; color: #1e3a8a; display: block; margin-bottom: 2px;">S.m. Ibrahim</span>
                            <span style="font-size: 10px; color: #555; display: block; margin-top: -3px; margin-bottom: 2px; font-weight: normal;">Owner</span>
                            <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01940-556114</span>
                            <span style="font-size: 11.5px; font-weight: 800; display: block; letter-spacing: 0.2px;">01810-499166</span>
                        </td>
                    </tr>
                </table>
                
                <div style="border-top: 2.5px solid #1e3a8a; margin-top: 8px; margin-bottom: 12px;"></div>
                
                <!-- কাস্টমার এবং বিল বিবরণী (ফাঁকা জায়গা বাড়ানো হয়েছে) -->
                <table style="width: 100%; font-size: 11px; margin-bottom: 12px; line-height: 1.4;">
                    <tr>
                        <td style="width: 55%; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 7px; font-weight: bold; font-size: 9.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">Bill To</span>
                            <div style="margin-top: 4px;"><b>Name:</b> {cust_name}</div>
                            <div style="margin-top: 2px;"><b>Address:</b> {cust_address}</div>
                        </td>
                        <td style="width: 45%; text-align: right; vertical-align: top;">
                            <span style="background-color: #1e3a8a; color: white; padding: 3px 12px; font-weight: bold; font-size: 10.5px; letter-spacing: 0.5px; border-radius: 2px; display: inline-block; margin-bottom: 4px;">INVOICE</span>
                            <div style="margin-top: 4px;"><b>Invoice No:</b> # {inv_num}</div>
                            <div style="margin-top: 2px;"><b>Date:</b> {current_date}</div>
                        </td>
                    </tr>
                </table>
                
                <!-- মেইন প্রোডাক্ট টেবিল (কলামগুলো আগের চেয়ে বড় ও রো-গুলো বেশি ফাঁকা) -->
                <table style="width: 100%; border-collapse: collapse; font-size: 11px; border: 1px solid #1e3a8a;">
                    <thead>
                        <tr style="background-color: #1e3a8a; color: white; text-align: center; font-weight: bold; font-size: 10px;">
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 8%;">S.L</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 6px; width: 52%;">DESCRIPTION</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 10%;">QTY</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 14%;">U.PRICE</th>
                            <th style="border: 1px solid #1e3a8a; padding: 6px 4px; width: 16%;">AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- রো ১ (ভেতরের ফাঁকা বা প্যাডিং বাড়ানো হয়েছে) -->
                        <tr style="text-align: center; height: 26px;">
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">1</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px 6px; text-align: left;">{item_desc}</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">1</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px;">{total_bill}/-</td>
                            <td style="border: 1px solid #1e3a8a; padding: 4px; font-weight: bold;">{total_bill}/-</td>
                        </tr>
                        <!-- বাকি ৯টি খালি রো (মোট ১০টা রো ফাঁকা ফাঁকা রাখার জন্য height ২৪px করা হয়েছে) -->
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">2</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">3</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">4</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">5</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">6</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">7</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">8</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">9</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        <tr style="height: 24px;"><td style="border: 1px solid #1e3a8a; padding: 4px;">10</td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td><td style="border: 1px solid #1e3a8a;"></td></tr>
                        
                        <!-- সাব টোটাল অংশ -->
                        <tr>
                            <td colspan="3" style="border: 1px solid #1e3a8a;"></td>
                            <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #1e3a8a; color: white; font-size: 10px;">SUB TOTAL</td>
                            <td style="border: 1px solid #1e3a8a; padding: 6px; text-align: center; font-weight: bold; background-color: #f3f4f6; font-size: 11px;">{total_bill} BDT</td>
                        </tr>
                    </tbody>
                </table>
                
                <!--底部: পেমেন্ট মেথড ও সিগনেচার -->
                <table style="width: 100%; position: absolute; bottom: 18px; left: 18px; width: calc(100% - 36px); font-size: 10px;">
                    <tr>
                        <td style="width: 50%; vertical-align: bottom;">
                            <div style="border: 1px solid #1e3a8a; display: inline-block; border-radius: 2px; background-color: white;">
                                <div style="background-color: #1e3a8a; color: white; padding: 2px 6px; font-weight: bold; font-size: 8.5px;">Payment Methods</div>
                                <div style="padding: 3px 6px; font-weight: bold; color: #222; font-size: 9.5px;">Cash | Bkash | Nagad | Bank</div>
                            </div>
                        </td>
                        <td style="width: 50%; text-align: right; vertical-align: bottom;">
                            <div style="display: inline-block; text-align: center; width: 150px;">
                                <div style="border-top: 1px solid #000; margin-bottom: 3px;"></div>
                                <b>Authorised Signature</b><br>
                                <span style="font-size: 8.5px; color: #444;">SM-TECH Computer & IT Solutions</span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            """
            
            # অ্যাপ স্ক্রিনে দেখানো
            st.markdown(invoice_html, unsafe_allow_html=True)
            st.write("")
            
            # 📥 ৫×৭ সাইজ অনুযায়ী নিখুঁত পিডিএফ ডাউনলোড/প্রিন্ট বাতন
            st.components.v1.html(f"""
                <script>
                function printInvoice() {{
                    var WinPrint = window.open('', '', 'width=600,height=800');
                    WinPrint.document.write('<html><head><title>Print Invoice</title>');
                    WinPrint.document.write('<style>@page {{ size: 5in 7in; margin: 0; }} body {{ margin: 0; }}</style></head><body>');
                    WinPrint.document.write(`{invoice_html}`);
                    WinPrint.document.write('</body></html>');
                    WinPrint.document.close();
                    WinPrint.focus();
                    setTimeout(function() {{ WinPrint.print(); }}, 500);
                }}
                </script>
                <div style="text-align: center; margin-top: 5px;">
                    <button onclick="printInvoice()" style="background-color: #059669; color: white; padding: 10px 25px; font-size: 14px; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                        📥 Download 5"x7" PDF / Print Invoice
                    </button>
                </div>
            """, height=65)
