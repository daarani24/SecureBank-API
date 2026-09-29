from abc import ABC, abstractmethod
from typing import Optional
from models.account import Account

class AccountRepository(ABC):

    @abstractmethod
    def save(self, account: Account) -> None:
        pass

    @abstractmethod
    def get(self, account_id: int) -> Optional[Account]:
        pass

    @abstractmethod
    def list_all(self) -> list[Account]:
        pass

    @abstractmethod
    def delete(self, account_id: int) -> None:
        pass