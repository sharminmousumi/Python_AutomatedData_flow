import pytest
import pandas as pd
from main import fetch_data, update_sql_table, API_URL
import sqlite3

TABLE_NAME = "students"

def test_fetch_data():
    df = fetch_data(API_URL)
    ## Check that we get a DataFrame
    assert isinstance(df, pd.DataFrame)
    #Check that important columns are present
    for col in ["id", "firstName", "lastName", "age", "email"]:
        assert col in df.columns
    # Check that we got at least 1 row
    assert len(df) > 0

def test_update_sql_table(tmp_path):
    # Create a small DataFrame
    test_df = pd.DataFrame([{
        "id": 1,
        "firstName": "Test",
        "lastName": "Student",
        "age": 22,
        "email": "test@student.com"
    }])

    # Use temporary database
    db_path = tmp_path / "test.db"
    update_sql_table(test_df, db_path, TABLE_NAME)

    # Verify that the data exists in SQLite
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cur.fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][1] == "Test"   # firstName ska vara "Test"
