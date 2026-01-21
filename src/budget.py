import ttkbootstrap as ttk
import tkinter as tk
from src.database import Database


class BudgetPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.db = Database()  # connect to database

        # -----------------------------
        # PAGE HEADING
        # -----------------------------
        heading = ttk.Label(
            self,
            text="Budget Planner",
            font=("Helvetica", 22, "bold")
        )
        heading.pack(pady=20)

        # -----------------------------
        # BUDGET FORM
        # -----------------------------
        form_frame = ttk.LabelFrame(self, text="Set Monthly Budget")
        form_frame.pack(fill="x", padx=30, pady=10)

        # Category
        ttk.Label(form_frame, text="Category:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.category_entry = ttk.Entry(form_frame, width=30)
        self.category_entry.grid(row=0, column=1, padx=10, pady=5)

        # Amount
        ttk.Label(form_frame, text="Budget Amount:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.amount_entry = ttk.Entry(form_frame, width=20)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Add Button
        add_btn = ttk.Button(
            form_frame,
            text="Add Budget",
            command=self.add_budget
        )
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # -----------------------------
        # BUDGET TABLE
        # -----------------------------
        table_frame = ttk.LabelFrame(self, text="Budget Overview")
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)

        columns = ("category", "amount")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        # Table headings
        self.table.heading("category", text="Category")
        self.table.heading("amount", text="Budget Amount")

        # Column widths
        self.table.column("category", width=200)
        self.table.column("amount", width=120)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Load saved budgets into table
        self.load_budgets()

    # -----------------------------
    # ADD BUDGET FUNCTION
    # -----------------------------
    def add_budget(self):
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if category and amount:
            # Save to database
            self.db.add_budget(category, amount)

            # Insert into table
            self.table.insert("", "end", values=(category, amount))

            # Clear fields
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

    # -----------------------------
    # LOAD BUDGETS FROM DATABASE
    # -----------------------------
    def load_budgets(self):
        budgets = self.db.get_budgets()
        for b in budgets:
            self.table.insert("", "end", values=(b["category"], b["amount"]))