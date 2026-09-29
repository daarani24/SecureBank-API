from typing import Optional
from models.account import Account
from repositories.account_repository import AccountRepository

class InMemoryAccountRepository(AccountRepository):
    def __init__(self):
        self.accounts={}

    def save(self, account: Account)->None:
        self.accounts[account.id]=account

    def get(self, account_id: int)->Optional[Account]:
        return self.accounts.get(account_id)

    def list_all(self) -> list[Account]:
        return list(self.accounts.values())

    def delete(self, account_id: int)->None:
        if account_id in self.accounts:
            del self.accounts[account_id]