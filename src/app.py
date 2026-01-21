import ttkbootstrap as ttk
import tkinter as tk

from src.dashboard import DashboardPage
from src.transactions import TransactionsPage
from src.budget import BudgetPage
from src.charts import ChartsPage
from src.settings import SettingsPage
from src.database import Database


class FinanceApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")

        self.title("Personal Finance Tracker")
        self.geometry("900x600")

        self.db = Database()  # shared database instance

        # -----------------------------
        # MAIN CONTAINER
        # -----------------------------
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # -----------------------------
        # SIDEBAR
        # -----------------------------
        sidebar = ttk.Frame(container, width=180)
        sidebar.pack(side="left", fill="y")

        ttk.Label(
            sidebar,
            text="Finance Tracker",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)

        # Sidebar buttons
        buttons = [
            ("Dashboard", lambda: self.show_frame("Dashboard")),
            ("Transactions", lambda: self.show_frame("Transactions")),
            ("Budget", lambda: self.show_frame("Budget")),
            ("Charts", lambda: self.show_frame("Charts")),
            ("Settings", lambda: self.show_frame("Settings")),
        ]

        for text, command in buttons:
            ttk.Button(sidebar, text=text, command=command).pack(
                fill="x", padx=10, pady=5
            )

        # -----------------------------
        # PAGE CONTAINER
        # -----------------------------
        self.frames = {}
        page_container = ttk.Frame(container)
        page_container.pack(side="right", fill="both", expand=True)

        # Initialize all pages
        for PageClass, name in [
            (DashboardPage, "Dashboard"),
            (TransactionsPage, "Transactions"),
            (BudgetPage, "Budget"),
            (ChartsPage, "Charts"),
            (SettingsPage, "Settings"),
        ]:
            frame = PageClass(page_container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show default page
        self.show_frame("Dashboard")

    # -----------------------------
    # SHOW PAGE
    # -----------------------------
    def show_frame(self, page_name):
        page = self.frames[page_name]

        # Refresh dashboard when opened
        if page_name == "Dashboard":
            page.refresh()

        page.tkraise()

        # ⭐ Refresh charts when Charts page is opened
        if page_name == "Charts":
            page.show()

    # -----------------------------
    # APPLY THEME (USED BY SETTINGS)
    # -----------------------------
    def apply_theme(self, theme_name):
        self.style.theme_use(theme_name)

    # -----------------------------
    # REFRESH ALL PAGES (USED AFTER RESET)
    # -----------------------------
    def refresh_all_pages(self):
        # Recreate pages so they reload data from database
        for name, frame in self.frames.items():
            frame.destroy()

        # Rebuild pages
        container = list(self.frames.values())[0].master

        self.frames = {}
        for PageClass, name in [
            (DashboardPage, "Dashboard"),
            (TransactionsPage, "Transactions"),
            (BudgetPage, "Budget"),
            (ChartsPage, "Charts"),
            (SettingsPage, "Settings"),
        ]:
            frame = PageClass(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()