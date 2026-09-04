from cli import run_cli
from services.bank_ledger import BankLedger
from repositories.json_account_repository import JsonAccountRepository
from repositories.json_transaction_repository import JsonTransactionRepository

if __name__=="__main__":
    account_repository=JsonAccountRepository()
    transaction_repository=JsonTransactionRepository()

    ledger=BankLedger(
        repository=account_repository,
        transaction_repository=transaction_repository
    )
    run_cli(ledger)