from exceptions.bank_exceptions import InvalidAmountError, InvalidNameError

def validate_amount(amount):
    if amount<=0:
        raise InvalidAmountError("Amount must be greater than zero")

def validate_customer_name(name):
    name=name.strip()
    if not name:
        raise InvalidNameError("Customer name cannot be empty")
    if len(name)<2:
        raise InvalidNameError("Customer name must be at least 2 characters")
    if len(name)>50:
        raise InvalidNameError("Customer name must be under 50 characters")
    return name
