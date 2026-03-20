import requests
from typing import Optional, Dict, Any
from models import InventoryItem

def fetch_product(query: str) -> Optional[Dict[str, Any]]:
    """
    Fetch product details from OpenFoodFacts API by barcode or product name search.
    """
    # First try as barcode
    barcode_url = f"https://world.openfoodfacts.org/api/v0/product/{query}.json"
    try:
        response = requests.get(barcode_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1 and data.get('product'):
                return data['product']
    except requests.RequestException:
        pass

    # Fallback to product name search
    search_url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 1
    }
    try:
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            if products:
                return products[0]
    except requests.RequestException:
        pass

    return None

def enrich_item_with_api(item_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich item data with API info if barcode or name provided.
    """
    barcode = item_data.get('barcode')
    name = item_data.get('product_name')
    query = barcode or name
    if query:
        api_data = fetch_product(query)
        if api_data:
            item_data['brands'] = api_data.get('brands')
            item_data['ingredients_text'] = api_data.get('ingredients_text')
    return item_data

