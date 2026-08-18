with users_subs as (
    select * from {{ ref('int_user_subscriptions') }}
),
payments as (
    select * from {{ ref('stg_payments') }}
),
lifetime_value as (
    select 
        subscription_id,
        sum(payment_amount) as total_revenue,
        count(payment_id) as total_payments_made
    from payments
    where payment_status = 'success'
    group by subscription_id
),
final as (
    select 
        users_subs.user_id,
        users_subs.full_name,
        users_subs.plan_name,
        users_subs.subscription_status,
        users_subs.monthly_rate as current_mrr,
        coalesce(lifetime_value.total_revenue, 0) as total_lifetime_value
    from users_subs
    left join lifetime_value on users_subs.subscription_id = lifetime_value.subscription_id
)
select * from final