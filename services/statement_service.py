import bisect
import timeit
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

def build_statement_index(transactions):
    sd=SortedDict()
    for i,t in enumerate(transactions):
        sd[(t.timestamp, i)]=t
    return sd

def get_statement(transactions,start_date, end_date):
    sd=build_statement_index(transactions)
    start=(start_date, 0)
    end=(end_date, float("inf"))
    return [sd[k] for k in sd.irange(start, end)]

def benchmark_insert_speed(count:int=5000):
    def bisect_insert():
        data=[]
        for i in range(count):
            bisect.insort(data, i)
    def sorteddict_insert():
        sd=SortedDict()
        for i in range(count):
            sd[i]=True

    bisect_time=timeit.timeit(bisect_insert, number=1)
    sorteddict_time=timeit.timeit(sorteddict_insert, number=1)

    return(
        f"Inserting {count} items:\n"
        f"bisect.insert : {bisect_time:.4f} sec\n"
        f"SortedDict    : {sorteddict_time:.4f} sec"
    )