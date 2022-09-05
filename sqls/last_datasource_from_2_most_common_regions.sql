SELECT 
	t.datasource 
FROM
	jobsity.trips AS t 
INNER JOIN
	(SELECT region, max(datetm) AS datetm FROM jobsity.trips GROUP BY region ORDER BY COUNT(1) limit 2) AS tmp
ON
    t.datetm = tmp.datetm
    AND t.region = tmp.region
 ORDER BY 
    t.datetm DESC
 LIMIT 1;
