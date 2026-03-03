#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Izdvaja svako pitanje iz Verifikacija-*.txt u zaseban fajl u folderu pojedinacno.
   Pitanja su u formatu grupa.broj (npr. 1.1, 2.10). Izlazni fajlovi: {grupa}.{broj}.txt"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
POJEDINACNO = os.path.join(BASE, "pojedinacno")

# Svi izvorni fajlovi (preimenovani po grupama)
FILES = [
    "Verifikacija-1-9.txt",
    "Verifikacija-10-31.txt",
    "Verifikacija-32-40.txt",
    "Verifikacija-41-44.txt",
    "Verifikacija-45-52.txt",
    "Verifikacija-3-i-4-grupa.txt",
]

# Početak pitanja: ## Pitanje 1.1: / ### **Pitanje 2.10.** / ## **Pitanje 1.32.** ili (3-i-4-grupa) Pitanje 3.1 / Pitanje 3.10.
# Hvata grupu i broj: (grupa, broj)
QUESTION_START = re.compile(
    r"^(?:#{2,3}\s*\*?\*?)?Pitanje\s+(\d+)\.(\d+)(?:[.:]\s*|\s)",
    re.IGNORECASE
)

def find_question_starts(path):
    """Vraća listu (line_1based, (grupa, broj)) za sve početke pitanja u fajlu."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = QUESTION_START.match(stripped)
        if m:
            grupa, broj = int(m.group(1)), int(m.group(2))
            result.append((i + 1, (grupa, broj)))  # 1-based line number
    return result, lines

def extract_question_content(lines, start_idx, end_idx):
    """Izdvaja sadržaj od start_idx do end_idx (end_idx se ne uključuje)."""
    return "".join(lines[start_idx:end_idx])

def main():
    os.makedirs(POJEDINACNO, exist_ok=True)
    for filename in FILES:
        path = os.path.join(BASE, filename)
        if not os.path.isfile(path):
            print(f"Preskačem (nije fajl): {filename}")
            continue
        starts, lines = find_question_starts(path)
        for k, (line_no, (grupa, broj)) in enumerate(starts):
            start_idx = line_no - 1  # 0-based
            if k + 1 < len(starts):
                end_idx = starts[k + 1][0] - 1
            else:
                end_idx = len(lines)
            content = extract_question_content(lines, start_idx, end_idx)
            out_name = f"{grupa}.{broj}.txt"
            out_path = os.path.join(POJEDINACNO, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Zapisano: {out_name}")
    print("Gotovo.")

if __name__ == "__main__":
    main()
