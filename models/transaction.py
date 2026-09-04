from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Transaction:
    type: str
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)