import click
import requests
import json

# Base URL for Flask API
BASE_URL = "http://127.0.0.1:5000"


@click.group()
def cli():
    """Inventory Management CLI"""
    pass


@cli.command()
def list():
    """View all inventory items."""
    try:
        res = requests.get(f"{BASE_URL}/inventory")
        res.raise_for_status()
        items = res.json()
        if items:
            click.echo(json.dumps(items, indent=2))
        else:
            click.echo("No items found.")
    except requests.RequestException as e:
        click.echo(f"Error connecting to API: {e}")


@cli.command()
@click.argument('item_id')
def view(item_id):
    """View one item by ID."""
    try:
        res = requests.get(f"{BASE_URL}/inventory/{item_id}")
        res.raise_for_status()
        click.echo(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        click.echo(f"Error: {e}")
        if res.status_code == 404:
            click.echo("Item not found.")


@cli.command()
@click.option('--name', '-n', required=True, prompt='Product Name')
@click.option('--price', '-p', required=True, type=float, prompt='Price')
@click.option('--stock', '-s', required=True, type=int, default=0, prompt='Stock')
@click.option('--barcode', '-b', default='')
def add(name, price, stock, barcode):
    """Add new inventory item."""
    data = {
        "product_name": name,
        "price": price,
        "stock": stock,
        "barcode": barcode or None
    }
    try:
        res = requests.post(f"{BASE_URL}/inventory", json=data)
        res.raise_for_status()
        click.echo(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument('item_id')
@click.option('--price', '-p', type=float)
@click.option('--stock', '-s', type=int)
def update(item_id, price, stock):
    """Update item by ID."""
    data = {}
    if price is not None:
        data["price"] = price
    if stock is not None:
        data["stock"] = stock
    if not data:
        click.echo("Specify at least --price or --stock.")
        return
    try:
        res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
        res.raise_for_status()
        click.echo(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument('item_id')
def delete(item_id):
    """Delete item by ID."""
    try:
        res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        res.raise_for_status()
        click.echo(json.dumps(res.json(), indent=2))
    except requests.RequestException as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument('barcode')
def lookup(barcode):
    """Search product from external API using barcode."""
    try:
        product = fetch_product(barcode)
        if product:
            enriched = enrich_item_with_api({'product_name': product.get('product_name', barcode), 'barcode': barcode})
            click.echo(json.dumps(enriched, indent=2))
        else:
            click.echo("Product not found.")
    except Exception as e:
        click.echo(f"Error: {e}")

def enrich_item_with_api(item_data):
    """Local enrich for tests - simplified."""
    from api_utils import enrich_item_with_api
    return enrich_item_with_api(item_data)


def fetch_product(query):
    """Compatible with test_cli.py mock."""
    from api_utils import fetch_product
    return fetch_product(query)


if __name__ == "__main__":
    cli()
