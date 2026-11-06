-- E-commerce Sales & Business Analytics
-- Run these queries after importing ecommerce_orders.csv into a table named orders.

-- 1. Overall business KPIs (delivered orders only)
SELECT
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(revenue) AS average_order_value
FROM orders
WHERE order_status = 'Delivered';

-- 2. Monthly revenue trend
SELECT
    EXTRACT(YEAR FROM order_date) AS sales_year,
    EXTRACT(MONTH FROM order_date) AS sales_month,
    SUM(revenue) AS monthly_revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY sales_year, sales_month
ORDER BY sales_year, sales_month;

-- 3. Best-performing product categories
SELECT category, SUM(revenue) AS revenue, SUM(profit) AS profit
FROM orders
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY revenue DESC;

-- 4. Revenue by region
SELECT region, SUM(revenue) AS revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY region
ORDER BY revenue DESC;

-- 5. Top 10 products
SELECT product, SUM(quantity) AS units_sold, SUM(revenue) AS revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;

-- 6. Return and cancellation rate
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status;
