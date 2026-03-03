# RAG odgovori na pitanja iz verifikacije softvera

## Prereqs
Pokrenuti skriptu `extract_questions.py` da se generisu pitanja u folderu `pojedinacno/`

## Kako koristiti

Pokrenuti proizvoljni IDE i napisati sledeci prompt agentu:
```
Iskoristi skriptu `random_questions.py` da mi postavis jedno pitanje iz grupe 1. Nakon toga cu dati odgovor na pitanje, a ti oceni koliko se poklapa sa tacnim odgovorom.

Nemoj da pitas nesto sto se ne nalazi u odgovoru. Ako kazem nesto sto je tacno, ali se ne nalazi u datom tekstu, nemoj racunati da je to ispravno.
```
Nakon toga ili odgovoriti na postavljeno pitanje ili popricati sa agentom o nejasnocama.

Pokretati prompt iz pocetka dok se ne odgovori na sva pitanja.
