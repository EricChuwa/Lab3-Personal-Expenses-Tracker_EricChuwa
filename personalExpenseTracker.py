import os
from collections import namedtuple
from datetime import datetime

# Class in order that everything is neatly encapsulated in the case I wanna use the tracker in the future
class PersonalExpenseTracker:
    def __init__(self):
        self.balance_file = "balance.txt"
        Menu = namedtuple('Menu', ["desc", "func"])
        self.m_menu = {
            "1": Menu("Check Remaining Balance", self.check_balance),
            "2": Menu("View Expenses", self.view_expenses),
            "3": Menu("Add New Expense", self.add_new_expense),
            "4": Menu("Quit", None)
        }
        self.s_menu_AddExp = {
            "1": Menu("Search by item name", self.search_by_name),
            "2": Menu("Search by amount", self.search_by_amount),
            "3": Menu("Back to main menu", None)
        }
    # Getting Balance
    def get_balance(self):
        if not os.path.exists(self.balance_file):
            with open(self.balance_file, "w") as f:
                f.write("0")
            return 0.0
        try:
            with open(self.balance_file, "r") as f:
                return float(f.read().strip())
        except Exception:
            return 0.0

    # Setting the Balance
    def set_balance(self, balance):
        with open(self.balance_file, "w") as f:
            f.write(str(balance))

    # Allows to me to display menuz
    def display_menu(self, menu):
        for key, item in menu.items():
            print(f"{key}. {item.desc}")

    def total_expenses(self):
        total = 0.0
        for fname in os.listdir():
            if fname.startswith('expenses') and fname.endswith('.txt'):
                with open(fname, "r") as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 5:  # ID, Datetime, Item, Amount, Date
                            try:
                                total += float(parts[3])
                            except:
                                continue
        return total

    def main(self):
        while True:
            print("\n===== Personal Expenses Tracker =====")
            self.display_menu(self.m_menu)
            user_choice = input("Enter choice: ").strip()
            menu_item = self.m_menu.get(user_choice)
            if menu_item:
                if menu_item.func:
                    menu_item.func()
                else:
                    print("Exiting. Goodbye!")
                    break
            else:
                print("Invalid option.")

    # Checking available balance
    def check_balance(self):
        balance = self.get_balance()
        total_exp = self.total_expenses()
        print("\n--- Balance Report ---")
        print(f"Current Balance: {balance:.2f}")
        print(f"Total Expenses: {total_exp:.2f}")
        print(f"Available Balance: {balance-total_exp:.2f}")
        add = input("Add money to balance? (y/n): ").strip().lower()
        if add == "y":
            try:
                amt = float(input("Amount to add: "))
                if amt > 0:
                    balance += amt
                    self.set_balance(balance)
                    print(f"New balance: {balance:.2f}")
                else:
                    print("Amount must be positive.")
            except:
                print("Invalid input.")

    # add a new expense
    # This took me hella long to figure out
    def add_new_expense(self):
        balance = self.get_balance()
        total_exp = self.total_expenses()
        available = balance - total_exp
        print(f"\nAvailable Balance: {available:.2f}")
        # Get date input & validate
        while True:
            date_input = input("Enter date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date_input, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
        item = input("Item name: ").strip()
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except:
            print("Invalid amount.")
            return
        print(f"Date: {date_input}, Item: {item}, Amount: {amount:.2f}, Available: {available:.2f}")
        confirm = input("Confirm (y/n)? ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return
        if amount > available:
            print("Insufficient balance! Cannot save expense.")
            return
        fname = f"expenses{date_input}.txt"
        # Generate expense ID for the day's file
        eid = 1
        if os.path.exists(fname):
            with open(fname, "r") as f:
                eid = sum(1 for _ in f) + 1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Columns: ID,Datetime,Item,Amount,Date
        with open(fname, "a") as f:
            f.write(f"{eid},{now},{item},{amount:.2f},{date_input}\n")
        self.set_balance(balance - amount)
        print(f"Expense (ID {eid}) saved in {fname}. Remaining balance: {self.get_balance():.2f}")

    # Collecting all expense data from files
    def collect_all_expenses(self):
        expenses = []
        for fname in os.listdir(): # using OS to list the current items in the dir
            if fname.startswith('expenses') and fname.endswith('.txt'):
                with open(fname, "r") as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 5:
                            eid, dt, item, amount, date = parts
                            expenses.append({
                                "file": fname,
                                "id": eid,
                                "datetime": dt,
                                "item": item,
                                "amount": float(amount),
                                "date": date
                            })
        return expenses

    # Displays my expenses
    def view_expenses(self):
        print("\n---- Expense Search ----")
        self.display_menu(self.s_menu_AddExp)
        user_choice = input("Enter: ").strip()
        menu_item = self.s_menu_AddExp.get(user_choice)
        if menu_item and menu_item.func:
            search_query = input("Enter search term: ")
            menu_item.func(search_query)
        elif menu_item and not menu_item.func:
            return
        else:
            print("Invalid option.")

    # allows to search by name
    def search_by_name(self, term):
        expenses = self.collect_all_expenses()
        matches = [e for e in expenses if term.lower() in e['item'].lower()]
        if matches:
            print("Matching Expenses:")
            for e in matches:
                print(f"{e['file']} | ID: {e['id']} | {e['datetime']} | {e['item']} | {e['amount']:.2f}")
        else:
            print("No matching expenses found.")

    # Allows to search by amount
    def search_by_amount(self, term):
        try:
            value = float(term)
        except ValueError:
            print("Invalid amount.")
            return
        expenses = self.collect_all_expenses()
        matches = [e for e in expenses if abs(e['amount'] - value) < 1e-2]
        if matches:
            print("Matching Expenses:")
            for e in matches:
                print(f"{e['file']} | ID: {e['id']} | {e['datetime']} | {e['item']} | {e['amount']:.2f}")
        else:
            print("No matching expenses found.")

# Only works from here
if __name__ == "__main__":
    tracker = PersonalExpenseTracker()
    tracker.main()
