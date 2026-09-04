from models.account import Account
from collections import defaultdict
from models.account import Account, Transaction
from exceptions.bank_exceptions import AccountNotFoundError, InsufficientFundsError
from utils.validators import validate_amount, validate_customer_name
from repositories.transaction_repository import TransactionRepository

class BankLedger:
    def __init__(self, repository=None, transaction_repository:TransactionRepository|None=None):
        self.repository=repository
        self.transaction_repository=transaction_repository
        self.accounts: dict[int, Account]={}
        self._next_account_id=1001
        self.transaction_log: dict[int, list[Transaction]]=defaultdict(list)
        self.customer_index: dict[str, list[int]]=defaultdict(list)

        if self.repository:
            for account in self.repository.list_all():
                self.accounts[account.id]=account
                self.customer_index[account.customer_name].append(account.id)

                if account.id>=self._next_account_id:
                    self._next_account_id=account.id+1

        if self.transaction_repository:
            for account_id in self.accounts:
                history=self.transaction_repository.get_by_account(account_id)
                self.transaction_log[account_id].extend(history)

    def create_account(self, customer_name):
        name=validate_customer_name(customer_name)
        account_id=self._next_account_id
        self._next_account_id+=1
        account=Account(id=account_id, customer_name=name)
        self.accounts[account_id]=account
        self.customer_index[name].append(account_id)
        if self.repository:
            self.repository.save(account)
        return account

    def get_account_by_id(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Account {account_id} does not exist")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        account.balance+=amount
        transaction=Transaction("deposit", amount)
        self.transaction_log[account_id].append(transaction)
        self._save_transaction(account_id, transaction)

        if self.repository:
            self.repository.save(account)
        return account

    def withdraw(self, account_id, amount):
        validate_amount(amount)
        account=self.get_account_by_id(account_id)
        if amount>account.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}, balance is {account.balance}"
            )
        account.balance-=amount
        transaction=Transaction("withdraw", amount)
        self.transaction_log[account_id].append(transaction)
        self._save_transaction(account_id, transaction)

        if self.repository:
            self.repository.save(account)
        return account

    def transfer(self, from_id, to_id, amount):
        validate_amount(amount)
        from_account=self.get_account_by_id(from_id)
        to_account=self.get_account_by_id(to_id)

        if amount>from_account.balance:
            raise InsufficientFundsError(
                f"Cannot transfer {amount}, balance is {from_account.balance}"
            )
        from_account.balance-=amount
        to_account.balance+=amount
        outgoing=Transaction("transfer_out", amount)
        incoming=Transaction("transfer_in", amount)

        self.transaction_log[from_id].append(outgoing)
        self.transaction_log[to_id].append(incoming)
        self._save_transaction(from_id, outgoing)
        self._save_transaction(to_id, incoming)

        if self.repository:
            self.repository.save(from_account)
            self.repository.save(to_account)

    def reverse_last_transaction(self, account_id):
        history=self.transaction_log[account_id]
        if not history:
            raise AccountNotFoundError(
                f"No transaction found for account {account_id}"
            )
        last=history[-1]
        account=self.get_account_by_id(account_id)

        if last.type in ("deposit", "transfer_in"):
            account.balance-=last.amount
        elif last.type in ("withdraw", "transfer_out"):
            account.balance+=last.amount

        reversal=Transaction("reversal", last.amount)
        history.append(reversal)
        self._save_transaction(account_id, reversal)

        if self.repository:
            self.repository.save(account)
        return account

    def get_accounts_by_customer(self, customer_name):
        ids=self.customer_index.get(customer_name, [])
        return [self.accounts[i] for i in ids if i in self.accounts]
    
    def get_balance(self, account_id):
        return self.get_account_by_id(account_id).balance

    def close_account(self, account_id):
        self.get_account_by_id(account_id)
        del self.accounts[account_id]
        if self.repository:
            self.repository.delete(account_id)

    def list_accounts(self):
        return list(self.accounts.values())

    def _save_transaction(self, account_id, transaction):
        if self.transaction_repository:
            self.transaction_repository.save(account_id, transaction)
