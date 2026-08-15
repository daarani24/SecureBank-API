import bisect
from sortedcontainers import SortedDict

def accounts_sorted_by_id_bisect(accounts):
    sorted_ids=[]
    for acc_id in accounts:
        bisect.insort(sorted_ids, acc_id)
    return [accounts[i] for i in sorted_ids]

def accounts_sorted_by_id_sorteddict(accounts):
    sd=SortedDict()
    for acc_id, acc in accounts.items():
        sd[acc_id]=acc
    return list(sd.values())

def accounts_sorted_by_balance(accounts):
    sd=SortedDict()
    for acc in accounts.values():
        sd.setdefault(acc.balance, []).append(acc)

    result=[]
    for group in sd.values():
        result.extend(group)
    return result