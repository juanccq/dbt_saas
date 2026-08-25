with source as (
    select * from {{ source('raw_app_data', 'clients') }}
),
renamed as (
    select 
        id as client_id,
        name as client_name,
        email as client_email,
        cast(created_at as date) as created_date
    from source
)
select * from renamed