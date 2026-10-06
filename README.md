# Weather ETL Pipeline

> **Learning Project**
>
> This is a project I copied/adapted from a YouTube tutorial for educational purposes.

An ETL pipeline that pulls current weather data for São Paulo from the [OpenWeatherMap API](https://openweathermap.org/api), transforms it with pandas, and loads it into PostgreSQL. It runs hourly, orchestrated by Apache Airflow inside Docker.

## Credits

- Original tutorial: [vbluuiza](https://www.youtube.com/watch?v=I8qPqbXQBDU&t=1066s)
- Goal: learn about Docker, PostgreSQL and Apache Airflow

## What I modified/learned

- Implemented the **extract → transform → load** steps from scratch as separate modules in `src/pipeline_yt/`
- Adapted the configuration to load credentials (API key, database user/password) from `config/.env` with `python-dotenv`
- Added automatic schema evolution: the API only returns some fields (e.g. `rain`, `snow`, `wind.gust`) when they exist, so the load step creates any missing columns in the table before inserting
- Built the Airflow DAG (`weather_pipeline`) with the TaskFlow API, retries, and an hourly schedule
- Explored the raw API response in a Jupyter notebook before writing the transformations

## How it works

```
OpenWeatherMap API ──► extract ──► data/weather_data.json
                                         │
                                     transform  (flatten JSON, rename/drop columns,
                                         │       convert timestamps to America/Sao_Paulo)
                                         ▼
                                data/temp_data.parquet
                                         │
                                       load ──► PostgreSQL (table: sp_weather)
```

## Project structure

```
├── dags/weather_data.py          # Airflow DAG (extract >> transform >> load)
├── src/pipeline_yt/
│   ├── extract_data.py           # Calls the API and saves the raw JSON
│   ├── transform_data.py         # Cleans and normalizes the data with pandas
│   └── load_data.py              # Writes the DataFrame to PostgreSQL
├── notebooks/analysis_data.ipynb # Data exploration
├── main.py                       # Runs the pipeline locally, without Airflow
├── docker-compose.yaml           # Airflow + PostgreSQL + Redis stack
└── config/.env                   # Credentials (not committed)
```

## Getting started

1. Create `config/.env`:

   ```env
   API_KEY=your_openweathermap_key
   DB_USER=your_db_user
   PASSWORD=your_db_password
   DATABASE=your_db_name
   ```

2. Start the Airflow stack:

   ```bash
   docker compose up -d
   ```

3. Open the Airflow UI at http://localhost:8080 and enable the `weather_pipeline` DAG.

To run the pipeline once without Airflow:

```bash
uv sync
uv run python main.py
```

## Technologies

- Python
- PostgreSQL
- Docker
- Apache Airflow
