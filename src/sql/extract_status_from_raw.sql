INSERT INTO dim_status(name)
SELECT
  DISTINCT
  (CASE 
    WHEN terminated_date = '01-01-1700' THEN 'Active' 
    ELSE 'Terminated'
  END
  ) AS name
FROM raw_employee;
