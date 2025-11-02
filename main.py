import csv
transactions = []

with open('transactions.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        cleaned = [item.strip() for item in row if item.strip()]
        transactions.append(cleaned)

print(f"Total transactions: {len(transactions)}")

if len(transactions) <= 20:
    num_blocks = 2
elif len(transactions) >= 50:
    num_blocks = 5
else:
    num_blocks = 10

block_size = len(transactions) // num_blocks
remainder = len(transactions) % num_blocks

blocks = []
start = 0
for i in range(num_blocks):
    end = start + block_size
    if i == num_blocks - 1:
        end += remainder
    blocks.append(transactions[start:end])
    start = end

print(f"\nTransactions divided into {num_blocks} blocks:")
for i, block in enumerate(blocks, 1):
    print(f"Block number {i} contains {len(block)} transactions")


if len(transactions) <= 20:
    minsupport = 2
elif len(transactions) <= 80:
    minsupport = int(0.2 * len(transactions))
else:
    minsupport = int(0.1 * len(transactions))

print(f"\nThe minsupport is  {minsupport}")

all_items = set()
for t in transactions:
    for item in t:
        all_items.add(item)

counts = {}
status = {}

for item in all_items:
    itemset = frozenset([item])
    counts[itemset] = 0
    status[itemset] = "open"


#نبدا
for b_index, block in enumerate(blocks, 1):
    for transaction in block:
        itemSet = set(transaction)
        for item in list(counts.keys()):
            if status[item] == "open" and item.issubset(itemSet):
                counts[item] += 1

    # بعد كل بلوك نحدّث الحالات
    The_remaining_blocks = num_blocks - b_index
    Thepossible = The_remaining_blocks * block_size

    for itemset in list(counts.keys()):
        c = counts[itemset]
        if c >= minsupport:
            status[itemset] = "solid"
        elif c + Thepossible < minsupport:
            status[itemset] = "pruned"
        else:
            status[itemset] = "open"

    solid_sets = [iset for iset, s in status.items() if s == "solid"]
    new_candidates = []
    for i in range(len(solid_sets)):
        for j in range(i + 1, len(solid_sets)):
            union = solid_sets[i].union(solid_sets[j])
            if len(union) == len(solid_sets[i]) + 1:  # توليد k+1 itemset
                new_candidates.append(union)

    for cand in new_candidates:
        if cand not in counts:
            counts[cand] = 0
            status[cand] = "open"


for transaction in transactions:
    tset = set(transaction)
    for itemset, s in status.items():
        if s == "open" and itemset.issubset(tset):
            counts[itemset] += 1

for itemset in list(counts.keys()):
    if counts[itemset] >= minsupport:
        status[itemset] = "solid"
    else:
        status[itemset] = "pruned"


print("\nThe frequent items are:")
for itemset, s in status.items():
    if s == "solid":
        print(f"{set(itemset)} with support equals {counts[itemset]}")


