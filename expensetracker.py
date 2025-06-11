import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# ==== Expense Class ====
class Expense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

# ==== Expense Tracker Class ====
class ExpenseTracker:
    def __init__(self, file_path="expenses.json"):
        self.expenses = []
        self.file_path = file_path
        self.load_expenses()

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_expenses()

    def get_expenses(self):
        return self.expenses

    def save_expenses(self):
        with open(self.file_path, "w") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=4)

    def load_expenses(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                    self.expenses = [Expense(**item) for item in data]
                except json.JSONDecodeError:
                    self.expenses = []

    def clear_expenses(self):
        self.expenses = []
        self.save_expenses()

# ==== GUI Class ====
class ExpenseTrackerApp:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")

        # Entry Fields
        tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, pady=5)

        tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, pady=5)

        tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=2, column=1, pady=5)

        # Buttons
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Clear All", command=self.clear_all).grid(row=3, column=2, pady=10)

        # Treeview for displaying expenses
        self.tree = ttk.Treeview(root, columns=("Amount", "Category", "Description"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.column("Amount", width=80)
        self.tree.column("Category", width=120)
        self.tree.column("Description", width=200)
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.load_tree()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        if not amount or not category:
            messagebox.showerror("Input Error", "Amount and Category are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")
            return

        expense = Expense(amount, category, description)
        self.tracker.add_expense(expense)
        self.tree.insert("", "end", values=(amount, category, description))

        # Clear fields
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def load_tree(self):
        for exp in self.tracker.get_expenses():
            self.tree.insert("", "end", values=(exp.amount, exp.category, exp.description))

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all expenses?"):
            self.tracker.clear_expenses()
            for item in self.tree.get_children():
                self.tree.delete(item)

# ==== Run the Application ====
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
