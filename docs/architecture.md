# Architecture — HumanitAID

## Stack technique

| Couche      | Technologie                      |
|-------------|----------------------------------|
| API         | Python 3.12+ / FastAPI           |
| ORM         | SQLAlchemy 2.0 (asyncio)         |
| Base de données | PostgreSQL 16                |
| Migrations  | Alembic                          |
| Paiement    | Stripe (via stripe-python)       |
| Email       | SMTP (via smtplib)               |
| Tests       | pytest + httpx + aiosqlite       |
| Conteneurisation | Docker / docker-compose     |

## Structure du projet

```
humanitaid/
├── app/
│   ├── api/           # Routes FastAPI
│   ├── models/        # Modèles SQLAlchemy
│   ├── schemas/       # Schémas Pydantic
│   ├── services/      # Logique métier (paiement, email)
│   └── tests/         # Tests
├── migrations/        # Migrations Alembic
├── docs/              # Documentation
└── docker-compose.yml
```

## Flux de données

```
Donateur → API → Service Paiement → Stripe
                → Base de données   → PostgreSQL
                → Service Email     → SMTP
```

## Sécurité

- Mots de passe hashés avec bcrypt
- Variables sensibles en variable d'environnement (`.env`)
- CORS configurable

## Démarrage rapide

```bash
cp .env.example .env
docker compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```
