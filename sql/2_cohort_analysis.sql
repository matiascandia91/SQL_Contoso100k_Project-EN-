-- Question 2: Cohort Analysis
-- Depends on the cohort_analysis view (see 0_create_cohort_view.sql).

-- Title: Customer Revenue by Cohort (NOT adjusted for time in market)
SELECT
    cohort_year,
    SUM(total_revenue) AS total_net_revenue,
    COUNT(DISTINCT customerkey) AS total_customers,
    SUM(total_revenue) / COUNT(DISTINCT customerkey) AS customer_revenue
FROM cohort_analysis
GROUP BY
    cohort_year;

-- Title: Customer Revenue by Cohort (Adjusted for time in market)
WITH purchase_days AS (
    SELECT
        customerkey,
        total_revenue,
        orderdate - MIN(orderdate) OVER (PARTITION BY customerkey) AS days_since_first_purchase
    FROM cohort_analysis
)

SELECT
    days_since_first_purchase,
    SUM(total_revenue) as total_revenue,
    SUM(total_revenue) / (SELECT SUM(total_revenue) FROM cohort_analysis) * 100 as percentage_of_total_revenue,
    SUM(SUM(total_revenue) / (SELECT SUM(total_revenue) FROM cohort_analysis) * 100) OVER (ORDER BY days_since_first_purchase) as cumulative_percentage_of_total_revenue
FROM purchase_days
GROUP BY days_since_first_purchase
ORDER BY days_since_first_purchase;

-- Title: Customer Revenue by Cohort (Adjusted for time in market) - Only First Purchase Date
SELECT
    cohort_year,
    SUM(total_revenue) AS total_revenue,
    COUNT(DISTINCT customerkey) AS total_customers,
    SUM(total_revenue) / COUNT(DISTINCT customerkey) AS customer_revenue
FROM cohort_analysis
WHERE orderdate = first_purchase
GROUP BY
    cohort_year;

-- Title: Monthly Net Revenue and Customers (3 Month Rolling Average)
-- Results are also saved in results/2d_monthly_trends.csv
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', orderdate)::date AS month,
        SUM(total_revenue) AS net_revenue,
        COUNT(DISTINCT customerkey) AS customers
    FROM cohort_analysis
    GROUP BY 1
)
SELECT
    month,
    net_revenue,
    customers,
    AVG(net_revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS revenue_3m_avg,
    AVG(customers)   OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS customers_3m_avg
FROM monthly
ORDER BY month;
