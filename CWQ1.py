import time
class Medicine:
    def __init__(self, medicine_id, name, item_type, price, quantity):
        self.medicine_id = medicine_id
        self.name = name
        self.item_type = item_type
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (
            f"ID: {self.medicine_id} | "
            f"Name: {self.name} | "
            f"Type: {self.item_type} | "
            f"Price: RM{self.price:.2f} | "
            f"Quantity: {self.quantity}"
        )


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.DELETED = "DELETED"

    def hash_func(self, key):
        return key % self.size

    def insert(self, medicine):
        index = self.hash_func(medicine.medicine_id)
        original_index = index

        while self.table[index] is not None and self.table[index] != self.DELETED:
            if self.table[index].medicine_id == medicine.medicine_id:
                print("Medicine ID already exists. Insert failed.")
                return False

            index = (index + 1) % self.size

            if index == original_index:
                print("Hash table is full. Insert failed.")
                return False

        self.table[index] = medicine
        print("Medicine inserted successfully at index", index)
        return True

    def search(self, medicine_id):
        index = self.hash_func(medicine_id)
        original_index = index

        while self.table[index] is not None:
            if self.table[index] != self.DELETED:
                if self.table[index].medicine_id == medicine_id:
                    print("Medicine found at index", index)
                    print(self.table[index])
                    return index

            index = (index + 1) % self.size

            if index == original_index:
                break

        print("Medicine not found.")
        return -1

    def search_silent(self, medicine_id):
        index = self.hash_func(medicine_id)
        original_index = index
        while self.table[index] is not None:
            if self.table[index] != self.DELETED:
                if self.table[index].medicine_id == medicine_id:
                    return index

            index = (index + 1) % self.size

            if index == original_index:
                break

        return -1

    def display(self):
        print("\n================ Pharmacy Hash Table ================")
        for i in range(self.size):
            if self.table[i] is None:
                print(i, ": Empty")
            elif self.table[i] == self.DELETED:
                print(i, ": Deleted")
            else:
                print(i, ":", self.table[i])
        print("=====================================================")

    def edit(self, medicine_id):
        index = self.search(medicine_id)

        if index != -1:
            print("\nEnter new medicine details")

            new_name = input("Enter new medicine name: ")
            new_price = float(input("Enter new price: RM"))
            new_quantity = int(input("Enter new quantity: "))

            self.table[index].name = new_name
            self.table[index].price = new_price
            self.table[index].quantity = new_quantity

            print("Medicine details updated successfully.")

    def delete(self, medicine_id):
        index = self.search(medicine_id)

        if index != -1:
            self.table[index] = self.DELETED
            print("Medicine deleted successfully.")


def insert_sample_data(hash_table):
    sample_medicines = [
        Medicine(101, "Paracetamol", "Tablet", 5.50, 100),
        Medicine(114, "Ibuprofen", "Tablet", 7.20, 80),
        Medicine(127, "Aspirin", "Tablet", 6.00, 75),
        Medicine(102, "Cetirizine", "Tablet", 4.80, 60),
        Medicine(115, "Loratadine", "Tablet", 8.50, 50),
        Medicine(128, "Metformin", "Tablet", 12.00, 40),
        Medicine(103, "Amoxicillin", "Tablet", 10.90, 30),
        Medicine(116, "Vitamin C", "Tablet", 9.90, 90)
    ]

    for medicine in sample_medicines:
        hash_table.insert(medicine)
    return sample_medicines

def array_search(medicine_list, medicine_id):
    for medicine in medicine_list:
        if medicine.medicine_id == medicine_id:
            return medicine
    return None

def performance_comparison(hash_table, medicine_list):
    search_ids = [101, 127, 116, 999, 130, 150]

    print("\n================ Search Performance Comparison ================")
    print("Search ID | Hash Table Time (ns) | Array Search Time (ns)")
    print("---------------------------------------------------------------")

    for medicine_id in search_ids:
        start_hash = time.perf_counter_ns()
        hash_table.search_silent(medicine_id)
        end_hash = time.perf_counter_ns()
        hash_time = end_hash - start_hash   

        start_array = time.perf_counter_ns()
        array_search(medicine_list, medicine_id)
        end_array = time.perf_counter_ns()
        array_time = end_array - start_array

        print(f"{medicine_id:<9} | {hash_time:<20} | {array_time:<20}")

    print("===============================================================")

def main():
    table_size = 13
    pharmacy_table = HashTable(table_size)

    print("Hash Table Size:", table_size)
    print("Welcome to Nanta's Pharmacy Inventory System")

    medicine_list = insert_sample_data(pharmacy_table)

    while True:
        print("\n========== Pharmacy Inventory System ==========")
        print("1. Display all medicines")
        print("2. Insert new medicine")
        print("3. Search medicine")
        print("4. Edit medicine")
        print("5. Delete medicine")
        print("6. Performance Comparison")
        print("7. Exit")
        print("===============================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            pharmacy_table.display()

        elif choice == "2":
            medicine_id = int(input("Enter medicine ID: "))
            name = input("Enter medicine name: ")
            item_type = "Tablet"
            price = float(input("Enter price: RM"))
            quantity = int(input("Enter quantity: "))

            new_medicine = Medicine(medicine_id, name, item_type, price, quantity)
            if pharmacy_table.insert(new_medicine):
                medicine_list.append(new_medicine)

        elif choice == "3":
            medicine_id = int(input("Enter medicine ID to search: "))
            pharmacy_table.search(medicine_id)

        elif choice == "4":
            medicine_id = int(input("Enter medicine ID to edit: "))
            pharmacy_table.edit(medicine_id)

        elif choice == "5":
            medicine_id = int(input("Enter medicine ID to delete: "))
            pharmacy_table.delete(medicine_id)
            for medicine in medicine_list:
                if medicine.medicine_id == medicine_id:
                    medicine_list.remove(medicine)
                    break

        elif choice == "6":
            performance_comparison(pharmacy_table, medicine_list)

        elif choice == "7":
            print("Exiting Pharmacy Inventory System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()