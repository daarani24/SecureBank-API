from pydantic import BaseModel
from models.account import Account

class AccountDTO(BaseModel):
    id: int
    customer_name: str
    balance: float

    @classmethod
    def from_account(cls, account: Account) -> "AccountDTO":
        return cls(
            id=account.id,
            customer_name=account.customer_name,
            balance=account.balance
        )