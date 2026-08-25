with sales as (
    select * from {{ ref('stg_sales') }}
),
sale_items as (
    select * from {{ ref('stg_sale_items') }}
),
sale_by_employee as (
    select
        sales.sale_id,
        sales.employee_id,
        sales.client_id,
        sales.sale_date,
        sale_items.sale_item_id,
        sale_items.product_id,
        sale_items.quantity,
        sale_items.unit_price,
        (sale_items.quantity * sale_items.unit_price) as total_sale_item
    from sale_items
    inner join sales on sales.sale_id = sale_items.sale_id
)
select * from sale_by_employee