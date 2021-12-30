WITH all_distinct_timesheet_records AS (
		SELECT employee_id, 
		punch_apply_date
		FROM raw_timesheet rt
		GROUP BY employee_id, punch_apply_date
	), 
	hours_worked AS (
		SELECT employee_id, 
		punch_apply_date,
		MIN(TO_TIMESTAMP (punch_in_time, 'YYYY.MM.DD HH24:MI:SS')::time) AS punch_in_time,
		MAX(TO_TIMESTAMP (punch_out_time, 'YYYY.MM.DD HH24:MI:SS')::time) AS punch_out_time,
		SUM(CAST(hours_worked AS FLOAT)) AS hours_worked
		FROM raw_timesheet rt
		WHERE paycode = 'WRK'
		GROUP BY employee_id, punch_apply_date
	),
	worked_shift_type AS (
		SELECT employee_id,
		punch_apply_date,
		(CASE 
			WHEN punch_in_time >= '05:00:00' AND punch_in_time < '12:00:00' THEN 'Morning'
			WHEN punch_in_time >= '12:00:00' AND punch_in_time <= '18:00:00' THEN 'Afternoon'
		END
		) AS shift_type
		FROM hours_worked	
	),
	attendance AS (
		SELECT t.employee_id , t.punch_apply_date,
		bool_and(attendance) AS attendance
		FROM (
			SELECT
			employee_id,
			punch_apply_date,
			(CASE 
			    WHEN paycode = 'ABSENT' THEN FALSE ELSE TRUE
			END
			) AS attendance
			FROM raw_timesheet
		) AS t
		GROUP BY t.employee_id, t.punch_apply_date
	),
	break_hours AS (
		SELECT
		employee_id,
		punch_apply_date,
		SUM(CAST(hours_worked AS FLOAT)) AS break_hours
		FROM raw_timesheet
		WHERE paycode = 'BREAK'
		GROUP BY employee_id, punch_apply_date
	),
	charge_hours AS (
		SELECT
		employee_id,
		punch_apply_date,
		SUM(CAST(hours_worked AS FLOAT)) AS charge_hours
		FROM raw_timesheet
		WHERE paycode = 'CHARGE'
		GROUP BY employee_id, punch_apply_date
	),
	on_call_hours AS (
		SELECT
		employee_id,
		punch_apply_date,
		SUM(CAST(hours_worked AS FLOAT)) AS on_call_hours
		FROM raw_timesheet
		WHERE paycode = 'ON_CALL'
		GROUP BY employee_id, punch_apply_date
	)
INSERT INTO fact_timesheet(employee_id, department_id, work_date, hours_worked, shift_type_id, punch_in_time, punch_out_time, attendance, work_code, has_taken_break, break_hour, was_charge, charge_hour, was_on_call, on_call_hour, is_weekend, num_teammates_absent, time_period_id)
SELECT fe.employee_id,
fe.department_id,
CAST(all_rec.punch_apply_date AS DATE) AS work_date,
hw.hours_worked,
ds.id AS shift_id,
hw.punch_in_time,
hw.punch_out_time,
att.attendance,
NULL AS work_code,
CASE WHEN COALESCE (bh.break_hours,0) > 0 THEN TRUE ELSE FALSE END AS has_taken_break,
COALESCE (bh.break_hours,0) AS break_hours,
CASE WHEN COALESCE (ch.charge_hours,0) > 0 THEN TRUE ELSE FALSE END AS was_charge,
COALESCE (ch.charge_hours,0) AS charge_hours,
CASE WHEN COALESCE (och.on_call_hours,0) > 0 THEN TRUE ELSE FALSE END AS was_on_call,
COALESCE (och.on_call_hours,0) AS on_call_hours,
(EXTRACT(ISODOW FROM CAST(all_rec.punch_apply_date AS DATE)) IN (6, 7)) AS is_weekend,
NULL AS num_teams_absent,
NULL AS time_period_id
FROM all_distinct_timesheet_records all_rec
LEFT JOIN fact_employee fe ON fe.client_employee_id = all_rec.employee_id
LEFT JOIN hours_worked hw ON all_rec.employee_id = hw.employee_id AND all_rec.punch_apply_date = hw.punch_apply_date
LEFT JOIN worked_shift_type wst ON wst.employee_id = hw.employee_id AND wst.punch_apply_date = hw.punch_apply_date
LEFT JOIN dim_shift ds ON ds.name = wst.shift_type
LEFT JOIN attendance att ON att.employee_id = all_rec .employee_id AND att.punch_apply_date = all_rec .punch_apply_date
LEFT JOIN break_hours bh ON bh.employee_id = all_rec.employee_id AND bh.punch_apply_date = all_rec.punch_apply_date
LEFT JOIN charge_hours ch ON ch.employee_id = all_rec.employee_id AND ch.punch_apply_date = all_rec.punch_apply_date
LEFT JOIN on_call_hours och ON och.employee_id = all_rec.employee_id AND och.punch_apply_date = all_rec.punch_apply_date
