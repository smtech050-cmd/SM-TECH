import tkinter as tk
from tkinter import ttk

# মূল উইন্ডো সেটআপ
root = tk.Tk()
root.title("SM-TECH POS v2.0")
root.geometry("1000x600")
root.configure(bg="#F0F2F5") # হালকা ব্যাকগ্রাউন্ড (বাম পাশের সাইডবারের জন্য)

# --- বাম পাশের সাইডবার (Sidebar) ---
sidebar = tk.Frame(root, bg="#F0F2F5", width=280)
sidebar.pack(side="left", fill="y", padx=10, pady=10)
sidebar.pack_propagate(False)

# সাইডবার টাইটেল
title_label = tk.Label(sidebar, text="💻 SM-TECH POS v2.0", font=("Arial", 14, "bold"), bg="#F0F2F5", fg="#1E293B")
title_label.pack(anchor="w", pady=(10, 20), padx=10)

# মেনু বাটনের তালিকা (আপনার স্ক্রিনশট অনুযায়ী)
menus = [
    ("🏠 ড্যাশবোর্ড", True), # এটিকে সিলেক্টেড বা অ্যাক্টিভ হিসেবে দেখানোর জন্য
    ("📦 স্টক ম্যানেজমেন্ট", False),
    ("🔍 পণ্য সার্চ", False),
    ("🧾 ব্ল্যাঙ্ক ইনভয়েস প্রিন্ট", False),
    ("👤 কাস্টমার ম্যানেজমেন্ট", False),
    ("📊 বিক্রয় রিপোর্ট", False),
    ("💰 লাভ-লোকসানের হিসাব", False)
]

for text, is_active in menus:
    # অ্যাক্টিভ মেনুর জন্য একটু আলাদা স্টাইল বা ব্যাকগ্রাউন্ড দেওয়া যেতে পারে
    btn_bg = "#FFFFFF"
    btn = tk.Button(sidebar, text=text, font=("Arial", 11), bg=btn_bg, fg="#1E293B",
                    bd=0, relief="flat", height=2, anchor="w", padx=20)
    btn.pack(fill="x", pady=5)

# লগআউট বাটন (নিচের দিকে)
logout_btn = tk.Button(sidebar, text="🔓 লগআউট", font=("Arial", 11), bg="#FFFFFF", fg="#1E293B",
                       bd=0, relief="flat", height=2, anchor="w", padx=20)
logout_btn.pack(side="bottom", fill="x", pady=20)


# --- ডান পাশের ড্যাশবোর্ড এরিয়া (Dashboard Area) ---
# স্ক্রিনশটের ডান পাশের মতো ডার্ক ব্লু/নেভি ব্লু ব্যাকগ্রাউন্ড
dashboard_frame = tk.Frame(root, bg="#0A192F") 
dashboard_frame.pack(side="right", fill="both", expand=True)

# ড্যাশবোর্ড টাইটেল বা হেডার
header_label = tk.Label(dashboard_frame, text="ড্যাশবোর্ড ওভারভিউ", font=("Arial", 18, "bold"), bg="#0A192F", fg="#FFFFFF")
header_label.pack(anchor="w", padx=30, pady=20)

# কন্টেইনার ফ্রেম (কার্ডগুলো সাজানোর জন্য)
cards_container = tk.Frame(dashboard_frame, bg="#0A192F")
cards_container.pack(fill="both", expand=True, padx=20, pady=10)


# --- স্টাইলিশ কার্ড তৈরির ফাংশন ---
def create_card(parent, title, value, icon, border_color):
    # কার্ডের মূল ফ্রেম (ডার্ক ব্যাকগ্রাউন্ডের ওপর কিছুটা উজ্জ্বল কালার)
    card = tk.Frame(parent, bg="#112240", highlightbackground=border_color, highlightthickness=2, bd=0)
    card.pack(side="left", padx=15, pady=15, width=220, height=180)
    card.pack_propagate(False)
    
    # আইকন এবং টাইটেল
    icon_label = tk.Label(card, text=icon, font=("Arial", 24), bg="#112240")
    icon_label.pack(anchor="nw", padx=15, pady=(15, 5))
    
    title_label = tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="#112240", fg="#FFFFFF", justify="left")
    title_label.pack(anchor="nw", padx=15)
    
    # টাকা বা মান (বড় ও স্পষ্ট করে)
    value_label = tk.Label(card, text=value, font=("Arial", 22, "bold"), bg="#112240", fg="#FFFFFF")
    value_label.pack(anchor="sw", padx=15, pady=(20, 15))

# --- কার্ডসমূহ যোগ করা ---
# ১. মোট বিক্রয় কার্ড (আপনার স্ক্রিনশটের ডিজাইনের মতো সায়ান/ব্লু বর্ডার)
create_card(cards_container, "মোট\nবিক্রয়", "৳ 0.00", "💰", "#00BCD4")

# উদাহরণ হিসেবে আরও দুটি কার্ড যুক্ত করা হলো:
create_card(cards_container, "মোট\nক্রয়", "৳ 0.00", "🛒", "#FF9800")
create_card(cards_container, "মোট\nলাভ", "৳ 0.00", "📈", "#4CAF50")

root.mainloop()
