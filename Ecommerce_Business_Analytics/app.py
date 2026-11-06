import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Business Analytics", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv("ecommerce_orders.csv", parse_dates=["order_date"])
    return data

df = load_data()
st.title("📊 E-commerce Sales & Business Analytics")
st.caption("An interactive dashboard to explore sales, profit, products, customers and operations.")

with st.sidebar:
    st.header("Dashboard filters")
    min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    categories = sorted(df["category"].unique())
    selected_categories = st.multiselect("Category", categories, default=categories)
    regions = sorted(df["region"].unique())
    selected_regions = st.multiselect("Region", regions, default=regions)
    statuses = sorted(df["order_status"].unique())
    selected_statuses = st.multiselect("Order status", statuses, default=["Delivered"])

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["order_date"].dt.date >= start_date) &
    (df["order_date"].dt.date <= end_date) &
    (df["category"].isin(selected_categories)) &
    (df["region"].isin(selected_regions)) &
    (df["order_status"].isin(selected_statuses))
].copy()

if filtered.empty:
    st.warning("No orders match these filters. Please change your selections.")
    st.stop()

total_revenue = filtered["revenue"].sum()
total_profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
customers = filtered["customer_id"].nunique()
avg_order_value = total_revenue / orders if orders else 0
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Unique customers", f"{customers:,}")
c5.metric("Profit margin", f"{profit_margin:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["revenue"].sum()
    fig = px.line(monthly, x="month", y="revenue", markers=True, title="Monthly revenue trend",
                  labels={"month":"Month", "revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    category_sales = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(category_sales, x="category", y="revenue", title="Revenue by category",
                 labels={"category":"Category", "revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    region_sales = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(region_sales, x="region", y="revenue", color="region", title="Revenue by region",
                 labels={"region":"Region", "revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    top_products = filtered.groupby("product", as_index=False).agg(
        revenue=("revenue","sum"), units_sold=("quantity","sum")
    ).sort_values("revenue", ascending=False).head(10)
    fig = px.bar(top_products.sort_values("revenue"), x="revenue", y="product", orientation="h",
                 title="Top 10 products by revenue", labels={"revenue":"Revenue (₹)", "product":"Product"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer and order insights")
a, b, c = st.columns(3)
a.metric("Average order value", f"₹{avg_order_value:,.0f}")
b.metric("Units sold", f"{filtered['quantity'].sum():,}")
delivered_share = (filtered["order_status"].eq("Delivered").mean() * 100)
c.metric("Delivered order share", f"{delivered_share:.1f}%")

payment = filtered["payment_method"].value_counts().rename_axis("payment_method").reset_index(name="orders")
fig = px.pie(payment, names="payment_method", values="orders", hole=.45, title="Orders by payment method")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Business recommendations")
best_category = category_sales.iloc[0]["category"]
best_region = region_sales.iloc[0]["region"]
best_product = top_products.iloc[0]["product"]
st.markdown(f"""
- **Category focus:** {best_category} currently contributes the highest revenue in the selected data. Review its inventory and marketing performance.
- **Regional opportunity:** {best_region} is the strongest region by revenue. Compare customer acquisition and delivery performance across other regions.
- **Product opportunity:** {best_product} is the leading product by revenue. Check whether its margin and stock availability can be improved.
- **Next analysis:** investigate returned and cancelled orders separately to understand potential revenue leakage.
""")

with st.expander("View filtered order data"):
    st.dataframe(filtered, use_container_width=True)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_ecommerce_orders.csv", mime="text/csv")

st.caption("Dataset is synthetic and created for learning/demo purposes. Currency is shown in INR (₹).")
