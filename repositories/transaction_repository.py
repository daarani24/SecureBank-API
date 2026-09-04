from abc import ABC, abstractmethod
from models.transaction import Transaction


class TransactionRepository(ABC):

    @abstractmethod
    def save(self, account_id, transaction):
        pass

    @abstractmethod
    def get_by_account(self, account_id):
        pass