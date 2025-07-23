# Todo API

Una semplice API REST per gestire todo items costruita con FastAPI e SQLite.

## Struttura del Progetto

```
├── src/                    # Codice sorgente dell'applicazione
│   ├── __init__.py
│   ├── main.py            # Entry point dell'applicazione FastAPI
│   ├── api/               # Endpoint API
│   │   ├── __init__.py
│   │   └── todos.py       # Route per i todo items
│   ├── db/                # Gestione database
│   │   ├── __init__.py
│   │   └── database.py    # Connessioni e operazioni database
│   └── models/            # Modelli Pydantic
│       ├── __init__.py
│       └── todo.py        # Modelli per i todo items
├── tests/                 # Test unitari e di integrazione
│   ├── __init__.py
│   ├── conftest.py        # Configurazione pytest e fixture
│   ├── test_api.py        # Test per le API
│   ├── test_database.py   # Test per il database
│   └── test_models.py     # Test per i modelli
├── my_api.db              # Database SQLite
├── requirements.txt       # Dipendenze Python
├── pytest.ini            # Configurazione pytest
├── run.py                 # Script per avviare l'applicazione
└── README.md             # Documentazione del progetto
```

## Installazione

1. Clona il repository
2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Utilizzo

### Avviare l'applicazione

```bash
python run.py
```

L'API sarà disponibile su http://localhost:8000

### Documentazione API

FastAPI genera automaticamente la documentazione interattiva:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Eseguire tutti i test:

```bash
pytest
```

Eseguire test con coverage:

```bash
pytest --cov=src
```

Eseguire test specifici:

```bash
pytest tests/test_api.py
pytest tests/test_database.py
pytest tests/test_models.py
```

## Endpoint API

- `GET /` - Root endpoint
- `GET /todos/` - Ottieni tutti i todo items
- `POST /todos/` - Crea un nuovo todo item
- `DELETE /todos/{item_id}` - Elimina un todo item

## Modelli Dati

### TodoItemCreate

```json
{
  "name": "string"
}
```

### TodoItemResponse

```json
{
  "id": 1,
  "name": "string",
  "created_on": "2023-01-01T12:00:00",
  "completed_on": null
}
```
