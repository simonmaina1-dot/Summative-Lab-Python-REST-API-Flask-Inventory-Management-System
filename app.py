from flask import Flask, request, jsonify, render_template_string
from api_utils import enrich_item_with_api, fetch_product
from models import InventoryItem
from typing import List
import uuid

app = Flask(__name__)

# In-memory storage
inventory: List[InventoryItem] = [
    InventoryItem(
        id="seed1",
        product_name="Sample Milk",
        brands="Organic Dairy",
        stock=50,
        price=2.99,
        barcode="3017620422003"
    )
]

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify([item.to_dict() for item in inventory])

@app.route('/inventory/<item_id>', methods=['GET'])
def get_item(item_id: str):
    for item in inventory:
        if item.id == item_id:
            return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or not data.get('product_name'):
        return jsonify({'error': 'product_name required'}), 400
    
    # Enrich with API if possible
    enriched_dict = enrich_item_with_api(data)
    item = InventoryItem.from_dict(enriched_dict)
    
    inventory.append(item)
    return jsonify(item.to_dict()), 201

@app.route('/inventory/<item_id>', methods=['PATCH'])
def update_item(item_id: str):
    data = request.get_json() or {}
    for item in inventory:
        if item.id == item_id:
            # Merge data
            update_dict = {**item.to_dict(), **data}
            # Enrich if new barcode/name
            if 'barcode' in data or 'product_name' in data:
                enrich_item_with_api(update_dict)
            updated_item = InventoryItem.from_dict(update_dict)
            # Replace in list (by index)
            idx = inventory.index(item)
            inventory[idx] = updated_item
            return jsonify(updated_item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id: str):
    global inventory
    original_len = len(inventory)
    inventory = [item for item in inventory if item.id != item_id]
    if len(inventory) < original_len:
        return jsonify({'message': 'Item deleted'})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'inventory_count': len(inventory)})

@app.route('/lookup/<query>', methods=['GET'])
def lookup_api(query: str):
    from api_utils import fetch_product
    product = fetch_product(query)
    if product:
        enriched = enrich_item_with_api({'product_name': product.get('product_name', query), 'barcode': query})
        return jsonify(enriched)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/', methods=['GET'])
def index():
    return '''
<!DOCTYPE html>
<html><head><title>Inventory</title>
<link rel="stylesheet" href="/static/style.css">
</head><body>
<h1>Inventory Management</h1>
<form id="lookupForm">
<input type="text" id="query" placeholder="Barcode or name" required>
<button type="submit">Lookup & Add</button>
</form>
<div id="preview"></div>
<h2>Current Inventory</h2><ul id="inventory"></ul>
<script>
fetch("/inventory").then(r=>r.json()).then(items=>{
const ul=document.getElementById("inventory");
items.forEach(item=>{
const li=document.createElement("li");
li.textContent=item.product_name+" (ID: "+item.id+", Stock: "+item.stock+", Price: $"+item.price+")";
ul.appendChild(li);});});
document.getElementById("lookupForm").onsubmit=async(e)=>{
e.preventDefault();
const query=document.getElementById("query").value;
const res=await fetch("/lookup/"+encodeURIComponent(query));
const preview=document.getElementById("preview");
if(res.ok){
const data=await res.json();
preview.innerHTML="<h3>Preview: "+(data.product_name||"Unknown")+" - Brands: "+(data.brands||"N/A")+"</h3><p>Stock: <input id=\\'stock\\' value=\\'0\\' type=\\'number\\' min=\\'0\\'> Price: <input id=\\'price\\' value=\\'"+(data.price||0)+"\\' type=\\'number\\' step=\\'0.01\\' min=\\'0\\'></p><button onclick=\\'addItem(\\""+(data.product_name||query)+"\\", \\""+(data.barcode||"")+"\\")\\'>Add to Inventory</button>";
}else{preview.innerHTML="<p>Product not found</p>";}});
function addItem(name, barcode){
const stockVal=document.getElementById("stock").value;
const priceVal=document.getElementById("price").value;
fetch("/inventory",{method:"POST",headers:{"Content-Type":"application/json"},
body:JSON.stringify({product_name:name,barcode:barcode,stock:parseInt(stockVal),price:parseFloat(priceVal)})})
.then(r=>{if(r.ok)location.reload();});}
</script>
</body></html>'''

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

