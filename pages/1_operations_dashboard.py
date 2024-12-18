import pandas as pd
import numpy as np
import streamlit as st
from Codes import Preprocessor_operations_dashboard as po
from typing import List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import calendar
import altair as alt
import plotly.graph_objects as go

#Define Page configuration
st.set_page_config(layout="wide")

alt.themes.enable("dark")

# Load datasets
order_data = pd.read_csv("olist_orders_dataset.csv")
df_payment = pd.read_csv("olist_order_payments_dataset.csv")
product_category_name_translation_dataset = pd.read_csv("product_category_name_translation.csv")
order_items_dataset = pd.read_csv('olist_order_items_dataset.csv')
df_order = pd.read_csv('olist_orders_dataset.csv')
products_dataset = pd.read_csv("olist_products_dataset.csv")

# Preprocess data
df_order = po.fetch_time_features(df_order)
df_order['order_purchase_timestamp'] = pd.to_datetime(df_order['order_purchase_timestamp'])
df_order['order_products_value'] = df_payment['payment_value'] * df_payment['payment_installments']

df_order = df_order.merge(order_items_dataset[['order_id', 'price','freight_value']], on='order_id')
df_order['total_price_value'] = df_order['price']+df_order['freight_value']
df_order = df_order[df_order['order_id'].isin(df_payment['order_id'])]

##
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');

    .styled-title {
        font-size: 35px;  /* Font size */
        text-align: center;
        color: #add568;   /* White font color */
        font-family: 'Poppins', sans-serif;  /* Custom Google Font */
         
        padding: 15px;
        
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);  /* Adds a subtle shadow */
    }
    </style>
    <h1 class="styled-title">Operations Team Dashboard</h1>
""", unsafe_allow_html=True)
##
# Set Streamlit layout
#st.set_page_config(layout="wide")
#st.title("Operation Team Dashboard")
# Sidebar Filters for Year and Month
st.sidebar.title("Filters")
all_years = df_order['order_purchase_timestamp'].dt.year.unique()
all_months = df_order['order_purchase_timestamp'].dt.month.unique()
select_all_years = st.sidebar.checkbox("Select All Years", value=True)
if select_all_years:
    selected_year = st.sidebar.multiselect("Select Year", all_years, default=all_years)
else:
    selected_year = st.sidebar.multiselect("Select Year", all_years)
select_all_months = st.sidebar.checkbox("Select All Months", value=True)
if select_all_months:
    selected_month = st.sidebar.multiselect("Select Month", all_months, default=all_months)
else:
    selected_month = st.sidebar.multiselect("Select Month", all_months)
# Filter data based on selections
filtered_df_order = df_order.copy()
if selected_year:
    filtered_df_order = filtered_df_order[filtered_df_order['order_purchase_timestamp'].dt.year.isin(selected_year)]
if selected_month:
    filtered_df_order = filtered_df_order[filtered_df_order['order_purchase_timestamp'].dt.month.isin(selected_month)]
# Calculate KPIs
total_revenue = filtered_df_order['total_price_value'].sum()
number_of_orders = filtered_df_order['order_id'].nunique()
aov = total_revenue / number_of_orders
total_sales = filtered_df_order['total_price_value'].sum()
total_sales_in_millions = round(filtered_df_order['total_price_value'].sum() / 1000000, 2)
formatted_total_sales = f"{total_sales_in_millions:.2f}M"
average_order_value_rounded = round(total_sales / number_of_orders)
#formatted_average_order_value = f"{average_order_value_rounded:.2f}K"
formatted_average_order_value = f"${average_order_value_rounded}"

total_freight_value = filtered_df_order['freight_value'].sum()
average_order_freight_value_rounded = round(total_freight_value / number_of_orders)
formatted_average_order_freight_value=f"${average_order_freight_value_rounded}"


# Display KPIs in one row
st.subheader("Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3,kpi_col4 = st.columns(4)
# Sales Over Time Analysis
filtered_df_order['order_purchase_date'] = filtered_df_order['order_purchase_timestamp'].dt.date
# # Convert 'order_date' to datetime if it's not already
if not pd.api.types.is_datetime64_any_dtype(filtered_df_order['order_purchase_date']):
    filtered_df_order['order_purchase_date'] = pd.to_datetime(filtered_df_order['order_purchase_date'])
monthly_data = filtered_df_order.groupby(filtered_df_order['order_purchase_date'].dt.to_period('M')).agg(
    {'order_products_value': 'sum', 'order_id': 'nunique'})
monthly_data['AOV'] = monthly_data['order_products_value'] / monthly_data['order_id']
monthly_data = monthly_data.reset_index()
monthly_data['order_purchase_date'] = monthly_data['order_purchase_date'].dt.to_timestamp()

# Monthly Total Sales
filtered_df_order['order_purchase_month'] = filtered_df_order['order_purchase_timestamp'].dt.to_period('M')
monthly_sales = filtered_df_order.groupby('order_purchase_month')['order_products_value'].sum().reset_index()
monthly_sales['order_purchase_month'] = monthly_sales['order_purchase_month'].dt.to_timestamp()
average_monthly_sales = monthly_sales['order_products_value'].mean()
rounded_average = round(average_monthly_sales, 2)
average_in_millions = rounded_average / 1000000
formatted_average = f"{average_in_millions:.2f}M"


monthly_orders = filtered_df_order.groupby('order_purchase_month')['order_id'].nunique().reset_index()
monthly_orders['order_purchase_month'] = monthly_orders['order_purchase_month'].dt.to_timestamp()
average_monthly_orders = monthly_orders['order_id'].mean()
rounded_order_average = round(average_monthly_orders)
#formatted_average_order = f"{rounded_average:.2f}M"



# Delivery Time Analysis
filtered_df_order['delivery_time'] = (
    filtered_df_order['order_delivered_customer_date'] - filtered_df_order['order_purchase_timestamp']
).dt.days
avg_delivery_time = filtered_df_order['delivery_time'].mean()
# st.subheader("Visual Insights")

chart_col1, chart_col2 = st.columns([30,70])
# # Plot Average Order Value Over Time  ## First plot
# Ensure 'order_purchase_timestamp' is in datetime format
monthly_data['order_purchase_timestamp'] = monthly_data['order_purchase_date']
# Extract year and month from 'order_purchase_timestamp'
monthly_data['year'] = monthly_data['order_purchase_timestamp'].dt.year
monthly_data['month'] = monthly_data['order_purchase_timestamp'].dt.month
# Pivot the data to have separate columns for each year's AOV
pivot_data = monthly_data.pivot_table(
    index='month',
    columns='year',
    values='AOV',
    aggfunc='mean'
).reset_index()
# # Plot Monthly Total Sales
# Ensure 'order_purchase_timestamp' is in datetime format
monthly_sales['order_purchase_timestamp'] = monthly_data['order_purchase_date']
monthly_sales['year'] = monthly_sales['order_purchase_timestamp'].dt.year
monthly_sales['month'] = monthly_sales['order_purchase_timestamp'].dt.month
#Pivot the data to have separate columns for each year's total sales
pivot_sales = monthly_sales.pivot_table(
    index='month',
    columns='year',
    values='order_products_value',
    aggfunc='sum'
).reset_index()

# Layout for Delivery Time Analysis
delivery_chart_col1, delivery_chart_col2 = st.columns(2,vertical_alignment="center")
# # Plot Average Delivery Time Over Time
monthly_avg_delivery_time = filtered_df_order.groupby('order_purchase_month')['delivery_time'].mean().reset_index()
monthly_avg_delivery_time['order_purchase_month'] = monthly_avg_delivery_time['order_purchase_month'].dt.to_timestamp()
# Ensure 'order_purchase_month' is in datetime format
monthly_avg_delivery_time['order_purchase_month'] = pd.to_datetime(monthly_avg_delivery_time['order_purchase_month'])
# Extract year and month from 'order_purchase_month'
monthly_avg_delivery_time['year'] = monthly_avg_delivery_time['order_purchase_month'].dt.year
monthly_avg_delivery_time['month'] = monthly_avg_delivery_time['order_purchase_month'].dt.month

# Pivot the data to have separate columns for each year's average delivery time
pivot_avg_delivery_time = monthly_avg_delivery_time.pivot_table(
    index='month',
    columns='year',
    values='delivery_time',
    aggfunc='mean'
).reset_index()

metric_card = """
    <div style="background-color: #5f5f5f; padding: 10px; border-radius: 10px;
                border: 1px solid #add568 ; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                text-align: center;">
        <h2 style="color: #add568 ; font-size: 2.5em;">{value}</h2>
        <p style="font-size: 1.2em; color: #add568 ;">{label}</p>
    </div>
"""
# Use different colors for different metrics
with kpi_col1:
    st.markdown(metric_card.format(value = number_of_orders, label="Total Orders"), unsafe_allow_html=True)
    #st.markdown(metric_card.format(value=formatted_total_sales, label="Total Revenue"), unsafe_allow_html=True)
with kpi_col2:
    st.markdown(metric_card.format(value=formatted_average_order_value, label="Average Order Value"), unsafe_allow_html=True)
    #st.markdown(metric_card.format(value = number_of_orders, label="Total Orders"), unsafe_allow_html=True)
with kpi_col3:
    st.markdown(metric_card.format(value=formatted_average_order_freight_value, label="Average Freight Value"), unsafe_allow_html=True)
with kpi_col4:
    st.markdown(metric_card.format(value=rounded_order_average, label="Average Monthly Orders"), unsafe_allow_html=True)
    
# Plot Order Delivered vs Cancelled
with chart_col1:
    order_status_data = filtered_df_order.groupby("order_status")["order_id"].nunique().sort_values(ascending=False).reset_index()

    total_order = order_status_data["order_id"].sum()
    delivered_order = order_status_data[order_status_data["order_status"]=="delivered"]["order_id"].sum()

    delivery_completed = round((delivered_order/total_order)*100,2)
    #st.write(total_order, delivered_order, delivery_completed)	
	# Create a gauge chart
    fig_delivery = go.Figure(
		go.Indicator(
			value=delivery_completed,
			mode="gauge+number",
			domain={"x": [0, 1], "y": [0, 1]},
			number={"suffix": "% (Order Delivered )", "font.size": 15},
			gauge={
				"axis": {"range": [0, 100], "tickwidth": 1}, 
				"bar": {"color": "yellow"},
			},
		
		)
	)
    
    fig_delivery.update_layout(
		font=dict(family="Arial", size=12),
		height=320,
		margin=dict(l=10, r=10,t=90,b=10, pad=8),
        title = "Order Delivery Percentage",  
	)
    
    st.plotly_chart(fig_delivery, use_container_width=True)


# Plot Monthly Total Sales
with chart_col2:
    #st.write("Monthly Total Sales")
    fig_sales = px.bar(pivot_sales, x='month', y=pivot_sales.columns[1:],
                        title="Monthly Total Sales",
                        labels={'value': 'Total Sales', 'month': 'Month'},
                        template="plotly_white")
    #fig_sales.update_traces(marker=dict(color='#00796B', line=dict(color='#004D40', width=1)))
    fig_sales.update_layout(xaxis_title="Months", yaxis_title="Sales",
                            legend_title="Year", font=dict(size=12),)
    st.plotly_chart(fig_sales)

# Plot Delivery Time Distribution
with delivery_chart_col1:
    #st.write("Delivery Time Distribution")
    delivery_time_counts = filtered_df_order['delivery_time'].value_counts().sort_index()
    fig_delivery_time = px.bar(delivery_time_counts, x=delivery_time_counts.index,
                                y=delivery_time_counts.values,
                                title="Delivery Time Distribution in Days",
                                labels={'x': 'Delivery Time in Days', 'y': 'Total Orders'},
                                template="plotly_white")
    fig_delivery_time.update_traces(marker_color='#FFAB40')
    st.plotly_chart(fig_delivery_time)
# Plot Average Delivery Time Over Time
with delivery_chart_col2:
    #st.write("Average Delivery Time Over Time")
    fig_avg_delivery_time = px.line(pivot_avg_delivery_time, x='month', y=pivot_avg_delivery_time.columns[1:],
                                      title="Average Delivery Time Over Time",
                                      labels={'value': 'Average Delivery Time', 'month': 'Month'},
                                      template="plotly_white")
    fig_avg_delivery_time.update_traces(line=dict(width=2))
    fig_avg_delivery_time.update_layout(xaxis_title="Months", yaxis_title="Days",
                                         legend_title="Year", font=dict(size=12))
    st.plotly_chart(fig_avg_delivery_time)
