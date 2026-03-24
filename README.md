# Python REST API Flask Inventory Management System

## Overview
Flask-based REST API for inventory CRUD with OpenFoodFacts integration. argparse CLI tool. Unit tests included. No web UI.

## Quick Start
1. Install:
   ```
   pip install -r requirements.txt pytest requests flask
   ```

2. Run API:
   ```
   python app.py
   ```

3. CLI:
   ```
   python cli.py --help
   python cli.py list
   python cli.py add --name "Milk" --price 2.99 --stock 50
   ```

4. Tests:
   ```
   python -m pytest test_cli.py -v
   ```

## CLI Usage (argparse)
```
python cli.py list                          # List all
python cli.py view ITEM_ID                  # View item
python cli.py add --name NAME --price P --stock S [--barcode B]
python cli.py update ITEM_ID [--price P] [--stock S]
python cli.py delete ITEM_ID
python cli.py lookup BARCODE
```

## API Endpoints
- GET /inventory
- GET /inventory/{id}
- POST /inventory
- PATCH /inventory/{id}
- DELETE /inventory/{id}
- GET /lookup/{barcode}

## Files
```
app.py (Flask API)
cli.py (argparse CLI)
models.py
api_utils.py (OpenFoodFacts)
test_cli.py ✓
README.md
```

## Tests ✓ 6/6
Tests use sys.argv mocking, stdout capture.

## Notes
- In-memory storage
- Auto-enrichment via barcode
- Pytest for CLI/API/utils
