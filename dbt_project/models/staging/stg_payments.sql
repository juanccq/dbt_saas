with source as (
    select * from {{ source('raw_app_data', 'payments') }}
),
renamed as (
    select 
        id as payment_id,
        subscription_id,
        cast(amount as numeric(10,2)) as payment_amount,
        cast(payment_date as date) as payment_date,
        lower(status) as payment_status
    from source
)
select * from renamed