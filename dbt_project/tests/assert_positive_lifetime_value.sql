-- This test will fail if any user has a negative lifetime value
select 
    user_id,
    total_lifetime_value
from {{ ref('dim_customers') }}
where total_lifetime_value < 0