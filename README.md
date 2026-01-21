# Rental Scout API

Backend API-first (FastAPI + PostgreSQL) dla katalogu pojazdów, ofert oraz leadów z importerem kalkulacji i ofert. Projekt wspiera wiele frontów (public i backoffice) i różne partnerstwa importowe.

## API requirements (minimum)

Public:
- `GET /public/vehicles?make=&model=`
- `GET /public/vehicles/{vehicle_catalog_id}`
- `GET /public/vehicles/{vehicle_catalog_id}/offers?term=&mileage=&partner=`
- `GET /public/offers?make=&model=&term=&mileage=&price_min=&price_max=&partner=`
- `GET /public/offers/{offer_id}`
- `POST /public/leads`
  - body: `{ "offer_id": "...", "contact_json": {...}, "notes": "...", "source":"web" }`

Backoffice:
- `POST /auth/login`
- `GET /backoffice/me`
- `CRUD /backoffice/partners` (ADMIN)
- `CRUD /backoffice/partner-routing-rules` (ADMIN)
- `POST /backoffice/imports/upload` (ADMIN) (multipart + partner_id)
- `POST /backoffice/imports/{id}/run` (ADMIN)
- `GET /backoffice/imports/{id}` (ADMIN)
- `CRUD /backoffice/calc-programs` (ADMIN)
- `GET /backoffice/calc-vehicles` (ADMIN/USER)
- `CRUD /backoffice/vehicles-catalog` (ADMIN/USER)
- `POST /backoffice/vehicles-catalog/{id}/images` (ADMIN/USER) -> MinIO
- `POST /backoffice/vehicles-catalog/{id}/link/{calc_vehicle_id}` (ADMIN/USER)
- `GET /backoffice/offers` (ADMIN/USER)
- `GET /backoffice/leads` (ADMIN/USER)
- `PATCH /backoffice/leads/{id}` (ADMIN)
- `POST /backoffice/leads/{id}/route` (ADMIN/service stub)

## Import RV/RM CSV (calc-ratecard)

Plik CSV zawiera m.in. kolumny:
- Marka, Model / Wersja, Okres, Przebieg Roczny, Przebieg
- Cena katalogowa PLN brutto, Cena po upuście PLN brutto, Rabat, Rejestracja
- RV_Table, RV_Base, RV_ID, RV_Adj, RV %, RV
- RM Table, RM_Val, RM_ID, RM_Val_per km, RM
- Amortyzacja, Bookvalue Y1..Y4
- Koszty: Ubezpieczenie - OC/AC/NNW/ASS, Samochód zastępczy, Likwidacja szkód, Administracja
- Opony: Koszt Opony medium (Jednostkowy), Koszt wymiany opon (Komplet), Koszt przechowywania opon (Komplet), Opony Rata, Opony Budget
- Unnamed:* -> zapis do cost_components jako `UNKNOWN_*`

Mapowanie w DB:
- `calc_programs.code` z nazwy pliku (np. `RENTAL_05_2025`) lub parametru w upload
- `calc_vehicles` upsert po `(partner_id, make, model, trim)`
- `calc_lines` upsert po unique `(calc_program_id, calc_vehicle_id, term_months, total_mileage_km)`
- koszty do `calc_cost_components`

## Lokalne uruchomienie

```bash
cp .env.example .env

docker compose up --build

alembic upgrade head

uvicorn app.main:app --reload
```

## Coolify (deploy)

1. Dodaj repo w Coolify i wybierz Dockerfile.
2. Ustaw zmienne środowiskowe (`DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`).
3. Uruchom usługę API oraz worker Celery (np. osobny service z komendą `celery -A app.workers.tasks worker --loglevel=info`).
4. Upewnij się, że PostgreSQL, Redis i MinIO są dostępne w sieci Coolify.
5. Wykonaj `alembic upgrade head` po starcie bazy.
