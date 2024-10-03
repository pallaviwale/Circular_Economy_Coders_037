import pandas as pd
import numpy as np
import streamlit as st

#set streamlit layout wide
st.set_page_config(layout="wide")

st.title("Marketing Team Dashboad")

customers = pd.read_csv('//olist_customers_dataset.csv')
geolocation = pd.read_csv('olist_geolocation_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
orders = pd.read_csv('olist_orders_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
sellers = pd.read_csv('olist_sellers_dataset.csv')
category_translation = pd.read_csv('product_category_name_translation.csv')
# customer distribution by state
#customers = pd.read_csv('olist_customers_dataset.csv')
customer_dist = customers.groupby('customer_state').size().reset_index(name='No of Customers')
customer_dist
st.bar_chart(customer_dist.set_index('customer_state')['No of Customers'],x_label='State',y_label='No of customers' )

# Product Popularity and Revenue Insights
products = pd.merge(products,category_translation,on='product_category_name',how='left')
order_product_data = pd.merge(order_items, orders, on='order_id')
order_product_data = pd.merge(order_product_data, products, on='product_id')

# Total revenue by product
st.write('Total revenue by product') 
revenue_by_category = order_product_data.groupby('product_category_name_english')['price'].sum().reset_index().sort_values(by='price',ascending=False).reset_index(drop=True)
revenue_by_category


# Average review score per product category
reviews_orders = pd.merge(reviews, orders, on='order_id')
reviews_products = pd.merge(reviews_orders, order_items[['order_id', 'product_id']], on='order_id')
reviews_products = pd.merge(reviews_products, products[['product_id', 'product_category_name_english']], on='product_id')
st.write("Average review score per product category")
avg_review_score = reviews_products.groupby('product_category_name_english')['review_score'].mean().reset_index().sort_values(by='review_score',ascending=False).reset_index(drop=True)
avg_review_score

#  Average freight value
# Merge order items with sellers data on seller_id
order_items_sellers = pd.merge(order_items, sellers, on='seller_id')
st.write("Average freight value")
# Group by seller_state and calculate the average freight value
avg_freight_by_state = order_items_sellers.groupby('seller_state')['freight_value'].mean().reset_index().sort_values(by='freight_value',ascending=False).reset_index(drop=True)
avg_freight_by_state



# yearly monthly total orders 
# Convert order_purchase_timestamp to datetime format
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['Year_month'] = orders['order_purchase_timestamp'].dt.to_period('M')
# Group by year to calculate total orders per year

# Group by year and month to calculate total orders per month
monthly_orders = orders.groupby('Year_month').size().reset_index(name='total_orders')
monthly_orders
st.subheader('Yearly-Monthly Total Orders (Line Chart)')
st.line_chart(monthly_orders.set_index('Year_month')['total_orders'],x_label='Year_month',y_label='total_orders')


# KPI 's

total_sales_revenue = order_product_data['price'].sum()
total_orders = orders['order_id'].nunique()
average_order_value = total_sales_revenue / total_orders if total_orders > 0 else 0
total_reviews = reviews['review_id'].count()
average_review_score = reviews['review_score'].mean()

# Displaying KPIs
st.header("Key Performance Indicators (KPIs)")
st.metric("Total Sales Revenue", f"${total_sales_revenue:,.2f}")
st.metric("Total Orders", total_orders)
st.metric("Average Order Value", f"${average_order_value:,.2f}")
st.metric("Total Reviews", total_reviews)
st.metric("Average Review Score", round(average_review_score, 2))