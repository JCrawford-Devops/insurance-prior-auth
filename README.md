\# Insurance Prior Auth



A FastAPI + PostgreSQL backend for managing insurance prior authorization requests.



\## Features

\- Submit prior auth requests

\- Validate request payloads with Pydantic

\- Save requests to PostgreSQL

\- Retrieve saved requests



\## Tech Stack

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Pydantic

\- Uvicorn



\## Endpoints

\- `GET /`

\- `GET /ping`

\- `POST /prior-auth`



\## Run locally

```bash

python -m uvicorn app.main:app --reload

