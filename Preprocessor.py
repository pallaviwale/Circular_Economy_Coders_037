import pandas as pd
import numpy as np
import streamlit as st

order_data = pd.read_csv("olist_orders_dataset.csv")
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