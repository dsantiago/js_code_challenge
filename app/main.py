from pyspark.sql import SparkSession
from app.helper import exec_sql, move_ingested_files

from pathlib import Path
from typing import Union
from fastapi import FastAPI

app = FastAPI()

opts = {
  "driver": "com.mysql.jdbc.Driver",
  "url": "jdbc:mysql://mysql:3306/jobsity?useSSL=false",
  "dbtable": "trips",
  "user": "root",
  "password": "passwd"
}

spark = SparkSession.builder.config("spark.driver.extraClassPath", "$SPARK_HOME/jars").getOrCreate()

JOBS = {}

@app.get("/ingestion")
def ingestion():
    last_id = max(JOBS.keys()) if JOBS else 0
    last_id += 1
    JOBS[last_id] = "processing"
    
    df = spark.read.option("header", "true").csv("file:///inputs/*.csv")
    df = df.withColumnRenamed("datetime", "datetm")
    df = df.withColumn("datetm", df.datetm.cast("timestamp"))
    df.write.mode("append").format("jdbc").options(**opts).save()

    move_ingested_files()
    JOBS[last_id] = "done"
    return {"OK": "OK", "JobId": last_id}


@app.get("/week_avg")
def week_avg(p1: str, p2: str):
    x1, y1 = map(str.strip, p1.split(","))
    x2, y2 = map(str.strip, p2.split(","))

    query = f"""
        SELECT 
            WEEKOFYEAR(datetm) AS week_year, 
            count(1) / (select count(1) from trips) AS perc from trips 
        WHERE 
            MBRContains(ST_GEOMFROMTEXT('POLYGON(({x1} {y1}, {x1} {y2}, {x2} {y2}, {x2} {y1}, {x1} {y1}))'), PointFromText(origin_coord)) 
        GROUP BY 
            WEEKOFYEAR(datetm)
    """

    ok, results = exec_sql(query)

    if not ok:
        return {"ERROR": result}
        
    result = [{"week_of_year": r[0], "percentage": float(r[1])} for r in results]
    return {"RESULT": result, "AAA": 111}
