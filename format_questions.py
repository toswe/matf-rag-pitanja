#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dodaje oznake Pitanje 3.N i Pitanje 4.N pitanjima u vs_pitanja___II_deo."""

import re

INPUT_FILE = "vs_pitanja___II_deo (1)_260227_160953.txt"
OUTPUT_FILE = INPUT_FILE  # prepisujemo isti fajl

def replacer(match):
    num = int(match.group(1))
    if 1 <= num <= 24:
        return f"Pitanje 3.{num} "
    if 25 <= num <= 53:
        return f"Pitanje 4.{num - 24} "
    return match.group(0)

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # Samo linije koje pocinju brojem, tackom i razmakom (prav broj pitanja)
    pattern = re.compile(r"^(\d{1,2})\. ", re.MULTILINE)
    new_content = pattern.sub(replacer, content)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Završeno. Zamenjene oznake pitanja (1.–24. → Pitanje 3.1–3.24, 25.–53. → Pitanje 4.1–4.29).")

if __name__ == "__main__":
    main()
