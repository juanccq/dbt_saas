{% snapshot subscription_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='id',
        strategy='check',
        check_cols=['plan_name', 'monthly_rate', 'status']
    )
}}

select * from {{ source('raw_app_data', 'subscriptions') }}

{% endsnapshot %}