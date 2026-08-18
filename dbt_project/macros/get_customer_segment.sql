{% macro get_customer_segment(mrr_column) %}
    case 
        when {{ mrr_column }} >= 99 then 'Enterprise Tier'
        when {{ mrr_column }} >= 29 then 'Professional Tier'
        else 'Basic Tier'
    end
{% endmacro %}