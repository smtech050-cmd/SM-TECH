# HTML ইনভয়েস লেআউট
        invoice_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            @page {{
                size: A5 portrait;
                margin: 0;
            }}
            body {{
                font-family: 'Noto Sans Bengali', Arial, sans-serif;
                margin: 0;
                padding: 12px;
                background: #fff;
                color: #0d47a1;
            }}
            .invoice-box {{
                border: 2.5px solid #0d47a1;
                padding: 12px;
                border-radius: 8px;
                position: relative;
                box-sizing: border-box;
                min-height: 95vh;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2.5px solid #0d47a1;
                padding-bottom: 8px;
            }}
            .logo-section {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            /* ১. SM-TECH লোগো ও হেডার স্পেসিং ঠিক করা */
            .logo-img {{
                width: 75px;
                height: 75px;
                border-radius: 50%;
                background: #ffffff;
                object-fit: contain;
                border: 2px solid #0d47a1;
            }}
            .logo-text {{
                font-size: 36px;
                font-weight: 900;
                color: #0d47a1;
                line-height: 1;
                letter-spacing: 0.5px;
            }}
            .logo-sub {{
                font-size: 11px;
                font-weight: 800;
                color: #0d47a1;
                letter-spacing: 0.5px;
                margin-top: 3px;
            }}
            .owner-info {{
                text-align: right;
                color: #0d47a1;
            }}
            .owner-name {{
                font-size: 18px;
                font-weight: 900;
                margin-bottom: 1px;
            }}
            .owner-title {{
                font-size: 11px;
                font-weight: bold;
                margin-bottom: 3px;
            }}
            .owner-phone {{
                font-size: 12px;
                font-weight: bold;
                line-height: 1.2;
            }}
            .bill-sec {{
                margin-top: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 11.5px;
                color: #0d47a1;
            }}
            .invoice-middle-badge {{
                text-align: center;
                flex-grow: 1;
            }}
            .invoice-title {{
                background: #0d47a1;
                color: white;
                padding: 3px 14px;
                font-weight: bold;
                font-size: 13px;
                border-radius: 4px;
                display: inline-block;
                letter-spacing: 1px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 11px;
            }}
            th {{
                background-color: #0d47a1;
                color: white;
                border: 1px solid #0d47a1;
                padding: 5px;
            }}
            td {{
                border: 1px solid #0d47a1;
                padding: 4px 6px;
                height: 17px;
                color: #0d47a1;
            }}
            .footer-sec {{
                position: absolute;
                bottom: 25px;
                left: 12px;
                right: 12px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                font-size: 11px;
                color: #0d47a1;
            }}
            
            /* ২. পেমেন্ট মেথড সোজা নিচে নিচে ১, ২, ৩, ৪ সাজানো */
            .payment-methods {{
                border: 1.5px solid #0d47a1;
                padding: 6px 12px;
                font-size: 11px;
                color: #0d47a1;
                border-radius: 4px;
                background: #ffffff;
                width: 190px;
            }}
            .pay-title {{
                font-size: 10px;
                font-weight: 800;
                text-transform: uppercase;
                margin-bottom: 4px;
                border-bottom: 1px dashed #0d47a1;
                padding-bottom: 2px;
                letter-spacing: 0.5px;
            }}
            .pay-list {{
                display: flex;
                flex-direction: column;
                gap: 2px;
                font-weight: bold;
                font-size: 11px;
            }}
            .pay-item {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .pay-logo-img {{
                height: 14px;
                width: auto;
                object-fit: contain;
            }}
            .print-btn-container {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .btn-print {{
                background: #0d47a1;
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
            <button class="btn-print" onclick="triggerPrint()">{cur_inv['print_btn']}</button>
        </div>

        <div class="invoice-box">
            <div class="header">
                <div class="logo-section">
                    <img class="logo-img" src="https://raw.githubusercontent.com/smtech050-cmd/SM-TECH/main/IMG_20260717_214948.png" alt="SM-TECH Logo">
                    <div>
                        <div class="logo-text">SM-TECH</div>
                        <div class="logo-sub">COMPUTER & IT SOLUTION</div>
                        <div style="font-size: 9px; color: #0d47a1; font-weight: bold; margin-top: 1px;">Smart Technology-Trusted Service</div>
                    </div>
                </div>
                <div class="owner-info">
                    <div class="owner-name">S.m. Ibrahim</div>
                    <div class="owner-title">Owner</div>
                    <div class="owner-phone">💬 01940-556114</div>
                    <div class="owner-phone">💬 01810-499166</div>
                </div>
            </div>

            <div class="bill-sec">
                <div style="width: 38%;">
                    <b>{cur_inv['bill_to']}</b> {cust_name}<br>
                    <b>{cur_inv['address']}</b> {cust_address}
                </div>
                
                <div class="invoice-middle-badge">
                    <span class="invoice-title">{cur_inv['inv_title']}</span>
                </div>

                <div style="text-align: right; width: 32%;">
                    <b>{cur_inv['inv_no']}</b> {inv_custom_num}<br>
                    <b>{cur_inv['date']}</b> <span id="real-time-date"></span>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 8%;">{cur_inv['sl']}</th>
                        <th style="width: 48%;">{cur_inv['desc']}</th>
                        <th style="width: 10%;">{cur_inv['qty']}</th>
                        <th style="width: 17%;">{cur_inv['price']}</th>
                        <th style="width: 17%;">{cur_inv['amount']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr>
                        <td colspan="3" style="border:1px solid #0d47a1;"><b>{cur_inv['words']}</b> {amount_in_words}</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">{cur_inv['subtotal']}</td>
                        <td style="font-weight:bold; text-align:right; background:#0d47a1; color:white;">{sub_total:,}</td>
                    </tr>
                </tbody>
            </table>

            <div class="footer-sec">
                <div>
                    <!-- পেমেন্ট মেথড ১, ২, ৩, ৪ সোজা লাইনে -->
                    <div class="payment-methods">
                        <div class="pay-title">{cur_inv['pay_meth']}</div>
                        <div class="pay-list">
                            <div class="pay-item">১। 💵 Cash</div>
                            <div class="pay-item">
                                ২। <img src="https://raw.githubusercontent.com/freelogovectors/bKash-Logo-PNG/main/bKash-Logo.png" class="pay-logo-img" alt="bKash"> Bkash
                            </div>
                            <div class="pay-item">
                                ৩। <img src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" class="pay-logo-img" alt="Nagad"> Nagad
                            </div>
                            <div class="pay-item">
                                ৪। <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/AB_Bank_Logo.svg/1200px-AB_Bank_Logo.svg.png" class="pay-logo-img" alt="Bank"> Bank
                            </div>
                        </div>
                    </div>
                </div>
                <div style="text-align: center;">
                    ------------------------------------------<br>
                    <b>{cur_inv['auth_sig']}</b><br>
                    <span style="font-size: 9px;">SM-TECH Computer & IT Solutions</span>
                </div>
            </div>

            <div style="position: absolute; bottom: 5px; left: 12px; right: 12px; display: flex; justify-content: space-between; font-size: 8px; color: #0d47a1; font-weight: bold;">
                <span>Print Date: <span id="real-time-stamp"></span></span>
                <span>Website: smtech.com.bd</span>
            </div>
        </div>

        <script>
            function updateDateTime() {{
                const now = new Date();
                const day = String(now.getDate()).padStart(2, '0');
                const month = String(now.getMonth() + 1).padStart(2, '0');
                const year = now.getFullYear();
                const formattedDate = `${{day}}/${{month}}/${{year}}`;
                
                const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                const monthName = monthNames[now.getMonth()];
                let hours = now.getHours();
                const minutes = String(now.getMinutes()).padStart(2, '0');
                const ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12;
                const formattedHours = String(hours).padStart(2, '0');
                
                const formattedTimeStamp = `${{day}}-${{monthName}}-${{year}} ${{formattedHours}}:${{minutes}} ${{ampm}}`;

                document.getElementById('real-time-date').innerText = formattedDate;
                document.getElementById('real-time-stamp').innerText = formattedTimeStamp;
            }}

            updateDateTime();

            function triggerPrint() {{
                updateDateTime();
                window.print();
            }}
        </script>

        </body>
        </html>
        """
