import json
from dataclasses import asdict
from pathlib import Path

from models.account import Account
from repositories.account_repository import AccountRepository

class JsonAccountRepository(AccountRepository):

    def __init__(self, file_path: str = "data/accounts.json"):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():
            self.file_path.write_text("{}")

    def _load_all(self):
        data = json.loads(self.file_path.read_text())

        return {
            int(account_id): Account(**account_data)
            for account_id, account_data in data.items()
        }

    def save(self, account):
        accounts = self._load_all()

        accounts[account.id] = account

        data = {
            str(account_id): asdict(account)
            for account_id, account in accounts.items()
        }

        self.file_path.write_text(
            json.dumps(data, indent=2)
        )

    def get(self, account_id):
        accounts = self._load_all()
        return accounts.get(account_id)

    def list_all(self):
        return list(self._load_all().values())

    def delete(self, account_id):
        accounts = self._load_all()

        if account_id in accounts:
            del accounts[account_id]

            data = {
                str(account_id): asdict(account)
                for account_id, account in accounts.items()
            }

            self.file_path.write_text(
                json.dumps(data, indent=2)
            )