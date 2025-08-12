# Project Online Retail — Customer Segmentation and RFM Analysis

## Overview

This project analyzes customer behavior using the Online Retail dataset. 
The project aims to identify top-selling products, customer purchasing patterns, and seasonal sales trends to support data-driven marketing and inventory decisions.
I apply RFM (Recency, Frequency, Monetary) analysis to segment customers and gain insights for marketing strategies.  
The project includes data cleaning, loading data into PostgreSQL, running SQL queries for analysis, and visualizing results.

## Key Insights

Top-selling products: Certain gift items and decorative products consistently generate the highest revenue.
Customer segmentation: RFM analysis identified a small but highly valuable group of loyal customers.
Seasonality: Peak sales occur in November–December, indicating strong holiday-related purchasing patterns.
High-value customers: Top 5% of customers contribute to over 50% of total revenue.

## Project Structure
```
project_online_retail/
│
├── data/
│ ├── raw/ Online_Retail.xlsx # Original raw Excel data files
│ ├── clean/ online_retail_clean.csv # Cleaned CSV files ready for analysis
│
├── scripts/ # Python scripts for data processing and analysis
│ ├── 01_load_to_postgres_and_data_cleaning.py
│ ├── rfm_analysis.py
│
├── sql/ # SQL queries for analysis in PostgreSQL
│ ├── analysis_queries.sql
│ ├── analysis_queries2.sql
│
├── visuals/ # Generated visualizations 
│ ├── number_of_orders_by_month.png
│ ├── rfm.png
│ ├── rfm_boxplots.png
│ ├── rfm_correlation.png
│ ├── top20byRevenue.png
│
├── README.md # This file
```

## Data Description

- **Raw data:** Original online retail sales data in Excel format.
- **Clean data:** Preprocessed and cleaned CSV files used for analysis and loading into PostgreSQL and Python.

## Scripts

- `01_load_to_postgres_and_data_cleaning.py`  
  Cleans raw data and loads it into the PostgreSQL database.
- `rfm_analysis.py`  
  Performs RFM analysis on the cleaned data, segments customers, and generates visualizations.

## PostgreSQL SQL Queries

- Stored in `sql/` folder, contain analytical queries for customer segmentation and business insights.

## Visualizations

- Histograms of R, F, M metrics.
- Top clients by revenue bar plot.
- Time series of monthly orders.
- Correlation heatmaps and boxplots for anomaly detection.

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/project_online_retail.git
cd project_online_retail
```

2. Create a Python virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Prepare your PostgreSQL database (create database, set up user).
5. Run data cleaning and loading script:

```bash
python scripts/01_load_to_postgres_and_data_cleaning.py
```

6. Run RFM analysis and visualization:

```bash
python scripts/rfm_analysis.py
```

## Usage
- Modify the scripts if necessary to connect to your PostgreSQL instance.  
- Explore the provided SQL queries for additional insights.  
- Visualize customer segments and behaviors to support marketing and business decisions.  

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.  

## License
Specify your license here (e.g., MIT, GPL, etc.).  
