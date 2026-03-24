import argparse
import requests
import json
import sys
from io import StringIO
from contextlib import redirect_stdout

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
        if hasattr(res, 'status_code') and res.status_code == 404:
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


def create_parser():
    parser = argparse.ArgumentParser(description="Inventory Management CLI", add_help=True)
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # list
    subparsers.add_parser('list', help='View all inventory items')
    
    # view
    view_parser = subparsers.add_parser('view', help='View one item by ID')
    view_parser.add_argument('item_id', help='Item ID')
    
    # add
    add_parser = subparsers.add_parser('add', help='Add new inventory item')
    add_parser.add_argument('--name', '-n', required=True, help='Product name')
    add_parser.add_argument('--price', '-p', type=float, required=True, help='Price')
    add_parser.add_argument('--stock', '-s', type=int, default=0, help='Stock quantity')
    add_parser.add_argument('--barcode', '-b', default='', help='Barcode for API enrichment')
    
    # update
    update_parser = subparsers.add_parser('update', help='Update item by ID')
    update_parser.add_argument('item_id', help='Item ID')
    update_parser.add_argument('--price', '-p', type=float, help='New price')
    update_parser.add_argument('--stock', '-s', type=int, help='New stock')
    
    # delete
    delete_parser = subparsers.add_parser('delete', help='Delete item by ID')
    delete_parser.add_argument('item_id', help='Item ID')
    
    # lookup
    lookup_parser = subparsers.add_parser('lookup', help='Search external API by barcode')
    lookup_parser.add_argument('barcode', help='Barcode')
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    handlers = {
        'list': do_list,
        'view': do_view,
        'add': do_add,
        'update': do_update,
        'delete': do_delete,
        'lookup': do_lookup,
    }
    
    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()
