import ttkbootstrap as ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.database import Database


class ChartsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.db = Database()  # connect to database

        # -----------------------------
        # PAGE HEADING
        # -----------------------------
        heading = ttk.Label(
            self,
            text="Charts & Analytics",
            font=("Helvetica", 22, "bold")
        )
        heading.pack(pady=20)

        # -----------------------------
        # CHART FRAME
        # -----------------------------
        self.chart_frame = ttk.LabelFrame(self, text="Income vs Expenses")
        self.chart_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # ⭐ Delay chart drawing so Tkinter can finish loading the page
        self.after(150, self.draw_chart)

    # -----------------------------
    # CALCULATE REAL TOTALS
    # -----------------------------
    def get_totals(self):
        transactions = self.db.get_transactions()

        total_income = 0
        total_expenses = 0

        for t in transactions:
            amount = float(t["amount"])
            if t["type"] == "Income":
                total_income += amount
            else:
                total_expenses += amount

        return total_income, total_expenses

    # -----------------------------
    # DRAW REAL DATA CHART
    # -----------------------------
    def draw_chart(self):
        # Clear old chart widgets
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        income, expenses = self.get_totals()

        # Avoid empty chart crash
        if income == 0 and expenses == 0:
            ttk.Label(
                self.chart_frame,
                text="No data available yet.\nAdd transactions to generate charts.",
                font=("Helvetica", 12, "italic")
            ).pack(pady=20)
            return

        # Create figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        labels = []
        values = []

        if income > 0:
            labels.append("Income")
            values.append(income)

        if expenses > 0:
            labels.append("Expenses")
            values.append(expenses)

        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Income vs Expenses")

        # Embed chart into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # -----------------------------
    # REFRESH CHART (CALLED AFTER RESET)
    # -----------------------------
    def refresh(self):
        self.draw_chart()

    # -----------------------------
    # SHOW PAGE (CALLED WHEN PAGE IS OPENED)
    # -----------------------------
    def show(self):
        self.draw_chart()