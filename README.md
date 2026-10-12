# Flight Tracker ETL

A Python pipeline that pulls live flight data from the OpenSky API and saves it to a local PostgreSQL database. It's built with OOP principles and designed to run automatically as a cron job.

## What it does
Authenticates with the OpenSky API and handles token expiration automatically.
Fetches real-time flight data for a specific area (configured in `settings.py`).
Filters and cleans the data using `pandas`.
Inserts new records into PostgreSQL.
Ignores duplicate entries on the database level using `ON CONFLICT DO NOTHING`.
Logs all actions and errors to `logs/app.log`.

## Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Giorgi1379/Flight-Tracker.git](https://github.com/Giorgi1379/Flight-Tracker.git)
   cd Flight-Tracker