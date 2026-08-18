with user_subs as (
    select * from {{ ref('int_user_subscriptions') }}
),
lifetime_value as (
    select subscription_id, sum(payment_amount) as total_revenue
    from {{ ref('stg_payments')}}
    where payment_status = 'success'
    group by subscription_id
),
user_events as (
    select
        user_id,
        max(event_created_at) as last_login_date,
        count(event_id) as total_actions_taken
    from {{ ref('stg_app_events') }}
    group by user_id
),
final as (
    select
        user_subs.user_id,
        user_subs.full_name,
        user_subs.subscription_status,
        {{ get_customer_segment('user_subs.monthly_rate') }} as customer_segment,
        coalesce(lifetime_value.total_revenue, 0) as total_lifetime_value,
        user_events.last_login_date,
        case
            when user_events.last_login_date < current_date - interval '30 days'
            and user_subs.subscription_status = 'active'
            then 'High Risk'
            else 'Healthy'
        end as churn_risk
    from user_subs
    left join lifetime_value on user_subs.subscription_id = lifetime_value.subscription_id
    left join user_events on user_subs.user_id = user_events.user_id
)
select * from final