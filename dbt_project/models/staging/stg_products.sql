with source as (
    select * from {{ source('raw_app_data', 'products') }}
),
renamed as (
    select 
        id as product_id,
        sku,
        name as product_name,
        cast(unit_price as numeric(10,2)) as product_unit_price
    from source
)
select * from renamed