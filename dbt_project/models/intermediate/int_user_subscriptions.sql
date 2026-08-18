with users as (
    select * from {{ ref('stg_users') }}
),
subscriptions as (
    select * from {{ ref('stg_subscriptions') }}
),
joined as (
    select
        users.user_id,
        users.full_name,
        users.email,
        users.signup_date,
        subscriptions.subscription_id,
        subscriptions.plan_name,
        subscriptions.monthly_rate,
        subscriptions.subscription_status
    from users
    left join subscriptions on users.user_id = subscriptions.user_id
)
select * from joined