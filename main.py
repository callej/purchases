import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        self.create_tables()

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(column=0, row=0, padx=10, pady=10)

        self.people_tab = ttk.Frame(self.notebook)
        self.items_tab = ttk.Frame(self.notebook)
        self.purchases_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.people_tab, text="People")
        self.notebook.add(self.items_tab, text="Items")
        self.notebook.add(self.purchases_tab, text="Purchases")
        self.notebook.add(self.report_tab, text="Report")

        self.create_people_tab()
        self.create_items_tab()
        self.create_purchases_tab()
        self.create_report_tab()

    def create_tables(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,
            person_id INTEGER NOT NULL,
            FOREIGN KEY (person_id) REFERENCES people (id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY,
            purchase_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id),
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
        """)

        conn.commit()
        conn.close()

    # People Tab
    def create_people_tab(self):
        # Labels
        ttk.Label(self.people_tab, text="Name:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.people_tab, text="Email:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.people_tab, text="Phone:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        # Entry widgets
        self.name_entry = ttk.Entry(self.people_tab)
        self.email_entry = ttk.Entry(self.people_tab)
        self.phone_entry = ttk.Entry(self.people_tab)

        self.name_entry.grid(column=1, row=0, padx=5, pady=5)
        self.email_entry.grid(column=1, row=1, padx=5, pady=5)
        self.phone_entry.grid(column=1, row=2, padx=5, pady=5)

        # Add button
        ttk.Button(self.people_tab, text="Add Person", command=self.add_person).grid(column=1, row=3, padx=5, pady=5)

    def add_person(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if not name or not email or not phone:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO people (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Person added successfully")
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    # Items Tab
    def create_items_tab(self):
        # Labels
        ttk.Label(self.items_tab, text="Item Name:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.items_tab, text="Price:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        # Entry widgets
        self.item_name_entry = ttk.Entry(self.items_tab)
        self.price_entry = ttk.Entry(self.items_tab)

        self.item_name_entry.grid(column=1, row=0, padx=5, pady=5)
        self.price_entry.grid(column=1, row=1, padx=5, pady=5)

        # Add button
        ttk.Button(self.items_tab, text="Add Item", command=self.add_item).grid(column=1, row=2, padx=5, pady=5)

    def add_item(self):
        item_name = self.item_name_entry.get()
        price = self.price_entry.get()

        if not item_name or not price:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO items (item_name, price) VALUES (?, ?)", (item_name, price))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item added successfully")
        self.item_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    # Purchases Tab
    def create_purchases_tab(self):
        # Labels
        ttk.Label(self.purchases_tab, text="Person:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.purchases_tab, text="Item:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.purchases_tab, text="Quantity:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        # Combobox widgets
        self.person_combobox = ttk.Combobox(self.purchases_tab, postcommand=self.update_people_combobox, state="readonly")
        self.item_combobox = ttk.Combobox(self.purchases_tab, postcommand=self.update_items_combobox, state="readonly")
        self.person_combobox.grid(column=1, row=0, padx=5, pady=5)
        self.item_combobox.grid(column=1, row=1, padx=5, pady=5)

        # Entry widgets
        self.quantity_entry = ttk.Entry(self.purchases_tab)
        self.quantity_entry.grid(column=1, row=2, padx=5, pady=5)

        # Add button
        ttk.Button(self.purchases_tab, text="Add Purchase", command=self.add_purchase).grid(column=1, row=3, padx=5, pady=5)

    def update_people_combobox(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM people")
        people = cursor.fetchall()
        conn.close()

        self.person_combobox["values"] = [f"{person[0]} - {person[1]}" for person in people]

    def update_items_combobox(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, item_name FROM items")
        items = cursor.fetchall()
        conn.close()

        self.item_combobox["values"] = [f"{item[0]} - {item[1]}" for item in items]

    def add_purchase(self):
        person = self.person_combobox.get()
        item = self.item_combobox.get()
        quantity = self.quantity_entry.get()

        if not person or not item or not quantity:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return

        person_id = int(person.split(" ")[0])
        item_id = int(item.split(" ")[0])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO purchases (person_id) VALUES (?)", (person_id,))
        purchase_id = cursor.lastrowid
        cursor.execute("INSERT INTO purchase_items (purchase_id, item_id, quantity) VALUES (?, ?, ?)", (purchase_id, item_id, quantity))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Purchase added successfully")
        self.person_combobox.set("")
        self.item_combobox.set("")
        self.quantity_entry.delete(0, tk.END)

    # Report Tab
    def create_report_tab(self):
        self.report_text = tk.Text(self.report_tab, wrap=tk.WORD, state="disabled", width=80, height=20)
        self.report_text.grid(column=0, row=0, padx=5, pady=5)

        ttk.Button(self.report_tab, text="Generate Report", command=self.generate_report).grid(column=0, row=1, padx=5, pady=5)

    def generate_report(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT p.id, pe.name, i.item_name, pi.quantity, i.price
        FROM purchases p
        JOIN people pe ON p.person_id = pe.id
        JOIN purchase_items pi ON p.id = pi.purchase_id
        JOIN items i ON pi.item_id = i.id
        """)
        purchases = cursor.fetchall()

        report = "Purchases:\n\n"

        total_cost = 0
        for purchase in purchases:
            cost = purchase[3] * purchase[4]
            report += f"{purchase[1]} bought {purchase[3]} x {purchase[2]} for ${cost:.2f}\n"
            total_cost += cost

        report += f"\nTotal Cost: ${total_cost:.2f}"

        conn.close()

        self.report_text.configure(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)
        self.report_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()





