import pandas as pd
import numpy as np
import streamlit as st

#convert date into datetime and get year,month and day
def fetch_time_features(df):
    df = df.dropna()
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_approved_at"] = pd.to_datetime(df["order_approved_at"])
    df["order_delivered_carrier_date"] = pd.to_datetime(df["order_delivered_carrier_date"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])
    df["Year"] = df["order_purchase_timestamp"].dt.year
    df["Month"] = df["order_purchase_timestamp"].dt.month
    df['Year_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    return df

def multiselect(title,options_list):
    selected = st.sidebar.multiselect(title, options_list)
    select_all = st.sidebar.checkbox("Select all", value = True, key = title)
    if select_all:
        selected_options = options_list
    else:
        selected_options = selected
    return selected_options
