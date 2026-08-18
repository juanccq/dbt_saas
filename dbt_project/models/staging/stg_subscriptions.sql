with source as (
    select * from {{ source('raw_app_data', 'subscriptions') }}
),
renamed as (
    select 
        id as subscription_id,
        user_id,
        plan_name,
        cast(monthly_rate as numeric(10,2)) as monthly_rate,
        lower(status) as subscription_status
    from source
)
select * from renamed