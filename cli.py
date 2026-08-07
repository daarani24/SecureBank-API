from services.bank_ledger import BankLedger
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
EXIT="7"

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
7. Exit
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

            elif choice==EXIT:
                print("Thank you for using SecureBank. Goodbye.")
                is_running=False

            else:
                print("Invalid option. Please choose between 1 and 7.")

        except (AccountNotFoundError, InsufficientFundsError, InvalidAmountError, InvalidNameError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter a valid number.")
