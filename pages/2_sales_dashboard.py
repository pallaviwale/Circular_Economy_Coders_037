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

#Year Filter
st.sidebar.multiselect("Choose Year",main_data["Year"].unique())

#Month Filter
st.sidebar.multiselect("Choose Month",main_data["Month"].unique())

#Product Category Filter
st.sidebar.multiselect("Choose Product Category",main_data["product_category_name_english"].unique())
