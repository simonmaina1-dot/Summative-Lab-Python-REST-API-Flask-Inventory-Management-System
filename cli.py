import click
import requests
import uuid
from api_utils import fetch_product

BASE_URL = 'http://127.0.0.1:5000'

@click.group()
def cli():
    pass

@cli.command()
def list():
    """List all inventory items."""
    response = requests.get(f'{BASE_URL}/inventory')
    click.echo(response.json())

@cli.command()
@click.argument('item_id')
def view(item_id):
    """View a single item by ID."""
    response = requests.get(f'{BASE_URL}/inventory/{item_id}')
    click.echo(response.json())

@cli.command()
@click.option('--barcode', help='Barcode to fetch from API')
@click.option('--name', help='Product name')
@click.option('--stock', type=int, default=0)
@click.option('--price', type=float, default=0.0)
def add(barcode, name, stock, price):
    """Add new inventory item."""
    if not name and not barcode:
        click.echo('Provide --name or --barcode')
        return
    data = {'product_name': name or 'Unknown', 'stock': stock, 'price': price, 'barcode': barcode}
    response = requests.post(f'{BASE_URL}/inventory', json=data)
    click.echo(response.json())

@cli.command()
@click.argument('item_id')
@click.option('--stock')
@click.option('--price')
def update(item_id, stock, price):
    """Update item stock or price."""
    data = {}
    if stock is not None:
        data['stock'] = stock
    if price is not None:
        data['price'] = price
    if not data:
        click.echo('Provide --stock or --price')
        return
    response = requests.patch(f'{BASE_URL}/inventory/{item_id}', json=data)
    click.echo(response.json())

@cli.command()
@click.argument('item_id')
def delete(item_id):
    """Delete item by ID."""
    response = requests.delete(f'{BASE_URL}/inventory/{item_id}')
    click.echo(response.json())

@cli.command()
@click.argument('query')
def lookup(query):
    """Lookup product on OpenFoodFacts API."""
    product = fetch_product(query)
    if product:
        click.echo(product)
    else:
        click.echo('Product not found')

if __name__ == '__main__':
    cli()

