import pandas as pd
import numpy as np
import streamlit as st


order_data = pd.read_csv("Ecommerce\\olist_orders_dataset.csv")
df = pd.DataFrame(order_data)
#convert date into datetime and get year,month and day
def fetch_time_features(df):
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_approved_at"] = pd.to_datetime(df["order_approved_at"])
    df["order_delivered_carrier_date"] = pd.to_datetime(df["order_delivered_carrier_date"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])
    df["Year"] = df["order_purchase_timestamp"].dt.year
    df["Month"] = df["order_purchase_timestamp"].dt.month
    df["Day"] = df["order_purchase_timestamp"].dt.day
    return df
fetch_time_features(df)
#Multiselect function
def multiselect(title,option_list):
    selected = st.sidebar.multiselect(title, option_list)
    select_all = st.sidebar.checkbox("Select all", value = True, key = title)
    if select_all:
        selected_options = option_list
    else:
        selected_options = selected
    return selected_options
def prepare_data(products_dataset, product_category_name_translation_dataset, order_items_dataset, orders_dataset):
    # Merge products dataset with product category translation dataset
    products_with_category = products_dataset.merge(product_category_name_translation_dataset, on='product_category_name')
    products_with_category.drop('product_category_name', axis=1, inplace=True)
    # Get product category in order items data from products_with_category
    order_items_data_merge = order_items_dataset.merge(products_with_category[['product_id', 'product_category_name_english']], on='product_id')
    # Merge with orders dataset to get order date information
    order_data_time_name = order_items_data_merge.merge(orders_dataset[['order_id', 'order_purchase_timestamp']], on='order_id')
    #order_data_time_name.head(3)
    #convert to datetime and take year, month,day
    order_data_time_name["order_purchase_timestamp"] = pd.to_datetime(order_data_time_name["order_purchase_timestamp"])
    order_data_time_name["Year"] = order_data_time_name["order_purchase_timestamp"].dt.year
    order_data_time_name["Month"] = order_data_time_name["order_purchase_timestamp"].dt.month
    order_data_time_name["Day"] = order_data_time_name["order_purchase_timestamp"].dt.day
    return order_data_time_name