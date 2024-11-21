# Derive Insights from BigQuery Data: Challenge Lab

## Task 1: Total Confirmed Cases
### What was the total count of confirmed cases on May 25, 2020?
```sql
select count(distinct subregion1_name) count_of_states
from bigquery-public-data.covid19_open_data.covid19_open_data
where date = '2020-05-25'
and country_name= 'United States of America'
and cumulative_deceased >150;
```

## Task 2. Worst affected areas
-- How many states in the US had more than 150 deaths on May 25, 2020?
```sql
select  count(subregion1_name) as count_of_states
from (
select subregion1_name
from bigquery-public-data.covid19_open_data.covid19_open_data
where date = '2020-05-25'
and country_name= 'United States of America'
and subregion1_name is not null
group by subregion1_name
having sum(cumulative_deceased)>150
);
```

## Task 3: Identifying Hotspots
-- List all the states in the United States of America that had more than 2000 confirmed cases on May 25, 2020?
```sql
select subregion1_name state, sum(cumulative_confirmed) total_confirmed_cases
from bigquery-public-data.covid19_open_data.covid19_open_data
where date = '2020-05-25'
and country_code= 'US'
and country_name= 'United States of America'
and subregion1_name is not null
group by subregion1_name
having total_confirmed_cases>2000
ORDER BY total_confirmed_cases DESC ;
```

## Task 4: Fatality ratio
-- What was the case-fatality ratio in Italy for the month of May 2020?" Case-fatality ratio here is defined as (total deaths / total confirmed cases) * 100.
```sql
select sum(cumulative_confirmed) as total_confirmed_cases, 
sum(cumulative_deceased) as total_deaths, 
sum(cumulative_deceased)/sum(cumulative_confirmed) *100 as case_fatality_ratio
from bigquery-public-data.covid19_open_data.covid19_open_data
WHERE country_name="Italy" and 
date BETWEEN "2020-05-01" AND "2020-05-31";
```

## Task 5. Identifying specific day
### On what day did the total number of deaths cross 12000 in Italy
```sql
SELECT date
FROM `bigquery-public-data.covid19_open_data.covid19_open_data` 
WHERE country_name="Italy" and cumulative_deceased > 12000
ORDER BY date ASC
LIMIT 1;
```

## Task 6. Finding days with zero net new cases
```sql
WITH india_cases_by_date AS (
  SELECT date, SUM(cumulative_confirmed) AS cases
  FROM
    `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE
    country_name="India"
    AND date between '2020-02-22' and '2020-03-13'
  GROUP BY date
  ORDER BY date ASC
 )
, india_previous_day_comparison AS
(SELECT date,  cases,  LAG(cases) OVER(ORDER BY date) AS previous_day,
  cases - LAG(cases) OVER(ORDER BY date) AS net_new_cases
FROM india_cases_by_date
)
SELECT count(*)
FROM india_previous_day_comparison
WHERE net_new_cases = 0;
```

## Task 7. Doubling rate
```sql
WITH us_cases_by_date AS (
  SELECT date, SUM(cumulative_confirmed) AS cases
  FROM
    `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE
    country_name="United States of America"
    AND date between '2020-03-22' and '2020-04-20'
  GROUP BY date
  ORDER BY date ASC
 )
, us_previous_day_comparison AS
(SELECT date,  cases,  LAG(cases) OVER(ORDER BY date) AS previous_day,
  cases - LAG(cases) OVER(ORDER BY date) AS net_new_cases,
  (cases - LAG(cases) OVER(ORDER BY date))*100/LAG(cases) OVER(ORDER BY date) AS percentage_increase
FROM us_cases_by_date
)
SELECT Date, cases as Confirmed_Cases_On_Day, previous_day as Confirmed_Cases_Previous_Day, percentage_increase as Percentage_Increase_In_Cases
FROM us_previous_day_comparison
WHERE percentage_increase > 5
```

## Task 8. Recovery rate
```sql
WITH cases_by_country AS (
  SELECT
    country_name AS country,
    sum(cumulative_confirmed) AS cases,
    sum(cumulative_recovered) AS recovered_cases
  FROM
    bigquery-public-data.covid19_open_data.covid19_open_data
  WHERE
    date = '2020-05-10'
  GROUP BY
    country_name
 )
, recovered_rate AS 
(SELECT
  country, cases, recovered_cases,
  (recovered_cases * 100)/cases AS recovery_rate
FROM cases_by_country
)
SELECT country, cases AS confirmed_cases, recovered_cases, recovery_rate
FROM recovered_rate
WHERE cases > 50000
ORDER BY recovery_rate desc
LIMIT 5
```

## Task 9. CDGR - Cumulative daily growth rate
```sql

WITH
  france_cases AS (
  SELECT
    date,
    SUM(cumulative_confirmed) AS total_cases
  FROM
    `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE
    country_name="France"
    AND date IN ('2020-01-24',
      '2020-05-25')
  GROUP BY
    date
  ORDER BY
    date)
, summary as (
SELECT
  total_cases AS first_day_cases,
  LEAD(total_cases) OVER(ORDER BY date) AS last_day_cases,
  DATE_DIFF(LEAD(date) OVER(ORDER BY date),date, day) AS days_diff
FROM
  france_cases
LIMIT 1
)

select first_day_cases, last_day_cases, days_diff, POW((last_day_cases/first_day_cases),(1/days_diff))-1 as cdgr
from summary
```

## Task 10. Create a Looker Studio report
```sql
SELECT
  date, SUM(cumulative_confirmed) AS country_cases,
  SUM(cumulative_deceased) AS country_deaths
FROM
  `bigquery-public-data.covid19_open_data.covid19_open_data`
WHERE
  date BETWEEN '2020-03-16'
  AND '2020-04-27'
  AND country_name ="United States of America"
GROUP BY date
```
