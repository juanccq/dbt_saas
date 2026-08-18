{% snapshot employees_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='id',
        strategy='check',
        check_cols=['name', 'role']
    )
}}

select * from {{ source('raw_app_data', 'employees') }}

{% endsnapshot %}