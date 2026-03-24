# Python REST API Flask Inventory Management System

## Overview
Flask-based REST API for inventory CRUD operations with OpenFoodFacts API integration for product enrichment. Click-based CLI tool for API interaction. Comprehensive unit tests included. Web UI removed for lab focus on API/CLI.

## Quick Start
1. Install dependencies:
   ```
   pip install -r requirements.txt click pytest requests flask
   ```
   (Note: May need virtualenv on some systems)

2. Start Flask API server:
   ```
   python app.py
   ```
   Server runs at http://127.0.0.1:5000 (debug mode)

3. Use CLI:
   ```
   python cli.py --help
   python cli.py list                    # List inventory
   python cli.py add --name "Milk" --price 2.99 --stock 50
   python cli.py view seed1
   ```

4. Run tests:
   ```
   python -m pytest -v
   ```
   All 6 CLI tests pass ✓

## API Endpoints
All endpoints under `/inventory`:

| Method | Endpoint          | Description                  |
|--------|-------------------|------------------------------|
| GET    | `/`               | Health/Inventory list       |
| GET    | `/{id}`           | Get item by ID              |
| POST   | `/`               | Add item (enriches via API) |
| PATCH  | `/{id}`           | Update price/stock          |
| DELETE | `/{id}`           | Delete item                 |
| GET    | `/lookup/{query}` | External product lookup     |

**Add example** (curl):
```
curl -X POST http://127.0.0.1:5000/inventory \\
  -H 'Content-Type: application/json' \\
  -d '{\"product_name\":\"Milk\",\"price\":2.99,\"stock\":50,\"barcode\":\"3017620422003\"}'
```

## CLI Commands (Click-powered)
```
cli.py list                    # View all items
cli.py view <id>              # View by ID  
cli.py add --name NAME --price PRICE --stock STOCK [--barcode BC]
cli.py update <id> --stock N --price P
cli.py delete <id>
cli.py lookup <barcode>       # OpenFoodFacts lookup
```

## Architecture & Files
```
├── app.py              # Flask REST API (in-memory DB)
├── cli.py             # Click CLI client
├── models.py          # InventoryItem dataclass
├── api_utils.py       # OpenFoodFacts API integration
├── requirements.txt   # Dependencies
├── test_app.py        # API tests
├── test_cli.py        # CLI tests ✓
├── test_api_utils.py  # Utils tests
└── README.md
```

## Features
- ✅ RESTful CRUD API
- ✅ Click CLI (interactive/non-interactive)
- ✅ OpenFoodFacts product enrichment (barcode/name lookup)
- ✅ UUID generation, validation
- ✅ Pytest suite (mocks for external APIs)
- ✅ Error handling, JSON responses
- ✅ No web UI (API/CLI focus)

## Testing Status
```
$ python -m pytest -v
test_cli.py::test_list PASSED   [16%]
test_cli.py::test_view PASSED   [33%]
...  
6 passed in X.XXs
```

## Development Notes
- In-memory storage resets on restart
- Barcode lookup uses OpenFoodFacts.org
- Click CLI supports prompts for interactive use
- Tests mock requests, don't require server

## Deployment
Production: Use Gunicorn + PostgreSQL instead of in-memory + debug server.
