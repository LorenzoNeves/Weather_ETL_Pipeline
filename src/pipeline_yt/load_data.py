from sqlalchemy import create_engine, text, inspect
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parents[2] / 'config' / '.env'

load_dotenv(env_path)

user = os.getenv('DB_USER')
password = str(os.getenv('PASSWORD'))
database = os.getenv('DATABASE')
#host = 'host.docker.internal'
host = 'localhost'

def get_engine():
    logging.info(f"→ Conectando em {host}:5432/{database}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )
    
engine = get_engine()

def sql_type(dtype) -> str:
    if pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    if pd.api.types.is_integer_dtype(dtype):
        return 'BIGINT'
    if pd.api.types.is_float_dtype(dtype):
        return 'DOUBLE PRECISION'
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    return 'TEXT'


def add_missing_columns(table_name:str, df):
    #a API só manda alguns campos (ex: rain, snow, wind.gust) quando eles existem, então a tabela pode não ter a coluna ainda
    if not inspect(engine).has_table(table_name):
        return

    existing = {c['name'] for c in inspect(engine).get_columns(table_name)}
    missing = [c for c in df.columns if c not in existing]

    with engine.begin() as conn:
        for column in missing:
            logging.info(f"Adicionando coluna '{column}' na tabela {table_name}")
            conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN "{column}" {sql_type(df[column].dtype)}'))


def load_weather_data(table_name:str, df):
    add_missing_columns(table_name, df)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )
    
    logging.info(f"✅ Dados carregados com sucesso!\n") 
    
    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}\n")