with source as (
    select * from {{ source('raw_app_data', 'app_events') }}
),
renamed as (
    select
        id as event_id,
        user_id,
        event_name,
        cast(created_at as timestamp) as event_created_at
    from source
)
select * from renamed