"""
utils.py - Fungsi utilitas untuk Chatbot Akademik UPGRIS
========================================================
Berisi fungsi-fungsi pembantu yang digunakan oleh modul lain.
"""

import csv
import io
import json
from pathlib import Path
from typing import Any


# ============================================================
# Path
# ============================================================
DATA_DIR = Path(__file__).parent / "data"
ASSETS_DIR = Path(__file__).parent / "assets"


def get_logo_path() -> str | None:
    """Mengembalikan path logo UPGRIS jika file ada, None jika tidak."""
    logo = ASSETS_DIR / "logo_upgris.png"
    if logo.exists():
        return str(logo)
    return None


def load_all_json_files() -> dict[str, Any]:
    """Memuat semua file JSON dari folder data/ ke dalam dictionary."""
    result = {}
    if not DATA_DIR.exists():
        return result
    for json_file in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                result[json_file.stem] = json.load(f)
        except (json.JSONDecodeError, IOError):
            result[json_file.stem] = {"error": "Gagal memuat file"}
    return result


def get_data_summary() -> list[dict]:
    """Mengembalikan ringkasan semua file data JSON."""
    summary = []
    if not DATA_DIR.exists():
        return summary
    for json_file in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            keys = list(data.keys()) if isinstance(data, dict) else []
            summary.append({
                "file": json_file.name,
                "ukuran": f"{json_file.stat().st_size:,} bytes",
                "jumlah_key": len(keys),
                "keys": ", ".join(keys[:5]) + ("..." if len(keys) > 5 else ""),
            })
        except (json.JSONDecodeError, IOError):
            summary.append({
                "file": json_file.name,
                "ukuran": "-",
                "jumlah_key": 0,
                "keys": "Error membaca file",
            })
    return summary


def export_transitions_csv(transitions: list[dict]) -> str:
    """Mengonversi riwayat transisi ke format CSV string untuk download."""
    output = io.StringIO()
    if not transitions:
        return ""
    fieldnames = ["no", "from", "to", "input", "intent"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for i, t in enumerate(transitions, 1):
        writer.writerow({
            "no": i,
            "from": t.get("from", ""),
            "to": t.get("to", ""),
            "input": t.get("input", ""),
            "intent": t.get("intent", ""),
        })
    return output.getvalue()


# ============================================================
# Contoh pertanyaan untuk quick buttons
# ============================================================
CONTOH_PERTANYAAN = [
    "Apa itu UPGRIS?",
    "Jelaskan Prodi Informatika",
    "Siapa dosen Informatika?",
    "Apa saja kurikulum Informatika?",
    "Bagaimana cara daftar PMB?",
    "Berapa UKT Informatika?",
    "Berapa biaya kuliah PGSD?",
    "Daftar UKT semua prodi",
    "Apa saja beasiswa di UPGRIS?",
    "Apa itu MBKM?",
    "Apa itu KRS?",
    "Bagaimana cara melihat KHS?",
    "Bagaimana proses skripsi?",
    "Apa syarat PKL?",
    "Apa syarat KKN?",
    "Apa syarat wisuda?",
    "Daftar fakultas di UPGRIS?",
    "Kalender akademik",
    "FAQ",
]
