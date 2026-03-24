import requests

# Base URL for Flask API
BASE_URL = "http://127.0.0.1:5000"


def view_all():
    """Fetch and display all inventory items."""
    res = requests.get(f"{BASE_URL}/inventory")
    print(res.json())


def view_one():
    """Fetch a single item by ID."""
    item_id = input("ID: ")
    res = requests.get(f"{BASE_URL}/inventory/{item_id}")
    print(res.json())


def add_item():
    """Add a new inventory item via API."""
    data = {
        "product_name": input("Name: "),
        "price": int(input("Price: ")),
        "stock": int(input("Stock: ")),
        "barcode": input("Barcode: ")
    }

    res = requests.post(f"{BASE_URL}/inventory", json=data)
    print(res.json())


def update_item():
    """Update an existing inventory item."""
    item_id = input("ID: ")
    data = {
        "price": int(input("New Price: ")),
        "stock": int(input("New Stock: "))
    }

    res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
    print(res.json())


def delete_item():
    """Delete an inventory item."""
    item_id = input("ID: ")
    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(res.json())


def search_external():
    """Search product from external API using barcode."""
    barcode = input("Barcode: ")
    res = requests.get(f"{BASE_URL}/external-product?barcode={barcode}")
    print(res.json())


def menu():
    """CLI menu loop."""
    while True:
        print("\n1. View All")
        print("2. View One")
        print("3. Add")
        print("4. Update")
        print("5. Delete")
        print("6. Search API")
        print("7. Exit")

        choice = input("Choice: ")

        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_external()
        elif choice == "7":
            break


if __name__ == "__main__":
    menu()