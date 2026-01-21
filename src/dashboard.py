import ttkbootstrap as ttk
import tkinter as tk
from src.database import Database


class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # -----------------------------
        # PAGE HEADING
        # -----------------------------
        heading = ttk.Label(
            self,
            text="Dashboard Overview",
            font=("Helvetica", 22, "bold")
        )
        heading.pack(pady=20)

        # -----------------------------
        # SUMMARY CARDS SECTION
        # -----------------------------
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill="x", padx=30)

        # Income Card
        income_card = ttk.LabelFrame(cards_frame, text="Total Income")
        income_card.pack(side="left", expand=True, fill="both", padx=10)
        self.income_label = ttk.Label(
            income_card,
            text="₦0.00",
            font=("Helvetica", 18, "bold")
        )
        self.income_label.pack(pady=10)

        # Expenses Card
        expense_card = ttk.LabelFrame(cards_frame, text="Total Expenses")
        expense_card.pack(side="left", expand=True, fill="both", padx=10)
        self.expense_label = ttk.Label(
            expense_card,
            text="₦0.00",
            font=("Helvetica", 18, "bold")
        )
        self.expense_label.pack(pady=10)

        # Balance Card
        balance_card = ttk.LabelFrame(cards_frame, text="Current Balance")
        balance_card.pack(side="left", expand=True, fill="both", padx=10)
        self.balance_label = ttk.Label(
            balance_card,
            text="₦0.00",
            font=("Helvetica", 18, "bold")
        )
        self.balance_label.pack(pady=10)

        # -----------------------------
        # RECENT TRANSACTIONS SECTION
        # -----------------------------
        recent_frame = ttk.LabelFrame(self, text="Recent Transactions")
        recent_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.recent_frame = recent_frame  # store for dynamic updates

    # ----------------------------------------------------
    # REFRESH DASHBOARD DATA (CALL THIS WHEN PAGE OPENS)
    # ----------------------------------------------------
    def refresh(self):
        db = Database()
        data = db.load_data()

        transactions = data["transactions"]

        # Calculate totals
        income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        balance = income - expenses

        # Update labels
        self.income_label.config(text=f"₦{income:,.2f}")
        self.expense_label.config(text=f"₦{expenses:,.2f}")
        self.balance_label.config(text=f"₦{balance:,.2f}")

        # Clear old recent transactions
        for widget in self.recent_frame.winfo_children():
            widget.destroy()

        # Show recent 5 transactions
        if not transactions:
            ttk.Label(
                self.recent_frame,
                text="No recent transactions available.",
                font=("Helvetica", 12, "italic")
            ).pack(pady=10)
        else:
            recent = transactions[-5:]
            for t in reversed(recent):
                ttk.Label(
                    self.recent_frame,
                    text=f"{t['description']} — ₦{t['amount']:,.2f} ({t['type']})",
                    font=("Helvetica", 11)
                ).pack(anchor="w", padx=10, pady=2)