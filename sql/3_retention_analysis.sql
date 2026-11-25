-- Question 3: Retention Analysis
-- A customer is labelled 'Churned' if their last purchase is more than 6 months
-- before the most recent order date in the dataset, otherwise 'Active'.
-- Only customers whose first purchase is older than 6 months are included,
-- so very recent customers are not misclassified.
-- Depends on the cohort_analysis view (see 0_create_cohort_view.sql).

WITH customer_last_purchase AS (
    SELECT
        customerkey,
        orderdate,
        ROW_NUMBER() OVER (PARTITION BY customerkey ORDER BY orderdate DESC) AS rn,
        first_purchase,
        cohort_year
    FROM cohort_analysis
),
churned_customers AS (
    SELECT
        customerkey,
        orderdate AS last_purchase_date,
        cohort_year,
        CASE
            WHEN orderdate < (SELECT MAX(orderdate) FROM sales) - INTERVAL '6 months' THEN 'Churned'
            ELSE 'Active'
        END AS customer_status
    FROM customer_last_purchase
    WHERE rn = 1
        AND first_purchase < (SELECT MAX(orderdate) FROM sales) - INTERVAL '6 months'
)
SELECT
    cohort_year,
    customer_status,
    COUNT(customerkey) AS num_customers,
    SUM(COUNT(customerkey)) OVER(PARTITION BY cohort_year) AS total_customers,
    ROUND(COUNT(customerkey) / SUM(COUNT(customerkey)) OVER(PARTITION BY cohort_year), 2) AS cohort_percentage
FROM churned_customers
GROUP BY
    cohort_year,
    customer_status
ORDER BY
    cohort_year,
    customer_status;
