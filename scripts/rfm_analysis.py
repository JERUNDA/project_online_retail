# Import core libraries for data analysis and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_csv(r"C:\online_retail_clean.csv")

# Show basic info about the dataframe (number of rows, columns, types)
df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 397884 entries, 0 to 397883
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype
---  ------       --------------   -----
 0   InvoiceNo    397884 non-null  int64
 1   StockCode    397884 non-null  object
 2   Description  397884 non-null  object
 3   Quantity     397884 non-null  int64
 4   InvoiceDate  397884 non-null  object
 5   UnitPrice    397884 non-null  float64
 6   CustomerID   397884 non-null  int64
 7   Country      397884 non-null  object
dtypes: float64(1), int64(3), object(4)
memory usage: 24.3+ MB

# Convert InvoiceDate from object (string) to datetime type for easier date calculations
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Verify the conversion
df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 397884 entries, 0 to 397883
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype
---  ------       --------------   -----
 0   InvoiceNo    397884 non-null  int64
 1   StockCode    397884 non-null  object
 2   Description  397884 non-null  object
 3   Quantity     397884 non-null  int64
 4   InvoiceDate  397884 non-null  datetime64[ns]
 5   UnitPrice    397884 non-null  float64
 6   CustomerID   397884 non-null  int64
 7   Country      397884 non-null  object
dtypes: datetime64[ns](1), float64(1), int64(3), object(3)
memory usage: 24.3+ MB

# Calculate the most recent date in the dataset (used as reference for Recency)
last_date = df['InvoiceDate'].max()

# Calculate Recency: days since last purchase for each customer
recency_df = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
recency_df['Recency'] = (last_date - recency_df['InvoiceDate']).dt.days

# Calculate Frequency: number of unique orders (InvoiceNo) per customer
frequency_df = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index().rename(columns={'InvoiceNo': 'Frequency'})

# Calculate Monetary: total spending per customer (Quantity * UnitPrice)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
monetary_df = df.groupby('CustomerID')['TotalPrice'].sum().reset_index().rename(columns={'TotalPrice': 'Monetary'})

# Merge Recency, Frequency, and Monetary into one DataFrame
rfm_df = recency_df.merge(frequency_df, on = 'CustomerID').merge(monetary_df, on = 'CustomerID')[['CustomerID', 'Recency', 'Frequency', 'Monetary']]
print(rfm_df.head())
   CustomerID  Recency  Frequency  Monetary
0       12346      325          1  77183.60
1       12347        1          7   4310.00
2       12348       74          4   1797.24
3       12349       18          1   1757.55
4       12350      309          1    334.40

# Assign scores (1-4) to R, F, M based on quartiles — higher is better
# For Recency, smaller values are better, so labels reversed implicitly by ordering
rfm_df['F_score'] = pd.qcut(rfm_df['Frequency'], 4, duplicates='drop').cat.codes + 1
rfm_df['R_score'] = pd.qcut(rfm_df['Recency'], 4, duplicates='drop').cat.codes + 1
rfm_df['M_score'] = pd.qcut(rfm_df['Monetary'], 4, duplicates='drop').cat.codes + 1

# Calculate combined RFM score
rfm_df['RFM_Score'] = rfm_df['R_score'] + rfm_df['F_score'] + rfm_df['M_score']

# Define segmentation conditions based on R, F, M scores
conditions = [(rfm_df['R_score'] >= 3) & (rfm_df['F_score'] >= 3) & (rfm_df['M_score'] >= 3), (rfm_df['R_score'] >=\ 3) & (rfm_df['F_score'] <= 2), (rfm_df['R_score'] <= 2) & (rfm_df['F_score'] >= 3)]
choices = ['Loyal', 'New', 'Leaving']

# Apply segmentation based on conditions; default segment is 'Low activity'
rfm_df['Segment'] = np.select(conditions, choices, default='Low activity')

# Print counts of customers in each segment
print(rfm_df['Segment'].value_counts())
Segment
New             2036
Low activity    1434
Leaving          758
Loyal            110
Name: count, dtype: int64

# Show average R, F, M metrics per segment (rounded)
print(rfm_df.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1))
              Recency  Frequency  Monetary
Segment
Leaving          13.4       13.4    7345.3
Low activity     22.5        2.7    1072.0
Loyal            96.2        8.0    3059.0
New             169.0        1.8     722.0

# Set seaborn plot style for better visuals
sns.set(style='whitegrid')

# Create a figure with 3 horizontal subplots for R, F, M distributions
fig, axs = plt.subplots(1, 3, figsize=(18,5))

# Plot Recency distribution histogram
sns.histplot(rfm_df['Recency'], bins=30, ax=axs[0], color='skyblue')
axs[0].set_title('Recency Distribution (Days Since Last Purchase)')

# Plot Frequency distribution histogram
sns.histplot(rfm_df['Frequency'], bins=30, ax=axs[1], color='lightgreen')
axs[1].set_title('Frequency Distribution (Order Frequency)')

# Plot Monetary distribution histogram
sns.histplot(rfm_df['Monetary'], bins=30, ax=axs[2], color='salmon')
axs[2].set_title('Monetary Distribution (Purchase Amount)')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show histograms
plt.show()

# Select top 20 customers by total monetary value
top_clients = rfm_df.sort_values('Monetary', ascending=False).head(20)

# Create a bar plot for top clients by revenue
plt.figure(figsize=(12,6))
sns.barplot(data=top_clients, x='CustomerID', y='Monetary', palette='viridis')
plt.xticks(rotation=45)
plt.title('Top 20 Clients by Revenue')
plt.xlabel('CustomerID')
plt.ylabel('Revenue')
plt.show()

# Extract month and year from InvoiceDate for monthly analysis
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

# Count number of unique orders per month
orders_per_month = df.groupby('InvoiceMonth')['InvoiceNo'].nunique().reset_index()

# Convert period to timestamp for plotting
orders_per_month['InvoiceMonth'] = orders_per_month['InvoiceMonth'].dt.to_timestamp()

# Plot the monthly number of orders over time
plt.figure(figsize=(14,6))
sns.lineplot(data=orders_per_month, x='InvoiceMonth', y='InvoiceNo')
plt.title('Number of orders by month')
plt.xlabel('Month')
plt.ylabel('Number of orders')
plt.show()

# Calculate correlation matrix between R, F, M variables
corr = rfm_df[['Recency','Frequency','Monetary']].corr()

# Plot heatmap to visualize correlations
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation between R, F, M')
plt.show()

# Create boxplots for detecting outliers in R, F, M metrics
fig, axs = plt.subplots(1, 3, figsize=(18,5))

# Boxplot for Recency
sns.boxplot(x=rfm_df['Recency'], ax=axs[0], color='skyblue')
axs[0].set_title('Boxplot Recency')

# Boxplot for Frequency
sns.boxplot(x=rfm_df['Frequency'], ax=axs[1], color='lightgreen')
axs[1].set_title('Boxplot Frequency')

# Boxplot for Monetary
sns.boxplot(x=rfm_df['Monetary'], ax=axs[2], color='salmon')
axs[2].set_title('Boxplot Monetary')

# Adjust layout spacing and display boxplots
plt.tight_layout()
plt.show()
