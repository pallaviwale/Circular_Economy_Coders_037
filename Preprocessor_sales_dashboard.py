import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

order_data = pd.read_csv("Ecommerce\\olist_orders_dataset.csv")
df = pd.DataFrame(order_data)

#Multiselect function
def multiselect(title,option_list):
    selected = st.sidebar.multiselect(title, option_list)
    select_all = st.sidebar.checkbox("Select all", value = True, key = title)
    if select_all:
        selected_options = option_list
    else:
        selected_options = selected
    return selected_options

#Product Category Sales

product_category_name_translation_dataset = pd.read_csv("Ecommerce\\product_category_name_translation.csv")
order_items_dataset = pd.read_csv('Ecommerce\\olist_order_items_dataset.csv')
orders_dataset = pd.read_csv('Ecommerce\\olist_orders_dataset.csv')
products_dataset = pd.read_csv("Ecommerce\\olist_products_dataset.csv")
payment_method_data = pd.read_csv("Ecommerce\\olist_order_payments_dataset.csv")
customer_data = pd.read_csv("Ecommerce\\olist_customers_dataset.csv")

def prepare_data(products_dataset, product_category_name_translation_dataset, order_items_dataset, orders_dataset,payment_method_data,customer_data):
    # Merge products dataset with product category translation dataset
    products_with_category = products_dataset.merge(product_category_name_translation_dataset, on='product_category_name')
    products_with_category.drop('product_category_name', axis=1, inplace=True)

    # Get product category in order items data from products_with_category
    order_items_data_merge = order_items_dataset.merge(products_with_category[['product_id', 'product_category_name_english']], on='product_id')

    # Merge with orders dataset to get order date information
    order_data_time_name = order_items_data_merge.merge(orders_dataset[['order_id', 'order_purchase_timestamp','customer_id']], on='order_id')

    #order_data_time_name.head(3)

    #merge order payment data with order items data
    order_data_time_name = order_data_time_name.merge(payment_method_data[['order_id', 'payment_type', 'payment_value']], on='order_id')
    
    #merge data to get customer city and state
    order_data_time_name = order_data_time_name.merge(customer_data[['customer_id', 'customer_city', 'customer_state']], on='customer_id')

    #convert to datetime and take year, month,day
    order_data_time_name["order_purchase_timestamp"] = pd.to_datetime(order_data_time_name["order_purchase_timestamp"], format = "mixed")

    order_data_time_name["Year"] = order_data_time_name["order_purchase_timestamp"].dt.year
    order_data_time_name["Month"] = order_data_time_name["order_purchase_timestamp"].dt.month
    order_data_time_name["Day"] = order_data_time_name["order_purchase_timestamp"].dt.day
    order_data_time_name["Month_String"] = order_data_time_name["order_purchase_timestamp"].dt.month_name()

    return order_data_time_name

def kpi_metrics_data(orders_dataset, order_items_dataset, payment_method_data, products_dataset, product_category_name_translation_dataset, customer_data):
    order_data = order_items_dataset.groupby(['order_id', 'product_id'])[['price', 'freight_value']].sum().reset_index()
    order_data = order_data.merge(orders_dataset[['order_id', 'customer_id', 'order_purchase_timestamp']], on='order_id')
    order_data = order_data.merge(customer_data[['customer_id','customer_unique_id', 'customer_city', 'customer_state']], on='customer_id')

    payment_data = payment_method_data.groupby('order_id')['payment_value'].sum().reset_index()
    payment_data = payment_data[payment_data['order_id'].isin(order_data['order_id'])]

    products_dataset = products_dataset.merge(product_category_name_translation_dataset, on='product_category_name').reset_index()

    kpi_data = order_data.merge(payment_data[['order_id', 'payment_value']], on='order_id')
    kpi_data['total_value'] = kpi_data['price']+kpi_data['freight_value']
    kpi_data = kpi_data.merge(products_dataset[['product_id','product_category_name_english']], on = 'product_id', how = 'left')
    kpi_data['product_category_name_english'] = kpi_data['product_category_name_english'].fillna('undefined')
    kpi_data["order_purchase_timestamp"] = pd.to_datetime(kpi_data["order_purchase_timestamp"], format = "mixed")

    kpi_data["Year"] = kpi_data["order_purchase_timestamp"].dt.year
    kpi_data["Month"] = kpi_data["order_purchase_timestamp"].dt.month
    kpi_data["Day"] = kpi_data["order_purchase_timestamp"].dt.day
    kpi_data["Month_String"] = kpi_data["order_purchase_timestamp"].dt.month_name()
    print(kpi_data['customer_unique_id'])
    #kpi_data.to_csv(r'C:\Users\Rushikesh Chougule\Desktop\Pallavi\Masai School\kpi_data_time2.txt', index = None, sep='#', mode='a')
    return kpi_data

#kpi_metrics_data(orders_dataset, order_items_dataset, payment_method_data, products_dataset, product_category_name_translation_dataset, customer_data)


#data =prepare_data(products_dataset, product_category_name_translation_dataset, order_items_dataset, orders_dataset,payment_method_data,customer_data)
#print(data.head(5))
#Payment Method Graph
#def payment_method_graph(payment_method_data):
    #a = payment_method_data[payment_method_data['payment_type'] != 'not_defined']
    #payment_methods = a.groupby("payment_type")["payment_value"].sum().sort_values(ascending = False).reset_index()

def payment_method_graph(payment_method_data):
  payment_methods = payment_method_data.groupby("payment_type")["payment_value"].sum().sort_values(ascending=False).reset_index()
  return payment_methods