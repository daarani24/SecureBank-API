from models.account import Account
from exceptions.bank_exceptions import AccountNotFoundError, InsufficientFundsError
from utils.validators import validate_amount, validate_customer_name

class BankLedger:
    def __init__(self):
        self.accounts: dict[int, Account]={}
        self._next_account_id=1001

    def create_account(self, customer_name):
        clean_name=validate_customer_name(customer_name)
        account_id=self._next_account_id
        self._next_account_id+=1
        account=Account(id=account_id, customer_name=clean_name)
        self.accounts[account_id]=account
        return account

    def get_account_by_id(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Account {account_id} does not exist")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        account.balance+=amount
        return account

    def withdraw(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        if amount>account.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}, balance is {account.balance}"
            )
        account.balance-=amount
        return account

    def get_balance(self, account_id):
        return self.get_account_by_id(account_id).balance

    def close_account(self, account_id):
        self.get_account_by_id(account_id)
        del self.accounts[account_id]

    def list_accounts(self):
        return list(self.accounts.values())
