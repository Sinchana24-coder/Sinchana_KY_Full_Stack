import tkinter as tk
from tkinter import messagebox, PhotoImage
import sqlite3
import random
from PIL import Image, ImageTk  # Importing Image and ImageTk from Pillow


# Database setup
def setup_database():
    conn = sqlite3.connect("saloon_ticketing.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        Name TEXT,
                        TicketID TEXT,
                        Services TEXT,
                        TotalAmount INTEGER
                    )''')
    conn.commit()
    conn.close()

# Add ticket to database
def add_to_database(name, ticket_id, services, total_amount):
    conn = sqlite3.connect("saloon_ticketing.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (Name, TicketID, Services, TotalAmount) VALUES (?, ?, ?, ?)",
                   (name, ticket_id, services, total_amount))
    conn.commit()
    conn.close()

# Login validation
def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password123":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Generate ticket
def generate_ticket():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Input Error", "Please enter the customer's name.")
        return

    selected_services = []
    total_amount = 0

    if haircut_var.get():
        selected_services.append("Hair Cut (₹300)")
        total_amount += 300
    if spa_var.get():
        selected_services.append("Spa (₹500)")
        total_amount += 500
    if facial_var.get():
        selected_services.append("Facial (₹350)")
        total_amount += 350

    if not selected_services:
        messagebox.showerror("Input Error", "Please select at least one service.")
        return

    ticket_id = f"T{random.randint(1000, 9999)}"
    service_list = ", ".join(selected_services)

    # Add to database
    add_to_database(name, ticket_id, service_list, total_amount)

    # Show ticket
    messagebox.showinfo("Ticket Generated",
                        f"Ticket ID: {ticket_id}\n"
                        f"Name: {name}\n"
                        f"Services: {service_list}\n"
                        f"Total Amount: ₹{total_amount}")

# Main Window
def open_main_window():
    global name_entry, haircut_var, spa_var, facial_var

    main_window = tk.Tk()
    main_window.title("Saloon Ticketing System")
    main_window.geometry("600x500")
    main_window.configure(bg="#f9f4f1")

    # Header
    tk.Label(main_window, text="Saloon Ticketing System", font=("Arial", 20, "bold"), bg="#f9f4f1", fg="#6e4b3e").pack(pady=10)

    # Customer name
    tk.Label(main_window, text="Customer Name:", font=("Arial", 14), bg="#f9f4f1", fg="#6e4b3e").pack(pady=10)
    name_entry = tk.Entry(main_window, font=("Arial", 14))
    name_entry.pack(pady=5)

    # Service selection
    tk.Label(main_window, text="Select Services:", font=("Arial", 14), bg="#f9f4f1", fg="#6e4b3e").pack(pady=10)

    haircut_var = tk.BooleanVar()
    spa_var = tk.BooleanVar()
    facial_var = tk.BooleanVar()

    # Use Pillow to open the images
    haircut_img = Image.open("haircut.jpg")  # Open the image with Pillow
    haircut_img = ImageTk.PhotoImage(haircut_img.resize((80, 80)))  # Resize the image and convert to Tkinter-compatible format
    spa_img = Image.open("spa.jpg")  # Same for spa image
    spa_img = ImageTk.PhotoImage(spa_img.resize((80, 80)))
    facial_img = Image.open("facial.jpg")  # Same for facial image
    facial_img = ImageTk.PhotoImage(facial_img.resize((80, 80)))


    #haircut_img = PhotoImage(file="haircut.jpg").subsample(5, 5)
    #spa_img = PhotoImage(file="spa.jpg").subsample(5, 5)
    #facial_img = PhotoImage(file="facial.jpg").subsample(5, 5)

    tk.Checkbutton(main_window, text="Hair Cut (₹300)", variable=haircut_var, font=("Arial", 12), bg="#f9f4f1", fg="#6e4b3e", image=haircut_img, compound="left").pack(pady=5)
    tk.Checkbutton(main_window, text="Spa (₹500)", variable=spa_var, font=("Arial", 12), bg="#f9f4f1", fg="#6e4b3e", image=spa_img, compound="left").pack(pady=5)
    tk.Checkbutton(main_window, text="Facial (₹350)", variable=facial_var, font=("Arial", 12), bg="#f9f4f1", fg="#6e4b3e", image=facial_img, compound="left").pack(pady=5)

    # Generate ticket button
    tk.Button(main_window, text="Generate Ticket", command=generate_ticket, font=("Arial", 14), bg="#6e4b3e", fg="white").pack(pady=20)

    main_window.mainloop()

# Login Window
def open_login_window():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login - Saloon Ticketing System")
    login_window.geometry("600x400")
    login_window.configure(bg="#f7efe8")

    # Add a background image using Pillow
    bg_img = Image.open("saloon_bg.jpg")
    bg_img = ImageTk.PhotoImage(bg_img.resize((600, 400)))  # Resize the background to fit the window
    bg_label = tk.Label(login_window, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)

    
    # Add a background image
    #bg_img = PhotoImage(file="saloon_bg.jpg")
    #bg_label = tk.Label(login_window, image=bg_img)
    #bg_label.place(relwidth=1, relheight=1)

    # Login form
    tk.Label(login_window, text="Saloon Ticketing System", font=("Arial", 20, "bold"), bg="#f7efe8", fg="#6e4b3e").place(x=150, y=50)
    tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#f7efe8", fg="#6e4b3e").place(x=150, y=150)
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.place(x=250, y=150)

    tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#f7efe8", fg="#6e4b3e").place(x=150, y=200)
    password_entry = tk.Entry(login_window, font=("Arial", 14), show="*")
    password_entry.place(x=250, y=200)

    tk.Button(login_window, text="Login", command=validate_login, font=("Arial", 14), bg="#6e4b3e", fg="white").place(x=250, y=250)

    login_window.mainloop()

# Initialize database and start application
setup_database()
open_login_window()