"""Utility helpers for the Google Sheets provider."""

from __future__ import annotations

from urllib.parse import quote


def encode_a1_range(range_name: str) -> str:
    """URL-encode an A1 range for inclusion in request paths."""

    safe_chars = "!:'$,-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    return quote(range_name, safe=safe_chars)
