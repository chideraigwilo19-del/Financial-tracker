import json
import os


DB_FILE = "finance_data.json"


class Database:
    def __init__(self):
        # Create file if missing
        if not os.path.exists(DB_FILE):
            self._create_empty_db()

    # -----------------------------
    # INTERNAL: CREATE EMPTY FILE
    # -----------------------------
    def _create_empty_db(self):
        empty_data = {
            "transactions": [],
            "budgets": []
        }
        with open(DB_FILE, "w") as f:
            json.dump(empty_data, f, indent=4)

    # -----------------------------
    # LOAD FULL DATABASE
    # -----------------------------
    def load_data(self):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            self._create_empty_db()
            return self.load_data()

    # -----------------------------
    # SAVE FULL DATABASE
    # -----------------------------
    def save_data(self, data):
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # -----------------------------
    # TRANSACTIONS
    # -----------------------------
    def add_transaction(self, description, amount, ttype):
        data = self.load_data()
        data["transactions"].append({
            "description": description,
            "amount": amount,
            "type": ttype
        })
        self.save_data(data)

    def get_transactions(self):
        data = self.load_data()
        return data["transactions"]

    def clear_transactions(self):
        data = self.load_data()
        data["transactions"] = []
        self.save_data(data)

    # -----------------------------
    # BUDGETS
    # -----------------------------
    def add_budget(self, category, amount):
        data = self.load_data()
        data["budgets"].append({
            "category": category,
            "amount": amount
        })
        self.save_data(data)

    def get_budgets(self):
        data = self.load_data()
        return data["budgets"]

    def clear_budgets(self):
        data = self.load_data()
        data["budgets"] = []
        self.save_data(data)

    # -----------------------------
    # RESET EVERYTHING
    # -----------------------------
    def reset_all(self):
        self._create_empty_db()