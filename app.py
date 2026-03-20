from flask import Flask, request, jsonify
from models import InventoryItem
from api_utils import enrich_item_with_api
from typing import List, Dict, Any
import uuid

app = Flask(__name__)

# In-memory storage
inventory: List[Dict[str, Any]] = []

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/inventory/<item_id>', methods=['GET'])
def get_item(item_id: str):
    for item in inventory:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or not data.get('product_name'):
        return jsonify({'error': 'product_name required'}), 400
    
    # Enrich with API if possible
    enriched_data = enrich_item_with_api(data)
    enriched_data['id'] = str(uuid.uuid4())
    
    inventory.append(enriched_data)
    return jsonify(enriched_data), 201

@app.route('/inventory/<item_id>', methods=['PATCH'])
def update_item(item_id: str):
    for item in inventory:
        if item['id'] == item_id:
            data = request.get_json() or {}
            # Enrich again if new barcode/name
            if 'barcode' in data or 'product_name' in data:
                enrich_item_with_api(data)
            item.update(data)
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id: str):
    global inventory
    original_len = len(inventory)
    inventory = [item for item in inventory if item['id'] != item_id]
    if len(inventory) < original_len:
        return jsonify({'message': 'Item deleted'})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'inventory_count': len(inventory)})

if __name__ == '__main__':
    app.run(debug=True)

