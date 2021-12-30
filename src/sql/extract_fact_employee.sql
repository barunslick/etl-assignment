INSERT INTO fact_employee(client_employee_id, department_id, manager_id, role_id, salary, active_status_id, weekly_hours)
SELECT 
  employee_id AS client_employee_id,
  (SELECT id FROM dim_department WHERE department_name = re.department_name AND client_department_id = re.department_id) AS department_id,
  (CASE 
   WHEN manager_employee_id = '-' THEN NULL ELSE manager_employee_id
   END  
  ) AS manager_id,
  (CASE
    WHEN re.employee_role LIKE '%Mgr%' OR re.employee_role LIKE '%Supv%' THEN 
      (SELECT role_id FROM dim_role WHERE name = 'Manager')
    ELSE (SELECT role_id FROM dim_role WHERE name = 'Employee')
  END
  ) AS role_id,
  CAST(salary AS FLOAT),
  (CASE 
    WHEN re.terminated_date = '01-01-1700' THEN 
      (SELECT status_id FROM dim_status WHERE name = 'Active')
    ELSE (SELECT status_id FROM dim_status WHERE name = 'Terminated')
  END
  ) AS active_status_id,
  CAST(fte AS FLOAT) * 40 AS weekly_hours
  FROM raw_employee re
