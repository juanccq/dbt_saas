with commission_by_employee as (
    select * from {{ ref('int_commission_by_employee') }}
),
monthly_bonus as (
    select
        employee_id,
        employee_name,
        role_at_time_of_sale,
        sum(commission_amount) as total_commission
    from commission_by_employee
    group by 1, 2, 3
)
select * 
from monthly_bonus