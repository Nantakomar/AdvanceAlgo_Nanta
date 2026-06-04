import time


class Transaction:
    def __init__(self, transaction_id, customer_name, product_name, amount, transaction_date):
        self.transaction_id = transaction_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.amount = amount
        self.transaction_date = transaction_date

    def __str__(self):
        return (
            f"ID: {self.transaction_id} | "
            f"Customer: {self.customer_name} | "
            f"Product: {self.product_name} | "
            f"Amount: RM{self.amount:.2f} | "
            f"Date: {self.transaction_date}"
        )


def load_sample_transactions():
    # Dataset is intentionally unsorted to show Merge Sort clearly.
    return [
        Transaction(108, "Aiman", "Wireless Mouse", 59.90, "2026-04-03"),
        Transaction(103, "Mei Ling", "Keyboard", 120.00, "2026-04-01"),
        Transaction(115, "Daniel", "Monitor", 699.00, "2026-04-07"),
        Transaction(101, "Sofia", "USB Cable", 15.50, "2026-03-28"),
        Transaction(112, "Arjun", "Laptop Stand", 88.00, "2026-04-06"),
        Transaction(106, "Hannah", "Webcam", 149.90, "2026-04-02"),
        Transaction(119, "Jason", "External SSD", 399.00, "2026-04-10"),
        Transaction(104, "Nurul", "Headset", 89.90, "2026-04-01"),
        Transaction(110, "Kevin", "Power Bank", 79.00, "2026-04-05"),
        Transaction(117, "Priya", "Smartwatch", 299.00, "2026-04-08"),
        Transaction(102, "Amir", "Phone Charger", 45.00, "2026-03-30"),
        Transaction(113, "Chloe", "Tablet Case", 39.90, "2026-04-06")
    ]


def display_transactions(transactions, title="Transaction Records"):
    print("\n================", title, "================")
    if len(transactions) == 0:
        print("No transaction records available.")
    else:
        for transaction in transactions:
            print(transaction)
    print("=" * 60)


def merge_sort(transactions, stats=None):
    if stats is not None:
        stats["recursive_calls"] += 1

    # Base case: an array with 0 or 1 item is already sorted.
    if len(transactions) <= 1:
        return transactions

    # DIVIDE STEP:
    # Split the transaction list into two smaller halves.
    mid = len(transactions) // 2
    left_half = transactions[:mid]
    right_half = transactions[mid:]

    # CONQUER STEP:
    # Recursively sort both halves.
    sorted_left = merge_sort(left_half, stats)
    sorted_right = merge_sort(right_half, stats)

    # COMBINE STEP:
    # Merge the two sorted halves into one sorted list.
    return merge(sorted_left, sorted_right)


def merge(left, right):
    sorted_transactions = []
    i = 0
    j = 0

    # Compare transaction_id from both halves and add the smaller one first.
    while i < len(left) and j < len(right):
        if left[i].transaction_id <= right[j].transaction_id:
            sorted_transactions.append(left[i])
            i += 1
        else:
            sorted_transactions.append(right[j])
            j += 1

    # Add any remaining records after one side becomes empty.
    while i < len(left):
        sorted_transactions.append(left[i])
        i += 1

    while j < len(right):
        sorted_transactions.append(right[j])
        j += 1

    return sorted_transactions


def binary_search(transactions, target_id, low, high, stats=None):
    if stats is not None:
        stats["recursive_calls"] += 1

    # Base case: target is not found.
    if low > high:
        return -1

    # DIVIDE STEP:
    # Find the middle index of the current search range.
    mid = (low + high) // 2

    # CONQUER STEP:
    # Compare the middle transaction with the target ID.
    if transactions[mid].transaction_id == target_id:
        return mid
    elif target_id < transactions[mid].transaction_id:
        # Search the left half.
        return binary_search(transactions, target_id, low, mid - 1, stats)
    else:
        # Search the right half.
        return binary_search(transactions, target_id, mid + 1, high, stats)


def linear_search(transactions, target_id):
    for i in range(len(transactions)):
        if transactions[i].transaction_id == target_id:
            return i
    return -1


def search_existing_and_non_existing(sorted_transactions):
    test_ids = [106, 999]

    print("\n========== Binary Search Test ==========")

    for target_id in test_ids:
        stats = {"recursive_calls": 0}

        index = binary_search(
            sorted_transactions,
            target_id,
            0,
            len(sorted_transactions) - 1,
            stats
        )

        if index != -1:
            print(f"Transaction ID {target_id} found:")
            print(sorted_transactions[index])
        else:
            print(f"Transaction ID {target_id} was not found.")

        print(f"Binary Search recursive calls: {stats['recursive_calls']}")
        print("----------------------------------------")


def performance_comparison(transactions):
    print("\n========== Performance Comparison ==========")

    # Measure Merge Sort time.
    merge_stats = {"recursive_calls": 0}

    start_sort = time.perf_counter_ns()
    sorted_transactions = merge_sort(transactions.copy(), merge_stats)
    end_sort = time.perf_counter_ns()

    merge_sort_time = end_sort - start_sort

    # Measure Binary Search time using a sorted list.
    target_id = 106
    binary_stats = {"recursive_calls": 0}

    start_binary = time.perf_counter_ns()
    binary_index = binary_search(
        sorted_transactions,
        target_id,
        0,
        len(sorted_transactions) - 1,
        binary_stats
    )
    end_binary = time.perf_counter_ns()

    binary_search_time = end_binary - start_binary

    # Measure Linear Search time for comparison.
    start_linear = time.perf_counter_ns()
    linear_index = linear_search(transactions, target_id)
    end_linear = time.perf_counter_ns()

    linear_search_time = end_linear - start_linear

    print(f"Merge Sort Time: {merge_sort_time} ns")
    print(f"Merge Sort Recursive Calls: {merge_stats['recursive_calls']}")
    print(f"Binary Search Time for ID {target_id}: {binary_search_time} ns")
    print(f"Binary Search Recursive Calls: {binary_stats['recursive_calls']}")
    print(f"Linear Search Time for ID {target_id}: {linear_search_time} ns")

    print("\nSearch Result Check:")
    if binary_index != -1:
        print("Binary Search found:", sorted_transactions[binary_index])
    else:
        print("Binary Search did not find the transaction.")

    if linear_index != -1:
        print("Linear Search found:", transactions[linear_index])
    else:
        print("Linear Search did not find the transaction.")


def display_complexity_table():
    print("\n================ Time Complexity Table ================")
    print("Algorithm       | Best Case      | Average Case   | Worst Case")
    print("-------------------------------------------------------")
    print("Merge Sort      | O(n log n)     | O(n log n)     | O(n log n)")
    print("Binary Search   | O(1)           | O(log n)       | O(log n)")
    print("Linear Search   | O(1)           | O(n)           | O(n)")
    print("=======================================================")


def insert_transaction(transactions):
    try:
        transaction_id = int(input("Enter transaction ID: "))
        customer_name = input("Enter customer name: ")
        product_name = input("Enter product name: ")
        amount = float(input("Enter amount: RM"))
        transaction_date = input("Enter transaction date (YYYY-MM-DD): ")

        new_transaction = Transaction(
            transaction_id,
            customer_name,
            product_name,
            amount,
            transaction_date
        )

        transactions.append(new_transaction)
        print("Transaction inserted successfully.")
        print("Note: Please sort again before using Binary Search.")

    except ValueError:
        print("Invalid input. Transaction ID must be integer and amount must be number.")


def main():
    transactions = load_sample_transactions()
    sorted_transactions = []
    is_sorted = False

    while True:
        print("\n========== Customer Transaction System ==========")
        print("1. Display all transactions")
        print("2. Sort transactions using Merge Sort")
        print("3. Search transaction using Binary Search")
        print("4. Search transaction using Linear Search")
        print("5. Test Binary Search with existing and non-existing IDs")
        print("6. Performance Comparison")
        print("7. Insert new transaction")
        print("8. Display time complexity table")
        print("9. Exit")
        print("=================================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_transactions(transactions, "Current Transaction Records")

        elif choice == "2":
            print("\nBefore Sorting:")
            display_transactions(transactions, "Before Merge Sort")

            stats = {"recursive_calls": 0}
            sorted_transactions = merge_sort(transactions.copy(), stats)
            transactions = sorted_transactions.copy()
            is_sorted = True

            print("\nAfter Sorting by Transaction ID:")
            display_transactions(sorted_transactions, "After Merge Sort")
            print("Merge Sort recursive calls:", stats["recursive_calls"])

        elif choice == "3":
            if not is_sorted:
                print("Binary Search requires sorted data.")
                print("Sorting the transactions using Merge Sort first...")
                stats = {"recursive_calls": 0}
                sorted_transactions = merge_sort(transactions.copy(), stats)
                transactions = sorted_transactions.copy()
                is_sorted = True

            try:
                target_id = int(input("Enter transaction ID to search using Binary Search: "))
                stats = {"recursive_calls": 0}

                index = binary_search(
                    sorted_transactions,
                    target_id,
                    0,
                    len(sorted_transactions) - 1,
                    stats
                )

                if index != -1:
                    print("Transaction found:")
                    print(sorted_transactions[index])
                else:
                    print("Transaction not found.")

                print("Binary Search recursive calls:", stats["recursive_calls"])

            except ValueError:
                print("Invalid input. Please enter a numeric transaction ID.")

        elif choice == "4":
            try:
                target_id = int(input("Enter transaction ID to search using Linear Search: "))
                index = linear_search(transactions, target_id)

                if index != -1:
                    print("Transaction found:")
                    print(transactions[index])
                else:
                    print("Transaction not found.")

            except ValueError:
                print("Invalid input. Please enter a numeric transaction ID.")

        elif choice == "5":
            if not is_sorted:
                stats = {"recursive_calls": 0}
                sorted_transactions = merge_sort(transactions.copy(), stats)
                transactions = sorted_transactions.copy()
                is_sorted = True

            search_existing_and_non_existing(sorted_transactions)

        elif choice == "6":
            performance_comparison(transactions)

        elif choice == "7":
            insert_transaction(transactions)
            is_sorted = False

        elif choice == "8":
            display_complexity_table()

        elif choice == "9":
            print("Exiting Customer Transaction System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()