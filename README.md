# Python REST API Flask Inventory Management System

## Overview
Flask-based REST API for inventory CRUD with OpenFoodFacts integration. Interactive menu CLI. Unit tests included. Web UI available.

## Quick Start
1. Install:
   ```
   pip install -r requirements.txt
   ```

2. Run API:
   ```
   python app.py
   ```
   Open http://127.0.0.1:5000

3. Interactive CLI:
   ```
   python cli.py
   ```
   Choose 1-6 from menu.

4. Tests:
   ```
   pytest test_cli.py -v
   ```

## CLI Menu (Interactive)
```
1. List all items
2. View item by ID     → prompt ID
3. Add new item        → prompts name, price, stock, barcode
4. Update item by ID   → prompt ID, optional price/stock
5. Delete item by ID   → prompt ID, confirm
6. Lookup product by barcode (no server needed)
0. Quit
```
CLI connects to running API. Lookup uses OpenFoodFacts.

## API Endpoints
- GET /inventory
- GET /inventory/{id}
- POST /inventory
- PATCH /inventory/{id}
- DELETE /inventory/{id}
- GET /lookup/{barcode}
- / (web UI)

## Files
```
app.py (Flask API + UI)
cli.py (interactive CLI)
models.py
api_utils.py (OpenFoodFacts)
test_cli.py ✓
```

## Tests ✓ 7/7
Tests mock API calls and input for handlers/menu.

## Notes
- In-memory storage (resets on restart)
- Auto-enrich via barcode (OpenFoodFacts)
- Pytest for CLI handlers

