import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
import sqlite3

class FinanceTracker:
    def __init__(self, master):
        self.master = master
        master.title("Finance Tracker")
        master.geometry("800x600")  # Increased initial window size

        # --- Database Connection ---
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # --- Styling ---
        self.font = ("Arial", 12)
        self.padx = 10
        self.pady = 5

        # --- Data ---
        self.income_categories = ["Salary", "Investment", "Other"]
        self.expense_categories = ["Food", "Rent", "Transportation", "Utilities", "Entertainment", "Other"]
        self.report_months = self.get_available_report_months()

        # --- UI Elements ---
        self.notebook = ttk.Notebook(master)
        self.income_tab = tk.Frame(self.notebook)
        self.expense_tab = tk.Frame(self.notebook)
        self.savings_tab = tk.Frame(self.notebook)
        self.report_tab = tk.Frame(self.notebook)

        self.notebook.add(self.income_tab, text="Income")
        self.notebook.add(self.expense_tab, text="Expenses")
        self.notebook.add(self.savings_tab, text="Savings")
        self.notebook.add(self.report_tab, text="Reports")
        self.notebook.pack(expand=True, fill="both", padx=self.padx, pady=self.pady)

        self.create_income_tab()
        self.create_expense_tab()
        self.create_savings_tab()
        self.create_report_tab()


    def create_tables(self):
        """Creates the necessary database tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
        self.conn.commit()

    def get_available_report_months(self):
        """Retrieves a list of months for which data exists in the database."""
        months = set()
        for table in ["incomes", "expenses", "savings"]:
            self.cursor.execute(f"SELECT DISTINCT strftime('%Y-%m', date) FROM {table}")
            results = self.cursor.fetchall()
            for row in results:
                months.add(row[0])
        return sorted(list(months), reverse=True) # Sort months in reverse chronological order


    # --- Income Tab ---

    def create_income_tab(self):
        """Creates the UI elements for the Income tab."""
        # Date
        self.income_date_label = tk.Label(self.income_tab, text="Date:", font=self.font)
        self.income_date_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.income_date_entry = tk.Entry(self.income_tab)
        self.income_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d")) # Default date
        self.income_date_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        # Category
        self.income_category_label = tk.Label(self.income_tab, text="Category:", font=self.font)
        self.income_category_label.grid(row=1, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.income_category_combo = ttk.Combobox(self.income_tab, values=self.income_categories, state="readonly")
        self.income_category_combo.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.income_category_combo.set(self.income_categories[0])  # Default category

        # Amount
        self.income_amount_label = tk.Label(self.income_tab, text="Amount:", font=self.font)
        self.income_amount_label.grid(row=2, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.income_amount_entry = tk.Entry(self.income_tab)
        self.income_amount_entry.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        # Description
        self.income_description_label = tk.Label(self.income_tab, text="Description:", font=self.font)
        self.income_description_label.grid(row=3, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.income_description_entry = tk.Entry(self.income_tab)
        self.income_description_entry.grid(row=3, column=1, padx=self.padx, pady=self.pady)

        # Add Income Button
        self.add_income_button = tk.Button(self.income_tab, text="Add Income", command=self.add_income, font=self.font)
        self.add_income_button.grid(row=4, column=0, columnspan=2, pady=self.pady)

        # Income Treeview
        self.income_tree = ttk.Treeview(self.income_tab, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.income_tree.heading("Date", text="Date")
        self.income_tree.heading("Category", text="Category")
        self.income_tree.heading("Amount", text="Amount")
        self.income_tree.heading("Description", text="Description")

        # Configure column widths
        self.income_tree.column("Date", width=100)
        self.income_tree.column("Category", width=100)
        self.income_tree.column("Amount", width=80)
        self.income_tree.column("Description", width=200)

        self.income_tree.grid(row=5, column=0, columnspan=2, padx=self.padx, pady=self.pady, sticky="nsew") # Expand and fill

        # Add scrollbar
        self.income_scrollbar = ttk.Scrollbar(self.income_tab, orient="vertical", command=self.income_tree.yview)
        self.income_scrollbar.grid(row=5, column=2, sticky="ns")
        self.income_tree.configure(yscrollcommand=self.income_scrollbar.set)

        #Make the TreeView expandable
        self.income_tab.grid_rowconfigure(5, weight=1)
        self.income_tab.grid_columnconfigure(0, weight=1)
        self.income_tab.grid_columnconfigure(1, weight=1)


        self.populate_income_tree()

    def add_income(self):
        """Adds a new income entry to the database."""
        date = self.income_date_entry.get()
        category = self.income_category_combo.get()
        try:
            amount = float(self.income_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        description = self.income_description_entry.get()

        self.cursor.execute("INSERT INTO incomes (date, category, amount, description) VALUES (?, ?, ?, ?)",
                            (date, category, amount, description))
        self.conn.commit()
        self.clear_income_fields()
        self.populate_income_tree()
        self.update_report_months()

    def populate_income_tree(self):
        """Populates the income Treeview with data from the database."""
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
        self.cursor.execute("SELECT date, category, amount, description FROM incomes ORDER BY date DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            self.income_tree.insert("", "end", values=row)

    def clear_income_fields(self):
        """Clears the input fields in the Income tab."""
        self.income_date_entry.delete(0, tk.END)
        self.income_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.income_amount_entry.delete(0, tk.END)
        self.income_description_entry.delete(0, tk.END)


    # --- Expenses Tab ---

    def create_expense_tab(self):
        """Creates the UI elements for the Expenses tab."""
        # Date
        self.expense_date_label = tk.Label(self.expense_tab, text="Date:", font=self.font)
        self.expense_date_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.expense_date_entry = tk.Entry(self.expense_tab)
        self.expense_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))  # Default date
        self.expense_date_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        # Category
        self.expense_category_label = tk.Label(self.expense_tab, text="Category:", font=self.font)
        self.expense_category_label.grid(row=1, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.expense_category_combo = ttk.Combobox(self.expense_tab, values=self.expense_categories, state="readonly")
        self.expense_category_combo.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.expense_category_combo.set(self.expense_categories[0])  # Default category

        # Amount
        self.expense_amount_label = tk.Label(self.expense_tab, text="Amount:", font=self.font)
        self.expense_amount_label.grid(row=2, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.expense_amount_entry = tk.Entry(self.expense_tab)
        self.expense_amount_entry.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        # Description
        self.expense_description_label = tk.Label(self.expense_tab, text="Description:", font=self.font)
        self.expense_description_label.grid(row=3, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.expense_description_entry = tk.Entry(self.expense_tab)
        self.expense_description_entry.grid(row=3, column=1, padx=self.padx, pady=self.pady)

        # Add Expense Button
        self.add_expense_button = tk.Button(self.expense_tab, text="Add Expense", command=self.add_expense, font=self.font)
        self.add_expense_button.grid(row=4, column=0, columnspan=2, pady=self.pady)

        # Expense Treeview
        self.expense_tree = ttk.Treeview(self.expense_tab, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Description", text="Description")

        # Configure column widths
        self.expense_tree.column("Date", width=100)
        self.expense_tree.column("Category", width=100)
        self.expense_tree.column("Amount", width=80)
        self.expense_tree.column("Description", width=200)

        self.expense_tree.grid(row=5, column=0, columnspan=2, padx=self.padx, pady=self.pady, sticky="nsew")  # Expand and fill

        # Add scrollbar
        self.expense_scrollbar = ttk.Scrollbar(self.expense_tab, orient="vertical", command=self.expense_tree.yview)
        self.expense_scrollbar.grid(row=5, column=2, sticky="ns")
        self.expense_tree.configure(yscrollcommand=self.expense_scrollbar.set)

        #Make the TreeView expandable
        self.expense_tab.grid_rowconfigure(5, weight=1)
        self.expense_tab.grid_columnconfigure(0, weight=1)
        self.expense_tab.grid_columnconfigure(1, weight=1)


        self.populate_expense_tree()

    def add_expense(self):
        """Adds a new expense entry to the database."""
        date = self.expense_date_entry.get()
        category = self.expense_category_combo.get()
        try:
            amount = float(self.expense_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        description = self.expense_description_entry.get()

        self.cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                            (date, category, amount, description))
        self.conn.commit()
        self.clear_expense_fields()
        self.populate_expense_tree()
        self.update_report_months()

    def populate_expense_tree(self):
        """Populates the expense Treeview with data from the database."""
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        self.cursor.execute("SELECT date, category, amount, description FROM expenses ORDER BY date DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            self.expense_tree.insert("", "end", values=row)

    def clear_expense_fields(self):
        """Clears the input fields in the Expense tab."""
        self.expense_date_entry.delete(0, tk.END)
        self.expense_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.expense_amount_entry.delete(0, tk.END)
        self.expense_description_entry.delete(0, tk.END)

    # --- Savings Tab ---

    def create_savings_tab(self):
        """Creates the UI elements for the Savings tab."""
        # Date
        self.savings_date_label = tk.Label(self.savings_tab, text="Date:", font=self.font)
        self.savings_date_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.savings_date_entry = tk.Entry(self.savings_tab)
        self.savings_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))  # Default date
        self.savings_date_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        # Amount
        self.savings_amount_label = tk.Label(self.savings_tab, text="Amount:", font=self.font)
        self.savings_amount_label.grid(row=1, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.savings_amount_entry = tk.Entry(self.savings_tab)
        self.savings_amount_entry.grid(row=1, column=1, padx=self.padx, pady=self.pady)

        # Description
        self.savings_description_label = tk.Label(self.savings_tab, text="Description:", font=self.font)
        self.savings_description_label.grid(row=2, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.savings_description_entry = tk.Entry(self.savings_tab)
        self.savings_description_entry.grid(row=2, column=1, padx=self.padx, pady=self.pady)

        # Add Savings Button
        self.add_savings_button = tk.Button(self.savings_tab, text="Add Savings", command=self.add_savings, font=self.font)
        self.add_savings_button.grid(row=3, column=0, columnspan=2, pady=self.pady)

        # Savings Treeview
        self.savings_tree = ttk.Treeview(self.savings_tab, columns=("Date", "Amount", "Description"), show="headings")
        self.savings_tree.heading("Date", text="Date")
        self.savings_tree.heading("Amount", text="Amount")
        self.savings_tree.heading("Description", text="Description")

        # Configure column widths
        self.savings_tree.column("Date", width=100)
        self.savings_tree.column("Amount", width=80)
        self.savings_tree.column("Description", width=200)

        self.savings_tree.grid(row=4, column=0, columnspan=2, padx=self.padx, pady=self.pady, sticky="nsew")  # Expand and fill

        # Add scrollbar
        self.savings_scrollbar = ttk.Scrollbar(self.savings_tab, orient="vertical", command=self.savings_tree.yview)
        self.savings_scrollbar.grid(row=4, column=2, sticky="ns")
        self.savings_tree.configure(yscrollcommand=self.savings_scrollbar.set)

        #Make the TreeView expandable
        self.savings_tab.grid_rowconfigure(4, weight=1)
        self.savings_tab.grid_columnconfigure(0, weight=1)
        self.savings_tab.grid_columnconfigure(1, weight=1)

        self.populate_savings_tree()

    def add_savings(self):
        """Adds a new savings entry to the database."""
        date = self.savings_date_entry.get()
        try:
            amount = float(self.savings_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        description = self.savings_description_entry.get()

        self.cursor.execute("INSERT INTO savings (date, amount, description) VALUES (?, ?, ?)",
                            (date, amount, description))
        self.conn.commit()
        self.clear_savings_fields()
        self.populate_savings_tree()
        self.update_report_months()


    def populate_savings_tree(self):
        """Populates the savings Treeview with data from the database."""
        for item in self.savings_tree.get_children():
            self.savings_tree.delete(item)
        self.cursor.execute("SELECT date, amount, description FROM savings ORDER BY date DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            self.savings_tree.insert("", "end", values=row)

    def clear_savings_fields(self):
        """Clears the input fields in the Savings tab."""
        self.savings_date_entry.delete(0, tk.END)
        self.savings_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.savings_amount_entry.delete(0, tk.END)
        self.savings_description_entry.delete(0, tk.END)


    # --- Reports Tab ---

    def create_report_tab(self):
        """Creates the UI elements for the Reports tab."""
        self.report_month_label = tk.Label(self.report_tab, text="Select Month:", font=self.font)
        self.report_month_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)

        self.report_month_combo = ttk.Combobox(self.report_tab, values=self.report_months, state="readonly")
        self.report_month_combo.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        if self.report_months:
            self.report_month_combo.set(self.report_months[0])  # Default to the most recent month
        else:
            self.report_month_combo.set("")


        self.generate_report_button = tk.Button(self.report_tab, text="Generate Report", command=self.generate_report, font=self.font)
        self.generate_report_button.grid(row=0, column=2, padx=self.padx, pady=self.pady)

        self.report_text = tk.Text(self.report_tab, wrap=tk.WORD, font=self.font)
        self.report_text.grid(row=1, column=0, columnspan=3, padx=self.padx, pady=self.pady, sticky="nsew")

        self.report_scrollbar = ttk.Scrollbar(self.report_tab, orient="vertical", command=self.report_text.yview)
        self.report_scrollbar.grid(row=1, column=3, sticky="ns")
        self.report_text.configure(yscrollcommand=self.report_scrollbar.set)

        #Make the report tab expandable
        self.report_tab.grid_rowconfigure(1, weight=1)
        self.report_tab.grid_columnconfigure(0, weight=1)
        self.report_tab.grid_columnconfigure(1, weight=1)
        self.report_tab.grid_columnconfigure(2, weight=1)

    def update_report_months(self):
        """Updates the available report months in the combo box."""
        self.report_months = self.get_available_report_months()
        self.report_month_combo['values'] = self.report_months
        if self.report_months:
            self.report_month_combo.set(self.report_months[0]) # set the most recent month
        else:
             self.report_month_combo.set("")


    def generate_report(self):
        """Generates a financial report for the selected month."""
        selected_month = self.report_month_combo.get()
        if not selected_month:
            messagebox.showinfo("Info", "No data available to generate a report.")
            return

        # Clear previous report
        self.report_text.delete("1.0", tk.END)

        # Calculate total income
        self.cursor.execute("SELECT SUM(amount) FROM incomes WHERE strftime('%Y-%m', date) = ?", (selected_month,))
        total_income = self.cursor.fetchone()[0]
        if total_income is None:
            total_income = 0.0

        # Calculate total expenses
        self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ?", (selected_month,))
        total_expenses = self.cursor.fetchone()[0]
        if total_expenses is None:
            total_expenses = 0.0

         # Calculate total savings
        self.cursor.execute("SELECT SUM(amount) FROM savings WHERE strftime('%Y-%m', date) = ?", (selected_month,))
        total_savings = self.cursor.fetchone()[0]
        if total_savings is None:
            total_savings = 0.0

        #Calculate net savings
        net_savings = total_income - total_expenses

        # Generate report string
        report = f"Financial Report for {calendar.month_name[int(selected_month[5:])]} {selected_month[:4]}\n\n" #Better month display
        report += f"Total Income: ${total_income:.2f}\n"
        report += f"Total Expenses: ${total_expenses:.2f}\n"
        report += f"Total Savings: ${total_savings:.2f}\n"
        report += f"Net savings: ${net_savings:.2f}\n\n"
        report += "--- Income Details ---\n"
        self.cursor.execute("SELECT category, amount, description FROM incomes WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC", (selected_month,))
        income_details = self.cursor.fetchall()
        for category, amount, description in income_details:
            report += f"{category}: ${amount:.2f} - {description}\n"

        report += "\n--- Expense Details ---\n"
        self.cursor.execute("SELECT category, amount, description FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC", (selected_month,))
        expense_details = self.cursor.fetchall()
        for category, amount, description in expense_details:
            report += f"{category}: ${amount:.2f} - {description}\n"

        report += "\n--- Savings Details ---\n"
        self.cursor.execute("SELECT amount, description FROM savings WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC", (selected_month,))
        savings_details = self.cursor.fetchall()
        for amount, description in savings_details:
            report += f"${amount:.2f} - {description}\n"

        self.report_text.insert(tk.END, report)

    def close_db_connection(self):
        """Closes the database connection when the application is closed."""
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close_db_connection(), root.destroy())) #Handle closing the window
