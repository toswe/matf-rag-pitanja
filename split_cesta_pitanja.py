#!/usr/bin/env python3
"""
Skripta koja iz cesta-pitanja.txt izdvaja svako pitanje u zaseban fajl.
- Naziv fajla: {broj pitanja}.txt (npr. 0.8.1.1.txt)
- Prva linija: samo tekst pitanja (bez "Pitanje X.Y.Z")
- Ostatak fajla: odgovor
"""

import re
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "cesta-pitanja.txt"
OUTPUT_DIR = Path(__file__).parent / "cesta_pitanja"

# Obrazac: "Pitanje " + broj (cifre i tačke) + razmak + ostatak (tekst pitanja)
QUESTION_PATTERN = re.compile(r"^Pitanje\s+([\d.]+)\s+(.*)$")


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    OUTPUT_DIR.mkdir(exist_ok=True)
    i = 0

    while i < len(lines):
        line = lines[i]
        match = QUESTION_PATTERN.match(line)
        if not match:
            i += 1
            continue

        broj = match.group(1)
        tekst_pitanja = match.group(2).strip()
        # Uklanjanje završne tačke iz teksta pitanja (npr. "Neformalni pregledi." -> "Neformalni pregledi")
        if tekst_pitanja.endswith("."):
            tekst_pitanja = tekst_pitanja[:-1].strip()

        # Odgovor: sve linije do sledećeg "Pitanje ..."
        answer_lines = []
        i += 1
        while i < len(lines) and not QUESTION_PATTERN.match(lines[i]):
            answer_lines.append(lines[i])
            i += 1

        # Sastavljanje sadržaja fajla: prva linija = pitanje, ostalo = odgovor
        content_lines = [tekst_pitanja]
        if answer_lines:
            content_lines.append("")
            content_lines.extend(answer_lines)

        out_path = OUTPUT_DIR / f"{broj}.txt"
        out_path.write_text("\n".join(content_lines) + "\n", encoding="utf-8")
        print(f"Napisan: {out_path.name}")

    print(f"\nGotovo. Fajlovi su u: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
