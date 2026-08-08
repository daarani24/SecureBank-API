from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Account:
    id: int
    customer_name: str
    balance: float=0.0

@dataclass
class Transaction:
    type: str
    amount: float
    timestamp: datetime=field(default_factory=datetime.now)