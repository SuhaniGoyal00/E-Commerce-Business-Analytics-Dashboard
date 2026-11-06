# E-commerce Sales & Business Analytics Dashboard

## Project overview
An entry-level business analytics project that explores e-commerce order data and turns it into business insights. The dashboard covers revenue, profit, orders, customers, monthly trends, categories, regions, top products, payment methods and order status.

## Tech stack
- Python
- Pandas
- Streamlit
- Plotly
- SQL

## Dataset
`ecommerce_orders.csv` contains 1,200 **synthetic** order records covering 2025. It is generated for this portfolio project; it is not real customer or company data.

## Run locally
1. Install Python 3.10 or newer.
2. Extract this project folder.
3. Open a terminal in this folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
6. Streamlit will provide a local URL, usually http://localhost:8501.

## SQL practice
Open `analysis_queries.sql` and run the queries after importing the CSV into a SQL table named `orders`. SQL syntax may need small changes depending on MySQL, PostgreSQL or SQLite.

## Key business questions
1. Which product category generates the most revenue?
2. Which region performs best?
3. How does revenue change month by month?
4. Which products are the top revenue contributors?
5. What share of orders are returned or cancelled?
6. What actions could improve revenue and profitability?

## Portfolio note
Be transparent in interviews that the dataset is synthetic. Explain the business questions, analysis, dashboard filters, and recommendations in your own words. Do not present generated data as actual company data.
