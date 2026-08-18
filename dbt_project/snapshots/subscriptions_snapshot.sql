{% snapshot subscription_snapshot %}
-- Maybe this file should be deleted
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