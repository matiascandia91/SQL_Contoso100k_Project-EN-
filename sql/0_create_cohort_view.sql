-- Creates the cohort_analysis view used by the analysis queries.
-- One row per customer per order date, with revenue, number of order lines,
-- customer attributes, first purchase date and cohort year.

CREATE OR REPLACE VIEW public.cohort_analysis
AS WITH customer_revenue AS (
         SELECT s.customerkey,
            s.orderdate,
            sum(s.quantity::double precision * s.netprice * s.exchangerate) AS total_revenue,
            count(s.orderkey) AS numb_order,
            c.countryfull,
            c.age,
            c.givenname,
            c.surname
           FROM sales s
             LEFT JOIN customer c ON c.customerkey = s.customerkey
          GROUP BY s.customerkey, s.orderdate, c.countryfull, c.age, c.givenname, c.surname
        )
 SELECT customerkey,
    orderdate,
    total_revenue,
    numb_order,
    countryfull,
    age,
    concat(TRIM(BOTH FROM givenname), ' ', TRIM(BOTH FROM surname)) AS full_name,
    min(orderdate) OVER (PARTITION BY customerkey) AS first_purchase,
    EXTRACT(year FROM min(orderdate) OVER (PARTITION BY customerkey)) AS cohort_year
   FROM customer_revenue cr;
