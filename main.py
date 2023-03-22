import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class App:
    def __init__(self, root1):
        self.root = root1
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
            item_id INTEGER NOT NULL,
            FOREIGN KEY (person_id) REFERENCES people (id),
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

        cursor.execute("INSERT INTO people (name, email, phone) VALUES (?, ?, ?)", (name        , email, phone))
        conn.commit()
        conn.close()

        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Person added successfully")

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
            messagebox.showerror("Error", "Invalid price value")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO items (item_name, price) VALUES (?, ?)", (item_name, price))
        conn.commit()
        conn.close()

        self.item_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Item added successfully")

    # Purchases Tab
    def create_purchases_tab(self):
        # Labels
        ttk.Label(self.purchases_tab, text="Person:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.purchases_tab, text="Item:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        # Dropdowns
        self.person_var = tk.StringVar()
        self.item_var = tk.StringVar()

        self.person_dropdown = ttk.Combobox(self.purchases_tab, textvariable=self.person_var, postcommand=self.update_people_dropdown)
        self.item_dropdown = ttk.Combobox(self.purchases_tab, textvariable=self.item_var, postcommand=self.update_items_dropdown)

        self.person_dropdown.grid(column=1, row=0, padx=5, pady=5)
        self.item_dropdown.grid(column=1, row=1, padx=5, pady=5)

        # Add button
        ttk.Button(self.purchases_tab, text="Add Purchase", command=self.add_purchase).grid(column=1, row=2, padx=5, pady=5)

    def update_people_dropdown(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM people")
        people = [person[0] for person in cursor.fetchall()]

        conn.close()

        self.person_dropdown["values"] = people

    def update_items_dropdown(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT item_name FROM items")
        items = [item[0] for item in cursor.fetchall()]

        conn.close()

        self.item_dropdown["values"] = items

    def add_purchase(self):
        person_name = self.person_var.get()
        item_name = self.item_var.get()

        if not person_name or not item_name:
            messagebox.showerror("Error", "Please select a person and an item")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM people WHERE name = ?", (person_name,))
        person_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM items WHERE item_name = ?", (item_name,))
        item_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO purchases (person_id, item_id) VALUES (?, ?)", (person_id, item_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Purchase added successfully")

        # Report Tab

    def create_report_tab(self):
        self.report_text = tk.Text(self.report_tab, wrap=tk.WORD, width=80, height=20)
        self.report_text.grid(column=0, row=0, padx=5, pady=5)

        ttk.Button(self.report_tab, text="Show Report", command=self.show_report).grid(column=0, row=1, padx=5, pady=5)

    def show_report(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
                SELECT people.name, items.item_name, items.price
                FROM purchases
                INNER JOIN people ON purchases.person_id = people.id
                INNER JOIN items ON purchases.item_id = items.id
                """)
        purchases = cursor.fetchall()

        conn.close()

        self.report_text.delete(1.0, tk.END)
        total_cost = 0

        for name, item_name, price in purchases:
            self.report_text.insert(tk.END, f"{name} bought {item_name} for ${price:.2f}\n")
            total_cost += price

        self.report_text.insert(tk.END, f"\nTotal cost of all purchases: ${total_cost:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


