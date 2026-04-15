# Insurance Prior Auth

A FastAPI + PostgreSQL backend for managing insurance prior authorization requests.

This project is a portfolio-ready backend application that demonstrates API design, request validation, database integration, and the foundation for a real-world prior authorization workflow system.

## Overview

Insurance prior authorization is often a manual, repetitive process. This application is the beginning of a system that can help automate that workflow by:

- accepting prior auth requests through a REST API
- validating incoming request data
- storing requests in PostgreSQL
- retrieving saved requests
- serving as a foundation for future workflow automation such as status tracking, OCR, rules engines, and packet generation

## Features

- FastAPI backend with interactive Swagger docs
- Pydantic request validation
- PostgreSQL persistence
- SQLAlchemy ORM integration
- Create and retrieve prior authorization requests
- Simple project structure for future scaling

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**

## Current Endpoints

### Health / Base
- `GET /`
- `GET /ping`

### Prior Authorization
- `POST /prior-auth`
- `GET /prior-auths`
- `GET /prior-auths/{auth_id}`

## Example Request

### `POST /prior-auth`

```json
{
  "patient_name": "John Doe",
  "insurance_provider": "Blue Cross",
  "procedure_code": "D1110",
  "diagnosis_code": "K02.9"
}