select sale_id, product_id, quantity, price, count(*)
from raw.sale_items si 
group by sale_id, product_id, quantity, si.price 
having count(*) > 1