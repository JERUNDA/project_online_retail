-- count the total number of transactions
select count(*) from online_retail;

-- count the number of unique customers
select count(distinct "CustomerID") from online_retail;

-- find the earliest and latest invoice dates 
select min("InvoiceDate"), max("InvoiceDate") from online_retail;

-- count how many transactions are cancellations
select count(*) filter (where "InvoiceNo" like 'C%') as cancellation
from online_retail;

-- create a CTE (daily_status) aggregating data by customer and date
with daily_status as (
select
"CustomerID",
date("InvoiceDate") as order_date,  -- extract date part from InvoiceDate (discard time)

-- check if customer made a purchase that day (InvoiceNo not starting with 'C')
max(case when "InvoiceNo" not like 'C%' then 1 else 0 end) as bought,  

-- check if customer made a cancellation that day (InvoiceNo starting with 'C')
max(case when "InvoiceNo" like 'C%' then 1 else 0 end) as cancelled
from online_retail
group by "CustomerID", order_date
)

-- count how many customers had both a purchase and a cancellation on the same day
select count(*)
from daily_status
where bought = 1 
and cancelled = 1;

-- select all transactions where quantity and unit price are positive and CustomerID is not null
select * from online_retail 
where "Quantity" > 0
and "UnitPrice" > 0
and "CustomerID" is not null;