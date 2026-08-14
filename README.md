# SecureBank API

A Python backend project built week by week — starts as an in-memory
console app and evolves into a secured, production-style FastAPI service.

## Structure
- models/ - data classes
- services/ - business logic (BankLedger)
- exceptions/ - custom exceptions
- utils/ - input validators
- cli.py - user interaction and printing only
- main.py - entry point

## Progress

### Week 1 - Account Fundamentals ✅
- Create account
- Deposit funds
- Withdraw funds
- Check balance
- Close account
- In-memory account storage using `dict[int, Account]`
- `Account` implemented using `@dataclass`
- Custom exception handling
- Working CLI application

### Week 2 - Transfers, Reversals & Customer Indexing ✅
- Transfer money between accounts
- Atomic transfer with manual rollback
- Transaction tracking using `Transaction` dataclass
- Reverse the last transaction
- Customer-name secondary index using `defaultdict(list)`
- Find all accounts belonging to a customer
- CLI support for transfer, reversal, and customer lookup
- Invalid operations handled without crashing

## Run
python main.py
