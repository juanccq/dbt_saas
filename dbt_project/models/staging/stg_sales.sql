with source as (
    select * from {{ source( 'raw_app_data', 'sales') }}
),
renamed as (
    select 
        id as sale_id,
        employee_id,
        client_id,
        cast(sale_date as date) as sale_date
    from source
)
select * from renamed