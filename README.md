# Avito Parser

This project provides simple utilities for parsing apartment listings on [Avito](https://www.avito.ru) and exporting the collected information to Excel.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the interactive parser:

```bash
python main.py
```

You will be prompted for an Avito advertisement URL. Parsed data will be saved to `output/apartments.xlsx`.

## Testing

Tests are located in the `tests/` directory and can be executed with:

```bash
python -m pytest -q
```
