import mysql.connector
from pathlib import Path


def exec_sql(query, has_return=True):
    conn = mysql.connector.connect(host='mysql', database='jobsity', user='root', password='passwd')
    
    if not conn.is_connected():
        return False, "Connection Lost."
    
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        return False, str(e)

    results = None
    if has_return:
        results = cursor.fetchall()

    conn.close()
    return True, results

def move_ingested_files():
    Path("/ingested_files").mkdir(exist_ok=True)
    csv_files = Path("/inputs").glob("*.csv")

    for csv_file in csv_files:
        new_path = str(csv_file).replace("inputs", "ingested_files")
        csv_file.rename(new_path)