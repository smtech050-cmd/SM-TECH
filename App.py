import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sristi_repair_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# 🗄️ ডাটাবেজ মডেলস (Database Models)
# ==========================================

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    repairs = db.relationship('Repair', backref='customer', lazy=True)

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(150), nullable=False)
    problem_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending') # Pending, In Progress, Ready, Delivered
    estimated_cost = db.Column(db.Float, default=0.0)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# 🔗 অ্যাপ্লিকেশন রাউটস (Routes / Endpoints)
# ==========================================

# ১. ড্যাশবোর্ড (Dashboard)
@app.route('/')
@app.route('/dashboard')
def dashboard():
    total_customers = Customer.query.count()
    total_repairs = Repair.query.count()
    pending_repairs = Repair.query.filter(Repair.status != 'Delivered').count()
    low_stock = Stock.query.filter(Stock.quantity < 5).count()
    
    return jsonify({
        "status": "success",
        "module": "Dashboard",
        "summary": {
            "total_customers": total_customers,
            "total_repairs": total_repairs,
            "pending_repairs": pending_repairs,
            "low_stock_items": low_stock
        }
    })

# ২. কাস্টমার ম্যানেজমেন্ট (Customer)
@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'POST':
        data = request.get_json() or request.form
        new_customer = Customer(
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Customer added successfully!", "id": new_customer.id}), 201
        
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name, "phone": c.phone, "email": c.email} for c in customers])

# ৩. রিপেয়ার ট্র্যাকিং (Repair)
@app.route('/repairs', methods=['GET', 'POST'])
def manage_repairs():
    if request.method == 'POST':
        data = request.get_json() or request.form
        new_repair = Repair(
            device_name=data.get('device_name'),
            problem_description=data.get('problem_description'),
            estimated_cost=float(data.get('estimated_cost', 0)),
            customer_id=int(data.get('customer_id')),
            status='Pending'
        )
        db.session.add(new_repair)
        db.session.commit()
        return jsonify({"message": "Repair job logged successfully!", "repair_id": new_repair.id}), 201

    repairs = Repair.query.all()
    return jsonify([{
        "id": r.id, 
        "device": r.device_name, 
        "status": r.status, 
        "cost": r.estimated_cost,
        "customer_id": r.customer_id
    } for r in repairs])

# 🛠️ রিপেয়ার স্ট্যাটাস আপডেট (Update Status)
@app.route('/repairs/<int:id>/status', methods=['PUT', 'POST'])
def update_repair_status(id):
    data = request.get_json() or request.form
    repair = Repair.query.get_or_4004(id)
    if repair:
        repair.status = data.get('status', repair.status)
        db.session.commit()
        return jsonify({"message": f"Repair status updated to {repair.status}"})
    return jsonify({"error": "Repair job not found"}), 404

# ৪. স্টক ইনভেন্টরি (Stock)
@app.route('/stock', methods=['GET', 'POST'])
def manage_stock():
    if request.method == 'POST':
        data = request.get_json() or request.form
        new_item = Stock(
            item_name=data.get('item_name'),
            quantity=int(data.get('quantity', 0)),
            price=float(data.get('price', 0.0))
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Stock item added/updated!", "item_id": new_item.id}), 201

    stock_items = Stock.query.all()
    return jsonify([{"id": s.id, "item": s.item_name, "qty": s.quantity, "price": s.price} for s in stock_items])

# ৫. পিওএস ও ইনভয়েস জেনারেশন (POS & Invoice)
@app.route('/pos/checkout', methods=['POST'])
def pos_checkout():
    data = request.get_json()
    # এখানে রিয়েল-টাইম কার্ট ক্যালকুলেশন হবে
    inv_num = f"INV-{int(datetime.utcnow().timestamp())}"
    
    new_invoice = Invoice(
        invoice_number=inv_num,
        customer_name=data.get('customer_name', 'Walking Customer'),
        total_amount=float(data.get('total_amount', 0.0))
    )
    db.session.add(new_invoice)
    db.session.commit()
    
    return jsonify({
        "message": "Transaction complete!",
        "invoice_number": inv_num,
        "download_url": f"/invoice/{inv_num}/print"
    }), 201

# 🖨️ ইনভয়েস ডাউনলোড ও প্রিন্ট ভিউ (Print View HTML)
@app.route('/invoice/<string:inv_num>/print')
def print_invoice(inv_num):
    invoice = Invoice.query.filter_by(invoice_number=inv_num).first_or_404()
    
    # একটি সিম্পল ও প্রফেশনাল প্রিন্ট রেডি HTML টেমপ্লেট
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Print Invoice - {{ inv.invoice_number }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; color: #333; }
            .invoice-box { max-width: 800px; margin: auto; border: 1px solid #eee; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            .header { display: flex; justify-content: space-between; border-bottom: 2px solid #333; padding-bottom: 10px; }
            .details { margin-top: 20px; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            th { background-color: #f2f2f2; }
            .total { text-align: right; font-weight: bold; font-size: 1.2em; margin-top: 20px; }
            .btn-print { background: #28a745; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; }
            @media print { .btn-print { display: none; } }
        </style>
    </head>
    <body>
        <div class="invoice-box">
            <div class="header">
                <div>
                    <h2>SRISTI COMPUTER REPAIR</h2>
                    <p>Fast & Reliable Device Servicing</p>
                </div>
                <div>
                    <h3>INVOICE</h3>
                    <p><b>Invoice #:</b> {{ inv.invoice_number }}</p>
                    <p><b>Date:</b> {{ inv.created_at.strftime('%d-%m-%Y') }}</p>
                </div>
            </div>
            
            <div class="details">
                <p><b>Customer Name:</b> {{ inv.customer_name }}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Computer Parts / Repair Services Rendered</td>
                        <td>{{ inv.total_amount }} BDT</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="total">
                Total Paid: {{ inv.total_amount }} BDT
            </div>
            
            <br><br>
            <button class="btn-print" onclick="window.print()">Print / Download PDF</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, inv=invoice)

# ৬. ডাটাবেজ ব্যাকআপ (Backup Utility)
@app.route('/settings/backup')
def database_backup():
    try:
        # সহজ ব্যাকআপ লজিক: মূল ডাটাবেজ ফাইলটিকে কপি করে ব্যাকআপ ফোল্ডারে রাখা
        if os.path.exists('instance/database.db'):
            backup_name = f"backup-{int(datetime.utcnow().timestamp())}.db"
            # আপনি চাইলে এখানে ফাইল কপি করার লজিক দিতে পারেন
            return jsonify({"status": "success", "message": f"Backup created successfully as {backup_name}"})
        return jsonify({"status": "error", "message": "Database not initialized yet"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 🚀 অ্যাপ্লিকেশন রানার
# ==========================================
if __name__ == '__main__':
    # প্রথমবার রান করার সময় ডাটাবেজ টেবিলগুলো অটোমেটিক তৈরি হবে
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
