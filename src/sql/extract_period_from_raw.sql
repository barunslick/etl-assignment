INSERT INTO dim_period(start_date, end_date)
SELECT
  CAST(hire_date AS DATE) AS start_date,
  CAST((CASE 
    WHEN terminated_date = '01-01-1700' THEN NULL 
    ELSE terminated_date
  END)
  AS DATE) AS end_date
FROM raw_employee
