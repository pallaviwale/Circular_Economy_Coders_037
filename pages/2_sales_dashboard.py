import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor

#set streamlit layout wide
st.set_page_config(layout="wide")

st.title("Sales Team Dashboad")

#Import all datasets
order_payment_data = pd.read_csv("Ecommerce\\olist_order_payments_dataset.csv")
product_category_name_translation_dataset = pd.read_csv("Ecommerce\\product_category_name_translation.csv")
order_items_dataset = pd.read_csv('Ecommerce\\olist_order_items_dataset.csv')
orders_dataset = pd.read_csv('Ecommerce\\olist_orders_dataset.csv')
products_dataset = pd.read_csv("Ecommerce\\olist_products_dataset.csv")

main_data = Preprocessor.prepare_data(products_dataset, product_category_name_translation_dataset, order_items_dataset, orders_dataset)

#sidebar
st.sidebar.title("Filters")

#Year, Month and product_category Filter
selected_year = Preprocessor.multiselect("Select Year", main_data["Year"].unique())
selected_month = Preprocessor.multiselect("Select Month", main_data["Month"].unique())
selected_product_category = Preprocessor.multiselect("Select Product Category", main_data["product_category_name_english"].unique())

#Global Filtering
filtered_main_df = main_data[(main_data["Year"].isin(selected_year)) & (main_data["Month"].isin(selected_month)) & (main_data["product_category_name_english"].isin(selected_product_category))]

#creating columns for KPI's
col1, col2, col3, col4 = st.columns(4)

#KPI for total sales
with col1:
    st.metric(label = "Total Sales", value = int(filtered_main_df["price"].sum()))


