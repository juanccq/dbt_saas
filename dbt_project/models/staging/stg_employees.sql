with source as (
    select * from {{ source('raw_app_data', 'employees')}}
),
renamed as (
    select 
        id as employee_id,
        name as employee_name,
        role as employee_role
    from source
)
select * from renamed