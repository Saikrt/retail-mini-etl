# retail-mini-etl

A beginner-friendly Python ETL project for retail data processing.

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL Script
```bash
python src/etl.py
```

### 5. Run Tests
```bash
pytest tests/
```

## Project Structure
- `src/` - Source code
- `tests/` - Test files
- `data/raw/` - Raw input data (gitignored)
- `data/processed/` - Processed output data (gitignored)
- `db/` - Database files (gitignored)
- `docs/` - Documentation