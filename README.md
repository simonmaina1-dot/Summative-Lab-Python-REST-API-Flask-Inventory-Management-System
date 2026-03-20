# Python REST API Flask Inventory Management System

## Overview
Flask-based REST API for inventory CRUD with OpenFoodFacts API integration. CLI tool for interaction. Unit tests included.

## Installation & Setup
1. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\\Scripts\\activate on Windows
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run Flask app (debug mode):
   ```
   python app.py
   ```
   API available at http://127.0.0.1:5000

4. Run CLI:
   ```
   python cli.py --help
   ```

5. Run tests:
   ```
   pytest
   ```

## API Endpoints (RESTful)
- `GET /inventory` → List all items
- `GET /inventory/<id>` → Get item by ID
- `POST /inventory` → Add item (json: {"product_name": "...", "stock": 10, "price": 5.99, "barcode": "optional"})
  - Auto-enriches with OpenFoodFacts if barcode/name provided
- `PATCH /inventory/<id>` → Update item (json: {"stock": 20})
- `DELETE /inventory/<id>` → Delete item

Test with curl/Postman, e.g.:
```
curl -X POST http://127.0.0.1:5000/inventory -H "Content-Type: application/json" -d '{"product_name":"Test","stock":10,"price":5.99,"barcode":"3017620422003"}'
```

## CLI Commands
```
python cli.py list                    # View all
python cli.py view <id>               # View one
python cli.py add --name "Milk" --stock 50 --price 2.99 --barcode 123456
python cli.py update <id> --stock 40  # Update
python cli.py delete <id>             # Delete
python cli.py lookup 3017620422003    # API lookup
```

## Features
- In-memory storage (list of dicts)
- OpenFoodFacts integration for product details (brands, ingredients)
- Error handling, UUID IDs
- Pytest unit tests (API, CLI, API utils with mocks)

## Repository Structure
```
.
├── app.py              # Flask API
├── cli.py              # CLI tool
├── models.py           # Data models
├── api_utils.py        # OpenFoodFacts fetch
├── requirements.txt
├── README.md
├── TODO.md
├── test_*.py           # Tests
└── .gitignore
```

## Testing
All tests pass with `pytest`. Mocks used for external API.

Push to GitHub:
```
git init
git add .
git commit -m "Initial commit: Complete Inventory API"
git remote add origin <your-repo>
git push -u origin main
```

# Summative-Lab-Python-REST-API-Flask-Inventory-Management-System
