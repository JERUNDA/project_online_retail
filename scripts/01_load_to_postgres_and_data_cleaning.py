# Import the pandas library for data manipulation and analysis
import pandas as pd

# Import the create_engine function from SQLAlchemy to establish database connections
from sqlalchemy import create_engine

# Define the path to the Excel file
file_path = r"C:\Online_Retail.xlsx"

# Read Excel file into a pandas DataFrame
df = pd.read_excel(file_path)

# Replace commas with dots in 'UnitPrice' to fix decimal format, then convert to numeric
df['UnitPrice'] = df['UnitPrice'].astype(str).str.replace(',', '.', regex=False)
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')

# Convert 'Quantity' column to numeric, coercing errors to NaN
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Convert 'CustomerID' to numeric with nullable integer type (allows NA values)
df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce').astype('Int64')

# Convert 'InvoiceDate' to datetime, coercing invalid parsing to NaT
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Database connection parameters (fill in your credentials)
username = ''
password = ''
host = ''
port = ''
database = ''

# Create SQLAlchemy engine for PostgreSQL connection
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

# Write the DataFrame to a SQL table named 'online_retail', replacing it if exists
df.to_sql('online_retail', engine, if_exists='replace', index=False)



# Execute SQL query to read data back from the database into a DataFrame.
# The query selects only rows where Quantity and UnitPrice are positive,
# and CustomerID is not null — effectively filtering out invalid or incomplete records.
# This step happens after the initial data upload and table creation in the database.
clean_df = pd.read_sql(""" select * from online_retail
... where "Quantity" > 0
... and "UnitPrice" > 0
... and "CustomerID" is not null;""", engine)

# Save the cleaned DataFrame to a CSV file with semicolon separator and without the index column
clean_df.to_csv(r'C:\online_retail_clean.csv', index = False, sep = ';')
