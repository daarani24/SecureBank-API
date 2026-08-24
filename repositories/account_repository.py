from abc import ABC, abstractmethod

class AccountRepository(ABC):

    @abstractmethod
    def save(self, account):
        pass

    @abstractmethod
    def get(self, account_id):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def delete(self, account_id):
        pass