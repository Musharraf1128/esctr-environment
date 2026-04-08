---
title: Invoice Extraction Environment
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
tags:
  - openenv
---

# Invoice Extraction Environment

An OpenEnv-compliant environment where AI agents extract structured data from unstructured invoice and receipt documents.

**Space URL:** `https://huggingface.co/spaces/musharraf7/invoice-extraction-env`

```python
import requests

# Connect to the environment
url = "https://musharraf7-invoice-extraction-env.hf.space"
r = requests.post(f"{url}/reset", json={"task_name": "simple_invoice"})
print(r.json())
```

## Environment Description

This environment simulates real-world document data extraction — a task faced daily by businesses processing invoices, receipts, and purchase orders. The agent receives unstructured text documents and must extract specific structured fields (invoice numbers, dates, vendor names, line items, totals, etc.).

### Why This Matters
- **$5B+ industry:** Automated document processing is one of the largest business process automation markets
- **Real RL training signal:** Partial-credit rewards on a per-field basis provide rich gradient
- **Difficulty progression:** Three task levels test increasingly complex reasoning

## Action Space

The agent sends an `InvoiceAction` with a `command` and optional `payload`:

| Command | Description | Payload |
|---------|-------------|---------|
| `view_document` | View the raw document text | — |
| `view_fields` | See required fields with descriptions | — |
| `extract` | Submit extracted fields | JSON string |
| `get_feedback` | Get detailed per-field feedback | — |

### Action Schema
```json
{
  "command": "extract",
  "payload": "{\"invoice_number\": \"INV-2024-001\", \"date\": \"2024-01-15\", ...}"
}
```

## Observation Space

Each step returns an `InvoiceObservation`:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Response text from the environment |
| `task_name` | string | Current task name |
| `current_score` | float | Best score achieved so far |
| `attempts_remaining` | int | Remaining extraction attempts |
| `required_fields` | list | Fields to extract |
| `done` | bool | Whether the episode has ended |
| `reward` | float | Reward signal [0.0–1.0] |

## Tasks

### 1. `simple_invoice` (Easy)
Clean, well-formatted invoices with clear field labels. The agent must extract 8 fields including invoice number, date, vendor/customer names, financial totals, and itemized line items.

**Required fields:** `invoice_number`, `date`, `vendor_name`, `customer_name`, `subtotal`, `tax`, `total`, `line_items`

### 2. `messy_invoice` (Medium)
Same fields but from messy, inconsistently formatted documents with abbreviations, typos, and non-standard layouts.

**Required fields:** Same as simple_invoice

### 3. `multi_document` (Hard)
Complex multi-section documents containing a purchase order, invoice, and credit memo/payment receipt. The agent must cross-reference sections and extract 11 fields including the adjusted total.

**Required fields:** All of the above + `po_number`, `adjustment_reason`, `adjusted_total`

## Reward Design

- **Per-field scoring:** Each field is scored independently (0.0–1.0)
  - Text fields: Fuzzy matching with SequenceMatcher
  - Numeric fields: Exact match (1.0), within 1% (0.9), within 5% (0.5)
  - Date fields: Normalized comparison (YYYY-MM-DD)
  - Line items: Matched by best-fit comparison of description, qty, price, amount
- **Overall score:** Weighted average of all field scores
- **Episode rewards:** Best score across all extraction attempts
- **Partial progress:** Feedback identifies weak fields for refinement

## Setup Instructions

### Run with Docker
```bash
docker build -t invoice-extraction-env .
docker run -p 7860:7860 invoice-extraction-env
```

### Run locally
```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Run inference
```bash
export ENV_URL="http://localhost:7860"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="meta-llama/Meta-Llama-3-8B-Instruct"
export HF_TOKEN="your_token_here"
python inference.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset` | POST | Reset with task selection |
| `/step` | POST | Execute an action |
| `/state` | GET | Get current state |
| `/schema` | GET | Get action/observation schemas |
| `/metadata` | GET | Get environment metadata |
| `/ws` | WebSocket | Persistent session |

## Project Structure
```
├── server/
│   ├── __init__.py
│   ├── app.py             # FastAPI application
│   ├── environment.py     # Core environment logic
│   ├── documents.py       # Document corpus
│   ├── graders.py         # Scoring/grading logic
│   └── models.py          # Pydantic Action/Observation types
├── __init__.py            # Package declaration
├── inference.py           # Baseline inference script
├── openenv.yaml           # OpenEnv manifest
├── pyproject.toml         # Package configuration
├── requirements.txt       # Dependencies
├── uv.lock                # Dependency lock file
├── Dockerfile             # Container definition
└── README.md              # This file
```
