import ttkbootstrap as ttk
import tkinter as tk
from src.database import Database


class TransactionsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.db = Database()  # connect to database

        # -----------------------------
        # PAGE HEADING
        # -----------------------------
        heading = ttk.Label(
            self,
            text="Transactions",
            font=("Helvetica", 22, "bold")
        )
        heading.pack(pady=20)

        # -----------------------------
        # ADD TRANSACTION FORM
        # -----------------------------
        form_frame = ttk.LabelFrame(self, text="Add New Transaction")
        form_frame.pack(fill="x", padx=30, pady=10)

        # Description
        ttk.Label(form_frame, text="Description:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.desc_entry = ttk.Entry(form_frame, width=40)
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)

        # Amount
        ttk.Label(form_frame, text="Amount:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.amount_entry = ttk.Entry(form_frame, width=20)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Type (Income/Expense)
        ttk.Label(form_frame, text="Type:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.type_var = tk.StringVar(value="Expense")
        type_menu = ttk.Combobox(
            form_frame,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            width=18
        )
        type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Add Button
        add_btn = ttk.Button(
            form_frame,
            text="Add Transaction",
            command=self.add_transaction
        )
        add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # -----------------------------
        # TRANSACTIONS TABLE
        # -----------------------------
        table_frame = ttk.LabelFrame(self, text="Transaction History")
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)

        columns = ("description", "amount", "type")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # Table headings
        self.table.heading("description", text="Description")
        self.table.heading("amount", text="Amount")
        self.table.heading("type", text="Type")

        # Column widths
        self.table.column("description", width=260)
        self.table.column("amount", width=120)
        self.table.column("type", width=120)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Load saved transactions into table
        self.load_transactions()

    # -----------------------------
    # ADD TRANSACTION FUNCTION
    # -----------------------------
    def add_transaction(self):
        desc = self.desc_entry.get().strip()
        amount_text = self.amount_entry.get().strip()
        ttype = self.type_var.get()

        if not desc or not amount_text:
            return  # ignore empty fields

        # Convert amount to float BEFORE saving
        try:
            amount = float(amount_text)
        except ValueError:
            return  # ignore invalid numbers

        # Save to database
        self.db.add_transaction(desc, amount, ttype)

        # Insert into table (formatted)
        self.table.insert("", "end", values=(desc, f"{amount:.2f}", ttype))

        # Clear fields
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    # -----------------------------
    # LOAD TRANSACTIONS FROM DATABASE
    # -----------------------------
    def load_transactions(self):
        transactions = self.db.get_transactions()
        for t in transactions:
            self.table.insert(
                "",
                "end",
                values=(t["description"], f"{float(t['amount']):.2f}", t["type"])
            )