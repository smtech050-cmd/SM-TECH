-- ১. ইউজার বা অ্যাডমিন টেবিল
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- ডিফল্ট অ্যাডমিন ইউজার তৈরি (Username: admin, Password: admin123)
INSERT IGNORE INTO admins (username, password) VALUES ('admin', 'admin123');

-- ২. স্টক বা ইনভেন্টরি টেবিল
CREATE TABLE IF NOT EXISTS stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_added VARCHAR(20) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    sell_rate DECIMAL(10, 2) NOT NULL
);

-- ৩. কাস্টমার টেবিল
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

-- ৪. বিক্রয় ও ইনভয়েস টেবিল
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no VARCHAR(100) NOT NULL UNIQUE,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    sale_date VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    profit DECIMAL(10, 2) NOT NULL
);
