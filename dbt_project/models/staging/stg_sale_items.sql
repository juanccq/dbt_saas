with source as (
    select * from {{ source('raw_app_data', 'sale_items') }}
),
renamed as (
    select 
        id as sale_item_id,
        sale_id,
        product_id,
        cast(quantity as integer) as quantity,
        cast(price as numeric(10,2)) as unit_price,
        row_number() over (partition by sale_id, product_id, quantity, price order by id) as rn
    from source
)
select 
    sale_item_id,
    sale_id,
    product_id,
    quantity,
    unit_price
from renamed
where rn = 1