
CREATE DATABASE jobsity;

DROP TABLE IF EXISTS jobsity.trips;

CREATE TABLE jobsity.trips (
    region varchar(255),
    origin_coord varchar(255),
    destination_coord varchar(255),
    datetm datetime,
    datasource varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
