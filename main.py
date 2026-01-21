import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.app import FinanceApp

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()