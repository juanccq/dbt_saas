with sales_by_employee as (
    select * from {{ ref('int_sales_by_employee') }}
),
employee as (
    select * from {{ ref('employees_snapshot')}}
),
commission_by_employee as (
    select
        e.id as employee_id,
        e.name as employee_name,
        e.role as role_at_time_of_sale,
        case 
            when e.role = 'cashier' then sbe.total_sale_item * 0.02
            when e.role = 'branch_admin' then sbe.total_sale_item * 0.05
            else 0
        end as commission_amount
    from sales_by_employee as sbe
    left join employee as e on e.id = sbe.employee_id
        and sbe.sale_date >= cast(e.dbt_valid_from as date)
        and (sbe.sale_date < cast(e.dbt_valid_to as date) or e.dbt_valid_to is null)
)
select *
from commission_by_employee