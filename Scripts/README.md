# Star Systems Importer

Skrypty umożliwiają wstawianie danych z plików XML o systemach gwiezdnych, gwiazdach i planetach do różnych baz danych: PostgreSQL, MySQL, MongoDB 6 i MongoDB 8.

## Jak używać

1. Skonfiguruj połączenie w pliku `config.py` dla wybranej bazy (użytkownik, hasło, host, port, nazwa bazy `star_db`).

2. Uruchom skrypt importu, podając ścieżkę do pliku XML:

```bash
python Scripts/PostgresImport/import_xml_to_db.py "ścieżka/do/pliku.xml"
