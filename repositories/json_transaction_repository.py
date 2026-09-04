import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from models.transaction import Transaction
from repositories.transaction_repository import TransactionRepository

class JsonTransactionRepository(TransactionRepository):

    def __init__(self, file_path: str = "data/transactions.json"):
        self.file_path=Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        if not self.file_path.exists():
            self.file_path.write_text("{}")

    def _load_all(self):
        data=json.loads(self.file_path.read_text())

        transactions={}

        for account_id, history in data.items():
            transactions[int(account_id)] = [
                Transaction(
                    type=item["type"],
                    amount=item["amount"],
                    timestamp=datetime.fromisoformat(item["timestamp"])
                )
                for item in history
            ]
        return transactions

    def save(self, account_id, transaction):
        transactions=self._load_all()

        if account_id not in transactions:
            transactions[account_id] = []

        transactions[account_id].append(transaction)

        data={
            str(account_id):[
                {
                    **asdict(transaction),
                    "timestamp": transaction.timestamp.isoformat()
                }
                for transaction in history
            ]
            for account_id, history in transactions.items()
        }
        self.file_path.write_text(
            json.dumps(data, indent=2)
        )

    def get_by_account(self, account_id):
        transactions=self._load_all()
        return transactions.get(account_id, [])