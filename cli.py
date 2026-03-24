import requests
import json
import sys

# Base URL for Flask API
BASE_URL = "http://127.0.0.1:5000"

def fetch_product(query):
    """Compatible with test_cli.py mock."""
    from api_utils import fetch_product
    return fetch_product(query)

def enrich_item_with_api(item_data):
    """Local enrich for tests - simplified."""
    from api_utils import enrich_item_with_api
    return enrich_item_with_api(item_data)

def do_list(args):
    """List command handler."""
    try:
        res = requests.get(f"{BASE_URL}/inventory")
        res.raise_for_status()
        items = res.json()
        if items:
            print(json.dumps(items, indent=2))
        else:
            print("No items found.")
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")

def do_view(args):
    """View command handler."""
    try:
        res = requests.get(f"{BASE_URL}/inventory/{args.item_id}")
        res.raise_for_status()
        print(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        print(f"Error: {e}")
        if 'res' in locals() and hasattr(res, 'status_code') and res.status_code == 404:
            print("Item not found.")

def do_add(args):
    """Add command handler."""
    data = {
        "product_name": args.name,
        "price": args.price,
        "stock": args.stock,
        "barcode": args.barcode or None
    }
    try:
        res = requests.post(f"{BASE_URL}/inventory", json=data)
        res.raise_for_status()
        print(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        print(f"Error: {e}")

def do_update(args):
    """Update command handler."""
    data = {}
    if args.price is not None:
        data["price"] = args.price
    if args.stock is not None:
        data["stock"] = args.stock
    if not data:
        print("Specify at least --price or --stock.")
        return
    try:
        res = requests.patch(f"{BASE_URL}/inventory/{args.item_id}", json=data)
        res.raise_for_status()
        print(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        print(f"Error: {e}")

def do_delete(args):
    """Delete command handler."""
    try:
        res = requests.delete(f"{BASE_URL}/inventory/{args.item_id}")
        res.raise_for_status()
        print(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        print(f"Error: {e}")

def do_lookup(args):
    """Lookup command handler."""
    try:
        product = fetch_product(args.barcode)
        if product:
            enriched = enrich_item_with_api({'product_name': product.get('product_name', args.barcode), 'barcode': args.barcode})
            print(json.dumps(enriched, indent=2))
        else:
            print("Product not found.")
    except Exception as e:
        print(f"Error: {e}")

def interactive_menu():
    """Interactive menu loop."""
    handlers = {
        'list': do_list,
        'view': do_view,
        'add': do_add,
        'update': do_update,
        'delete': do_delete,
        'lookup': do_lookup,
    }
    
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. List all items")
        print("2. View item by ID")
        print("3. Add new item")
        print("4. Update item by ID")
        print("5. Delete item by ID")
        print("6. Lookup product by barcode")
        print("0. Quit")
        
        choice = input("\nEnter choice (0-6): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            do_list(None)
        elif choice == '2':
            item_id = input("Enter item ID: ").strip()
            args = type('Args', (), {'item_id': item_id})()
            do_view(args)
        elif choice == '3':
            name = input("Product name: ").strip()
            price_str = input("Price: ").strip()
            stock_str = input("Stock quantity (default 0): ").strip() or '0'
            barcode = input("Barcode (optional): ").strip()
            try:
                price = float(price_str)
                stock = int(stock_str)
                args = type('Args', (), {'name': name, 'price': price, 'stock': stock, 'barcode': barcode or None})()
                do_add(args)
            except ValueError:
                print("Invalid number for price/stock.")
        elif choice == '4':
            item_id = input("Enter item ID: ").strip()
            print("Enter new values (leave blank to skip):")
            price_str = input("New price: ").strip()
            stock_str = input("New stock: ").strip()
            data_provided = False
            data = {}
            if price_str:
                data["price"] = float(price_str)
                data_provided = True
            if stock_str:
                data["stock"] = int(stock_str)
                data_provided = True
            if not data_provided:
                print("No changes specified.")
                continue
            args = type('Args', (), {'item_id': item_id, 'price': data.get('price'), 'stock': data.get('stock')})()
            do_update(args)
        elif choice == '5':
            item_id = input("Enter item ID: ").strip()
            confirm = input(f"Confirm delete {item_id}? (y/N): ").strip().lower()
            if confirm == 'y':
                args = type('Args', (), {'item_id': item_id})()
                do_delete(args)
            else:
                print("Delete cancelled.")
        elif choice == '6':
            barcode = input("Enter barcode: ").strip()
            args = type('Args', (), {'barcode': barcode})()
            do_lookup(args)
        else:
            print("Invalid choice. Try again.")

def main():
    interactive_menu()

if __name__ == "__main__":
    main()

