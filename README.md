# ECOMUTE

A REST API for managing an e-bike rental service, built with FastAPI and async SQLAlchemy.

---

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy 2.x (async)** — ORM and database access
- **SQLite + aiosqlite** — database
- **JWT (python-jose)** — authentication
- **passlib + bcrypt** — password hashing
- **scikit-learn / joblib** — ML trip duration prediction

---

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```

3. Open the interactive docs at `http://localhost:8000/docs`

> The database and tables are created automatically on startup. Seed data is loaded if the database is empty.

---

## Authentication

The API uses JWT Bearer tokens.

1. Call `POST /auth/token` with your username and password to get a token.
2. Pass the token in the `Authorization` header on protected requests:
   ```
   Authorization: Bearer <your_token>
   ```

Tokens expire after **30 minutes**.

---

## Endpoints

### Auth

**`POST /auth/token`**
Login with username and password. Returns a JWT access token.

---

### Users

**`POST /users/`**
Create a new user.

**`POST /users/signup-test`**
Sign up with email validation and password rules (min 8 characters, alphanumeric only).

**`GET /users/`**
Get all users.

**`GET /users/{user_id}`**
Get a single user by ID.

**`PUT /users/{user_id}`**
Update a user.

**`DELETE /users/{user_id}`**
Delete a user.

---

### Bikes

**`GET /bikes/`**
Get all bikes. Optionally filter by status:
```
GET /bikes/?status=available
GET /bikes/?status=rented
GET /bikes/?status=maintenance
```

**`GET /bikes/{bike_id}`**
Get a single bike by ID.

**`POST /bikes/`**
Create a new bike.

**`PUT /bikes/{bike_id}`**
Update a bike.

**`DELETE /bikes/{bike_id}`**
Delete a bike.

---

### Stations

**`GET /stations/`**
Get all stations.

**`POST /stations/`** _(Admin only)_
Create a new station.

---

### Rentals

**`POST /rentals/`**
Create a rental. The bike's battery must be at least 20%.

---

### Admin

**`GET /admin/stats`** _(Admin only)_
Get admin stats.

---

### ML Prediction

**`POST /predict/duration`**
Predict the duration of a trip given distance and battery level.

---

## Data Models

### Bike
```json
{
  "model": "Trek FX3",
  "battery": 85,
  "status": "available",
  "station_id": 2
}
```

### Station
```json
{
  "name": "Central Park North",
  "location": "110th St & Lenox Ave",
  "capacity": 15
}
```

### Rental
```json
{
  "user_id": 1,
  "bike_id": 3,
  "bike_battery": 75
}
```

### Trip Prediction
```json
{
  "distance_km": 4.5,
  "battery_level": 80.0
}
```

---

## Roles

| Role | Description |
|------|-------------|
| `rider` | Default role. Access to all public endpoints. |
| `admin` | Extended access to `POST /stations/` and `GET /admin/stats`. |
