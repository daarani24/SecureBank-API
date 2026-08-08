from models.account import Account
from collections import defaultdict
from models.account import Account, Transaction
from exceptions.bank_exceptions import AccountNotFoundError, InsufficientFundsError
from utils.validators import validate_amount, validate_customer_name

class BankLedger:
    def __init__(self):
        self.accounts: dict[int, Account]={}
        self._next_account_id=1001
        self.transaction_log: dict[int, list[Transaction]]=defaultdict(list)
        self.customer_index: dict[str, list[int]]=defaultdict(list)

    def create_account(self, customer_name):
        clean_name=validate_customer_name(customer_name)
        account_id=self._next_account_id
        self._next_account_id+=1
        account=Account(id=account_id, customer_name=clean_name)
        self.accounts[account_id]=account
        self.customer_index[clean_name].append(account_id)
        return account

    def get_account_by_id(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Account {account_id} does not exist")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        account.balance+=amount
        self.transaction_log[account_id].append(Transaction("deposit", amount))
        return account

    def withdraw(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        if amount>account.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}, balance is {account.balance}"
            )
        account.balance-=amount
        self.transaction_log[account_id].append(Transaction("withdraw", amount))
        return account

    def transfer(self, from_id, to_id, amount):
        validate_amount(amount)
        self.get_account_by_id(from_id)
        self.get_account_by_id(to_id)
        self.withdraw(from_id, amount)
        try:
            self.deposit(to_id, amount)
        except Exception:
            self.deposit(from_id, amount)
            raise
        self.transaction_log[from_id][-1]=Transaction("transfer_out", amount)
        self.transaction_log[to_id][-1]=Transaction("transfer_in",amount)

    def reverse_last_transaction(self, account_id):
        history=self.transaction_log[account_id]
        if not history:
            raise AccountNotFoundError(f"No transaction found for account {account_id}")
        last=history.pop()
        account=self.get_account_by_id(account_id)
        if last.type in ("deposit", "transfer_in"):
            account.balance-=last.amount
        elif last.type in ("withdraw", "transfer_out"):
            account.balance+=last.amount

    def get_accounts_by_customer(self, customer_name):
        ids=self.customer_index.get(customer_name, [])
        return [self.accounts[i] for i in ids if i in self.accounts]
    
    def get_balance(self, account_id):
        return self.get_account_by_id(account_id).balance

    def close_account(self, account_id):
        self.get_account_by_id(account_id)
        del self.accounts[account_id]

    def list_accounts(self):
        return list(self.accounts.values())

