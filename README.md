# Overview

Jobsity Data Eng. code challenge.

For this task I had firstly used 3 containers in a docker-compose:
- Hadoop
- Api + Spark
- Mysql

But I had intermitent problems reading files from the remote hdfs in `Hadoop` container from `Api` container. So I decided to comment the hadoop entry and imagine i am reading form `/inputs` as it was on hdfs.

## Installation
There's just 2 steps:
- Run docker-compose (be sure to be in root directory).
```bash
docker-compose up -d
```

- Once the API and Mysql containers are up, initialize `trips` table. (the file is already in container).
```bash
docker exec -it mysql bash -c "mysql -u root -ppasswd < initialize.sql"
```

## Running application

The table trips will be empty, what we can do first is import data, this will load `trips.csv` via Spark and insert into Mysql. Column `datetime` was changed to `datetm` to avoid any reserved term. There's an internal variable `JOBS` that appends where job is `running` and when it's `done`. Could be done with another table in Mysql also. Files that are loaded from `/inputs` are moved to `/ingested_files`

```bash
http://localhost:8080/ingestion
```

For consulting avarage number of trips in a rectangle region, the `week_avg` endpoint can be used. The parameters `p1` and `p2` indicates the top-left and bottom-right points from this rectangle as can be seen in the example:

```bash
http://localhost:8080/week_avg?p1=0,0&p2=50,50
```

## Entering Containers

```bash
docker exec -it api bash # Api Container
```

```bash
docker exec -it mysql bash # Mysql Container, user=root, password=passwd
```

In Api container, `/files` is a linked volume if one wants to use files in container.

## Troubleshooting

On MacOS, sometimes the internal network do not work. To fix it:
- System Preferences -> Sharing -> Check the "Remote Login" box.
- The `hadoop` container works and can be reached in:

```bash
http://localhost:9870
```

but like I said before, lost too much time trying to fix the remote connection from one container to another and even though it worked, was intermitent so I choose to not keep with using it.

## Specifics
- __Scalability__:
The solution is asked to be scalable to 100 million entries. This can be achieved using a DFS(Hadoop, S3, etc.), read by Spark and ingested on demand in target database.
- __Cloud__: One could use Aws Lambda, Google Functions, etc in place of FastApi and use internatl tools for ingestion like Aws Glue on top of Boto3.
- __Automation__: The solution is not automated by any means but we can think of any tools the schedule jobs, from simples crontabs to Airflow, invoking Api calls.

## Questions
- From the two most commonly appearing regions, which is the latest datasource?
R: baba_car. Solution can be found in `sqls/last_datasource_from_2_most_common_regions.sql`

- What regions has the "cheap_mobile" datasource appeared in?
R: Prague, Turin, Hamburg. Solution can be found in `sqls/regions_cheapmobile_appeared.sql`
