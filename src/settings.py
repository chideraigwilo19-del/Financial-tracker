import ttkbootstrap as ttk
import tkinter as tk
from src.database import Database


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.db = Database()  # connect to database
        self.controller = controller

        # -----------------------------
        # PAGE HEADING
        # -----------------------------
        heading = ttk.Label(
            self,
            text="Settings",
            font=("Helvetica", 22, "bold")
        )
        heading.pack(pady=20)

        # -----------------------------
        # THEME SETTINGS
        # -----------------------------
        theme_frame = ttk.LabelFrame(self, text="Theme Settings")
        theme_frame.pack(fill="x", padx=30, pady=10)

        ttk.Label(theme_frame, text="Select Theme:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        self.theme_var = tk.StringVar(value="default")

        theme_menu = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["default", "darkly", "flatly", "superhero", "cosmo"],
            width=20
        )
        theme_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        apply_theme_btn = ttk.Button(
            theme_frame,
            text="Apply Theme",
            command=lambda: controller.apply_theme(self.theme_var.get())
        )
        apply_theme_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # -----------------------------
        # CURRENCY SETTINGS
        # -----------------------------
        currency_frame = ttk.LabelFrame(self, text="Currency Settings")
        currency_frame.pack(fill="x", padx=30, pady=10)

        ttk.Label(currency_frame, text="Select Currency:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        self.currency_var = tk.StringVar(value="₦")

        currency_menu = ttk.Combobox(
            currency_frame,
            textvariable=self.currency_var,
            values=["₦", "$", "€", "£"],
            width=10
        )
        currency_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        save_currency_btn = ttk.Button(
            currency_frame,
            text="Save Currency",
            command=self.save_currency
        )
        save_currency_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # -----------------------------
        # DATA RESET SECTION
        # -----------------------------
        reset_frame = ttk.LabelFrame(self, text="Data Management")
        reset_frame.pack(fill="x", padx=30, pady=20)

        reset_btn = ttk.Button(
            reset_frame,
            text="Reset All Data",
            command=self.reset_data
        )
        reset_btn.pack(pady=10)

        ttk.Label(
            reset_frame,
            text="(This will clear all transactions and budgets)",
            font=("Helvetica", 10, "italic")
        ).pack()

    # -----------------------------
    # SAVE CURRENCY FUNCTION
    # -----------------------------
    def save_currency(self):
        print(f"Currency saved: {self.currency_var.get()}")

    # -----------------------------
    # RESET DATA FUNCTION
    # -----------------------------
    def reset_data(self):
        self.db.reset_all()
        print("All data has been reset.")

        # OPTIONAL: Refresh other pages if needed
        if hasattr(self.controller, "refresh_all_pages"):
            self.controller.refresh_all_pages()