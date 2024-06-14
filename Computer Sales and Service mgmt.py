import tkinter as tk #lib
from tkinter import messagebox #module
from tkinter import ttk #module
import mysql.connector as sql #module from lib
from turtle import RawTurtle, TurtleScreen #module

#connect to the database
def connect_to_db():
    try:
        conn = sql.connect(
            host="localhost",
            user="root",
            passwd="Guru@2004",
            database="sales"
        )
        if conn.is_connected():
            messagebox.showinfo("Success", "Successfully connected to the database.")
        return conn
    except sql.Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        return None

#Application Class
class App:
    def __init__(self, root):
        self.root = root
        self.conn = connect_to_db()
        self.c1 = self.conn.cursor() if self.conn else None
        self.root.geometry("600x600")
        self.style = ttk.Style()
        self.configure_styles()
        self.draw_turtle_image()

    def configure_styles(self):
        #Configuring styles for dark theme
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TButton", background="#3A3A3A", foreground="#FFFFFF")
        self.style.map("TButton",
                       background=[("active", "#2A2A2A")],  # Button color hover darken
                       foreground=[("active", "#FFFFFF")])
        self.style.configure("TEntry", fieldbackground="#3A3A3A", foreground="#FFFFFF")
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("Treeview", background="#2E2E2E", foreground="#FFFFFF", fieldbackground="#2E2E2E")
        self.style.configure("Treeview.Heading", background="#3A3A3A", foreground="#FFFFFF")

    def draw_turtle_image(self):
        #Create a canvas for Turtle graphics
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(pady=20,padx=20)

        screen = TurtleScreen(self.canvas)
        screen.bgcolor("#2E2E2E")

        pen = RawTurtle(screen)
        pen.color("white")
        pen.speed(10)

        #image generation
        for i in range(18):
            pen.forward(100)
            pen.right(170)

        pen.hideturtle()

        #Wait for a while then clear the Turtle canvas and show the main window
        self.root.after(500, self.clear_turtle_and_show_main)

    def clear_turtle_and_show_main(self):
        self.canvas.pack_forget()  #Hide the canvas
        self.create_main_window()

        #main window generation
    def create_main_window(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Computer Sales and Service System", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(main_frame, text="Buy Computer Parts", command=self.buy_computer_parts).pack(pady=5)
        ttk.Button(main_frame, text="Ask for Computer Service", command=self.ask_computer_service).pack(pady=5)
        ttk.Button(main_frame, text="Report a Problem", command=self.report_problem).pack(pady=5)
        ttk.Button(main_frame, text="View Comments and Ratings", command=self.view_comments_ratings).pack(pady=5)
        ttk.Button(main_frame, text="View Computer Sales", command=self.view_comp_sales).pack(pady=5)
        ttk.Button(main_frame, text="View Computer Service", command=self.view_comp_service).pack(pady=5)
        ttk.Button(main_frame, text="Exit", command=self.root.destroy).pack(pady=5)

        #sales window
    def buy_computer_parts(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Buy Computer Parts")
        new_window.configure(bg="#2E2E2E")
        self.create_form_sale(new_window, self.submit_computer_parts)
    #sales DB insertion
    def submit_computer_parts(self, data, window):
        cust_name, phno, email, address, part, rating, comment = data

        try:
            insert = f"INSERT INTO 1_comp_sales VALUES('{cust_name}', {phno}, '{email}', '{address}', '{part}')"
            self.c1.execute(insert)
            self.conn.commit()

            insert1 = f"INSERT INTO rating_comment VALUES('{cust_name}', {phno}, '{email}', '{address}', {rating}, '{comment}')"
            self.c1.execute(insert1)
            self.conn.commit()

            if int(rating) < 5:
                messagebox.showinfo("Rating", "Sorry for our poor performance. Next time we will be good enough.")
            else:
                messagebox.showinfo("Rating", "Thanks for rating us. Next time we will be even better.")

            messagebox.showinfo("Thank You", f"Thank you, {cust_name}. Your computer part will be delivered shortly and you can pay cash to the delivery boy.")
            window.destroy()
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #service window
    def ask_computer_service(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Ask for Computer Service")
        new_window.configure(bg="#2E2E2E")
        self.create_form_service(new_window, self.submit_computer_service)
    #service submission
    def submit_computer_service(self, data, window):
        name, phno, email, address, service, rating, comment = data

        try:
            insert = f"INSERT INTO 1_comp_service VALUES('{name}', {phno}, '{email}', '{address}', '{service}')"
            self.c1.execute(insert)
            self.conn.commit()

            insert1 = f"INSERT INTO rating_comment VALUES({phno}, '{address}', '{email}', {rating}, '{comment}')"
            self.c1.execute(insert1)
            self.conn.commit()

            if int(rating) < 5:
                messagebox.showinfo("Rating", "Sorry for our poor performance. Next time we will be good enough.")
            else:
                messagebox.showinfo("Rating", "Thanks for rating us. Next time we will be even better.")

            messagebox.showinfo("Thank You", f"Thank you, {name}. The service you asked will be done shortly.")
            window.destroy()
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #proble window
    def report_problem(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Report a Problem")
        new_window.configure(bg="#2E2E2E")
        self.create_problem_form(new_window, self.submit_problem)
    #problem Submissin
    def submit_problem(self, data, window):
        cus_name, phno1, typ_prob, del_nam, prob = data

        try:
            insert = f"INSERT INTO prob VALUES('{cus_name}', {phno1}, '{del_nam}', '{typ_prob}', '{prob}')"
            self.c1.execute(insert)
            self.conn.commit()
            messagebox.showinfo("Thank You", "Sorry for the problem. We will ensure this does not happen next time. Thank you.")
            window.destroy()
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #view comments table
    def view_comments_ratings(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Comments and Ratings")
        new_window.configure(bg="#2E2E2E")

        # Define columns
        columns = ("Phone", "Address", "Email",  "Rating", "Comment")
        tree = ttk.Treeview(new_window, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=150, stretch=tk.NO)

        try:
            self.c1.execute("SELECT * FROM rating_comment")
            rows = self.c1.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #view sales table
    def view_comp_sales(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Computer Sales")
        new_window.configure(bg="#2E2E2E")

        columns = ("Customer Name", "Phone", "Email", "Address", "Part")
        tree = ttk.Treeview(new_window, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=150, stretch=tk.NO)

        try:
            self.c1.execute("SELECT * FROM 1_comp_sales")
            rows = self.c1.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #view Sevice table
    def view_comp_service(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Computer Service")
        new_window.configure(bg="#2E2E2E")

        columns = ("Name", "Phone", "Email", "Address", "Service")
        tree = ttk.Treeview(new_window, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=150, stretch=tk.NO)

        try:
            self.c1.execute("SELECT * FROM 1_comp_service")
            rows = self.c1.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
        except sql.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    #service input form
    def create_form_service(self, window, submit_callback):
        frame = ttk.Frame(window)
        frame.pack(padx=20, pady=20)

        labels = ["Name:", "Phone Number:", "Email:", "Address:", "Type of Service:", "Rating:", "Comment:"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries.append(entry)

        ttk.Button(frame, text="Submit", command=lambda: submit_callback([entry.get() for entry in entries], window)).grid(row=len(labels), columnspan=2, pady=10)
    #sales input form
    def create_form_sale(self, window, submit_callback):
        frame = ttk.Frame(window)
        frame.pack(padx=20, pady=20)

        labels = ["Name:", "Phone Number:", "Email:", "Address:", "Part:", "Rating:", "Comment:"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries.append(entry)

        ttk.Button(frame, text="Submit", command=lambda: submit_callback([entry.get() for entry in entries], window)).grid(row=len(labels), columnspan=2, pady=10)
    #problem input form
    def create_problem_form(self, window, submit_callback):
        frame = ttk.Frame(window)
        frame.pack(padx=20, pady=20)

        labels = ["Name", "Phone Number", "Service Problem", "Sales Person Name", "Problem Description"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries.append(entry)

        ttk.Button(frame, text="Submit", command=lambda: submit_callback([entry.get() for entry in entries], window)).grid(row=len(labels), columnspan=2, pady=10)

# Main window setup
root = tk.Tk()
app = App(root)
root.mainloop()
