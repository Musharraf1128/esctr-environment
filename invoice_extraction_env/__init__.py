"""
Invoice Extraction Environment — An OpenEnv environment for structured
data extraction from unstructured invoice and receipt documents.

Example:
    >>> import requests
    >>> r = requests.post("http://localhost:7860/reset", json={"task_name": "simple_invoice"})
    >>> obs = r.json()
"""

from .models import InvoiceAction, InvoiceObservation, InvoiceState

__all__ = [
    "InvoiceAction",
    "InvoiceObservation",
    "InvoiceState",
]
