from services.bank_ledger import BankLedger
from services.statement_service import accounts_sorted_by_id_bisect, accounts_sorted_by_balance
from exceptions.bank_exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidNameError,
)

CREATE="1"
DEPOSIT="2"
WITHDRAW="3"
BALANCE="4"
CLOSE="5"
LIST_ALL="6"
TRANSFER="7"
REVERSE="8"
FIND_BY_NAME="9"
SORT_BY_ID = "10"
SORT_BY_BALANCE = "11"
EXIT="12"

MENU="""
=============================
      SecureBank CLI
=============================
1. Create Account
2. Deposit Money
3. Withdraw Money
4. Check Balance
5. Close Account
6. List All Accounts
7. Transfer Money
8. Reverse Last Transaction
9. Find Accounts by Customer Name
10. Sort by ID
11. Sort by Balance
12. Exit
=============================
"""

def run_cli():
    ledger=BankLedger()
    is_running=True

    while is_running:
        print(MENU)
        choice=input("Choose an option: ").strip()

        try:
            if choice==CREATE:
                name=input("Customer name: ")
                acc=ledger.create_account(name)
                print("\n--- Account Created ---")
                print(f"Account ID : {acc.id}")
                print(f"Name       : {acc.customer_name}")
                print(f"Balance    : Rs.{acc.balance:.2f}")
                print("Please note down your Account ID.")
                print("------------------------\n")

            elif choice==DEPOSIT:
                acc_id=int(input("Account ID: "))
                amount=float(input("Amount: "))
                acc=ledger.deposit(acc_id, amount)
                print(f"Deposit successful. New Balance: Rs.{acc.balance:.2f}")

            elif choice==WITHDRAW:
                acc_id=int(input("Account ID: "))
                amount=float(input("Amount: "))
                acc=ledger.withdraw(acc_id, amount)
                print(f"Withdrawal successful. New Balance: Rs.{acc.balance:.2f}")

            elif choice==BALANCE:
                acc_id=int(input("Account ID: "))
                balance=ledger.get_balance(acc_id)
                print(f"Current Balance: Rs.{balance:.2f}")

            elif choice==CLOSE:
                acc_id=int(input("Account ID: "))
                ledger.close_account(acc_id)
                print(f"Account {acc_id} closed successfully.")

            elif choice==LIST_ALL:
                accounts=ledger.list_accounts()
                if not accounts:
                    print("No accounts yet.")
                else:
                    print("\n------------------- All Accounts -------------------")
                    for acc in accounts:
                        print(f"ID: {acc.id} | Name: {acc.customer_name} | Balance: Rs.{acc.balance:.2f}")
                    print("------------------------------------------------------\n")

            elif choice==TRANSFER:
                from_id=int(input("From Account ID: "))
                to_id=int(input("To Account ID: "))
                amount=float(input('Amount: '))
                ledger.transfer(from_id, to_id, amount)
                print(f"Transferred Rs.{amount:.2f} from {from_id} to {to_id} successfully.")

            elif choice==REVERSE:
                acc_id=int(input("Account ID: "))
                ledger.reverse_last_transaction(acc_id)
                new_balance=ledger.get_balance(acc_id)
                print(f"Last transaction reversed. New Balance: Rs.{new_balance:.2f}")

            elif choice==FIND_BY_NAME:
                name=input("Customer name: ").strip()
                accounts=ledger.get_accounts_by_customer(name)
                if not accounts:
                    print("No accounts found for that name.")
                else:
                    print(f"\n---------- Accounts for {name} ----------")
                    for acc in accounts:
                        print(f"ID: {acc.id} | Balance: Rs.{acc.balance:.2f}")
                    print("--------------------------------------------\n")

            elif choice==SORT_BY_ID:
                accounts=accounts_sorted_by_id_bisect(ledger.accounts)
                print("\n--- Accounts Sorted by ID ---")
                for acc in accounts:
                    print(f"ID: {acc.id} | Name: {acc.customer_name} | Balance: Rs.{acc.balance:.2f}")
                print("-----------------------------\n")

            elif choice==SORT_BY_BALANCE:
                accounts=accounts_sorted_by_balance(ledger.accounts)
                print("\n--- Accounts Sorted by Balance ---")
                for acc in accounts:
                    print(f"ID: {acc.id} | Name: {acc.customer_name} | Balance: Rs.{acc.balance:.2f}")
                print("-----------------------------------\n")

            elif choice==EXIT:
                print("Thank you for using SecureBank. Goodbye.")
                is_running=False

            else:
                print("Invalid option. Please choose between 1 and 7.")

        except (AccountNotFoundError, InsufficientFundsError, InvalidAmountError, InvalidNameError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter a valid number.")
