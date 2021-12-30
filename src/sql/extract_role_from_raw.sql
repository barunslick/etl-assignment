INSERT INTO dim_role(name)
SELECT
  DISTINCT 
  (CASE 
    WHEN employee_role LIKE '%Mgr%' OR employee_role LIKE '%Supv%' THEN 'Manager' 
    ELSE 'Employee'
  END
  ) AS name
FROM raw_employee;
