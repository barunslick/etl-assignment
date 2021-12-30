INSERT INTO dim_department (client_department_id, department_name)
SELECT DISTINCT department_id, department_name FROM raw_employee re
