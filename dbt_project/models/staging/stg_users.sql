with source as (
    select * from {{ source('raw_app_data', 'users')}}
),
renamed as (
    select
        id as user_id,
        full_name,
        email,
        cast(signup_date as date) as signup_date
    from source
)
select * from renamed