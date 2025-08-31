import sqlite3  
import pandas as pd   
import requests  
import os  
from logger_config import setup_logger  

## Setting up logging
logger = setup_logger()

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

API_URL = "https://dummyjson.com/users"

#Defines a function that fetches data from the API and returns a pandas DataFrame.
def fetch_data(api_url: str) -> pd.DataFrame:
    """Hämtar studentdata från API och returnerar en DataFrame."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # API returns dict with "users" key
        users = data["users"]

        # Create DataFrame and select useful columns
        df = pd.DataFrame(users)
        df = df[['id', 'firstName', 'lastName', 'age', 'email']]
        logger.info(f"Data hämtades från API, {len(df)} studenter.")
        return df
    except Exception:
        logger.exception("Kunde inte hämta data från API.")
        raise

def update_sql_table(df: pd.DataFrame, db_path: str, table_name: str):
    """Uppdaterar en SQL-tabell med ny data."""
    try:
        conn = sqlite3.connect(db_path) #Connects to the SQLite database at db_path.
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        #Logs that the table was successfully updated.
        logger.info(f"Tabellen '{table_name}' uppdaterades i {db_path}.")
    except Exception:
        logger.exception("Kunde inte uppdatera SQL-tabellen.") #Catches any errors while updating the database.
        raise

if __name__ == "__main__":
    db_path = "data/my_database.db"
    table = "students"

    df = fetch_data(API_URL)
    update_sql_table(df, db_path, table)

    # Print first 10 rows to see the result in terminal
    print(df.head(10))
