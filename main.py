from cli import run_cli
from services.bank_ledger import BankLedger
from repositories.json_account_repository import JsonAccountRepository

if __name__=="__main__":
    repository=JsonAccountRepository()
    ledger=BankLedger(repository=repository)
    run_cli(ledger)