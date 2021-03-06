CREATE TABLE fact_timesheet(
    employee_id INT,
    work_date DATE,
    department_id INT,
    hours_worked FLOAT,
    shift_type_id INT,
    punch_in_time TIME,
    punch_out_time TIME,
    time_period_id INT,
    attendance BOOLEAN,
    work_code VARCHAR(255),
    has_taken_break BOOLEAN,
    break_hour FLOAT,
    was_charge BOOLEAN,
    charge_hour FLOAT,
    was_on_call BOOLEAN,
    on_call_hour FLOAT,
    is_weekend BOOLEAN,
    num_teammates_absent INT,
    FOREIGN KEY(employee_id) REFERENCES fact_employee(employee_id),
    FOREIGN KEY(department_id) REFERENCES dim_department(id),
    FOREIGN KEY(shift_type_id) REFERENCES dim_shift(id),
    FOREIGN KEY(time_period_id) REFERENCES dim_period(id)
)
