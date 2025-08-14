-- top 10 products by total sales (in pounds sterling)
select Description,
sum(Quantity) as TotalQuantity,   -- total units sold for this product        
sum(Quantity * UnitPrice) as TotalSales   -- total sales amount for this product
from online_retail_clean
group by Description
order by TotalSales desc
limit 10;

-- top 10 products by total margin (using artificial margin = UnitPrice * 0.3)
select Description,
sum(Quantity) as TotalQuantity,  -- total units sold for this product
sum(Quantity * (UnitPrice * 0.3)) as TotalMargin  -- total margin amount for this product
from online_retail_clean
group by Description
order by TotalMargin desc
limit 10;

-- monthly revenue, sorted from highest to lowest
select date_trunc('month', InvoiceDate) as month,
sum(Quantity * UnitPrice) as revenue
from online_retail_clean
group by month
order by revenue desc;

-- yearly revenue
select date_trunc('year', InvoiceDate) as year,
sum(Quantity * UnitPrice) as revenue
from online_retail_clean
group by year;

-- monthly revenue with % change from previous month
with monthly_revenue as (
select date_trunc('month', InvoiceDate) as month, -- truncate date to month level
sum(Quantity * UnitPrice) as revenue  -- total monthly revenue
from online_retail_clean
group by month
)
select month,
revenue,
lag(revenue) over (order by month) as prev_revenue,   -- revenue from previous month
round( case
when lag(revenue) over (order by month) is null then null   -- no previous month for first row
else (revenue - lag(revenue) over (order by month))
/ lag(revenue) over (order by month) * 100 end, 2) as pct_change   -- % change formula
from monthly_revenue
order by month;

-- number of unique customers per month
select date_trunc('month', InvoiceDate) as month,   -- truncate date to month level
count(distinct CustomerID) as unique_customer       -- count of unique customers in that month
from online_retail_clean
group by month;

-- calculate monthly revenue, unique customers, and count of missing CustomerIDs
with monthly_stats as (
select date_trunc('month', InvoiceDate) as month,  -- truncate date to month level
sum(Quantity * UnitPrice) as revenue,     -- total monthly revenue
count(distinct CustomerID) as unique_customer   -- number of unique customers per month
from online_retail_clean
group by month
),
missing_customers as (
select count (*) as missing_customer_count   -- count rows with missing CustomerID
from online_retail_clean
where  CustomerID is null
)
select ms.month,
ms.revenue,
ms.unique_customer,
round (ms.revenue::numeric / nullif(ms.unique_customer, 0), 2) as avg_revenue_per_customer,  -- average revenue per unique customer
mc.missing_customer_count    -- same missing customer count for all months (via CROSS JOIN)
from monthly_stats ms
cross join missing_customers mc   -- add single missing_customer_count row to each month
order by ms.month;

-- count returns based on InvoiceNo starting with 'C'
select count(*) as returns_count
from online_retail_clean
where InvoiceNo like 'C%';

-- count returns based on negative quantity
select count(*) as returns_count
from online_retail_clean
where Quantity < 0;

-- monthly sales vs returns, and % of returns from total transactions
with monthly_stats as (
select date_trunc('month', InvoiceDate) as month,  -- truncate date to month
count(*) FILTER (where InvoiceNo not like 'C%') as sales_count,    -- number of sales transactions
count (*) filter (where InvoiceNo like 'C%') as returns_count    -- number of return transactions
from online_retail_clean
group by month
)
select
month,
sales_count,
returns_count,
round(returns_count::numeric 
/ nullif(sales_count + returns_count, 0) * 100, 2) as pct_returns  -- percentage of returns out of all transactions
from monthly_stats
order by month;
