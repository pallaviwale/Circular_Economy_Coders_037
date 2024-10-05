import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor_sales_dashboard
from typing import List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import calendar
import altair as alt
import plotly.graph_objects as go

#Define Page configuration
st.set_page_config(layout="wide")

#st.title("📊 Sales Dashboard")
alt.themes.enable("dark")
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
    <h1 class="styled-title">📊Sales Team Dashboard</h1>
""", unsafe_allow_html=True)

@st.cache_data
def load_data() -> pd.DataFrame:
    product_category_name_translation_dataset = pd.read_csv("Ecommerce\\product_category_name_translation.csv")
    order_items_dataset = pd.read_csv('Ecommerce\\olist_order_items_dataset.csv')
    orders_dataset = pd.read_csv('Ecommerce\\olist_orders_dataset.csv')
    products_dataset = pd.read_csv("Ecommerce\\olist_products_dataset.csv")
    payment_method_data = pd.read_csv("Ecommerce\\olist_order_payments_dataset.csv")
    customer_data = pd.read_csv("Ecommerce\\olist_customers_dataset.csv")

    main_data = Preprocessor_sales_dashboard.prepare_data(products_dataset, product_category_name_translation_dataset, order_items_dataset, orders_dataset,payment_method_data,customer_data)

    return main_data

def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
    st.sidebar.header("Filters")

    selected_year = Preprocessor_sales_dashboard.multiselect("Select Year", data["Year"].unique())
    #selected_month = Preprocessor.multiselect("Select Month", data["Month"].unique())
    selected_product_category = Preprocessor_sales_dashboard.multiselect("Select Product Category", data["product_category_name_english"].unique())
    selected_state = Preprocessor_sales_dashboard.multiselect("Select State", data["customer_state"].unique())
    

    return selected_year, selected_state, selected_product_category

data = load_data()
selected_year, selected_state, selected_product_category = display_sidebar(data)

filtered_data = data.copy()

# GLobal Filtering
filtered_data = filtered_data[(filtered_data["Year"].isin(selected_year)) & (filtered_data["customer_state"].isin(selected_state)) & (filtered_data["product_category_name_english"].isin(selected_product_category))]

# Display metrics with custom cards

metric_card = """
    <div style="background-color: #5f5f5f; padding: 10px; border-radius: 10px;
                border: 1px solid #add568 ; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                text-align: center;">
        <h2 style="color: #add568 ; font-size: 2.5em;">{value}</h2>
        <p style="font-size: 1.2em; color: #add568 ;">{label}</p>
    </div>
"""

total_sales = filtered_data['price'].sum()
total_sales_in_millions = round(filtered_data['price'].sum() / 1000000, 2)
formatted_total_sales = f"{total_sales_in_millions:.2f}M"
total_orders = filtered_data['order_id'].nunique()
average_order_value_rounded = round(total_sales / total_orders / 1000, 2)
formatted_average_order_value = f"{average_order_value_rounded:.2f}K"
total_customers = filtered_data['customer_id'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card.format(value=formatted_total_sales, label="Total Sales"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card.format(value = total_orders, label="Total Orders"), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card.format(value=formatted_average_order_value, label="Average Order Value"), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card.format(value = total_customers, label="Total Customers"), unsafe_allow_html=True)

#Visualizations -

col1, col2 = st.columns([3,2],vertical_alignment="center")
with col1:
    # Line chart for Total Month-Year Sales
    #st.markdown('<h1 style="font-family: Arial; font-size: 24px; color: #add568; text-align: center;">Total Month-Year Sales</h1>', unsafe_allow_html=True)
    total_sales_data = filtered_data[['Year', 'Month_String', 'Month', 'price']].groupby(['Month', 'Year', 'Month_String'], as_index=False)['price'].sum()
    fig = px.line(total_sales_data, x="Month_String", y="price", color="Year", markers=True, color_discrete_sequence=["#FF69B4", "#FFD700", "#00FF00"], title="Total Month-Year Sales")
    # Customize colors and font sizes
    fig.update_layout(
        font=dict(family="Arial", size=14),
        title_font=dict(size=24, color="#add568"),
        title_x=0.33,
        xaxis_title="Month-Year",
        yaxis_title="Total Sales",
        legend_title="Year",
        legend_font=dict(size=12),
        height = 550
    )
    st.plotly_chart(fig, use_container_width=True)


with col2:
    
    c0,col2_c1,c100 = st.columns([1,98,1],vertical_alignment="top")
    with col2_c1:
        guage_data_2018 = data[data['Year']==2018]
        guage_data_2017 = data[data['Year']==2017]
        
        Sale_2017_Sep = guage_data_2017[guage_data_2017['Month']<=9].groupby('Year')['price'].sum().reset_index()
        Sale_2017_Sep_Val = Sale_2017_Sep['price'].values[0]
        Sale_2018_Sep = guage_data_2018[guage_data_2018['Month']<=9].groupby('Year')['price'].sum().reset_index()
        Sale_2018_Sep_Val = Sale_2018_Sep['price'].values[0]
        
        Sale_2017_Dec = guage_data_2017[guage_data_2017['Month']>9].groupby('Year')['price'].sum().reset_index()
        Sale_2017_Dec_Val = Sale_2017_Dec['price'].values[0]
        
        Sep_increase = Sale_2018_Sep_Val/Sale_2017_Sep_Val
        projected_dec_2018 = round(Sale_2017_Dec_Val * Sep_increase)
        forcast_value = round(Sale_2018_Sep_Val + projected_dec_2018)
	
		# Create a gauge chart
        fig = go.Figure(
			go.Indicator(
				value=forcast_value,
				mode="gauge+number",
				domain={"x": [0, 1], "y": [0, 1]},
				number={"suffix": " (Forecast)", "font.size": 15},
				gauge={
					"axis": {"range": [0, forcast_value * 1.25], "tickwidth": 1}, 
					"bar": {"color": "green"},
				},
			
			)
		)
        
        fig.update_layout(
			font=dict(family="Arial", size=12),
			height=250,
			margin=dict(l=10, r=10,t=90,b=10, pad=8),
            title = "Sales Forcast till 2018",
            title_font=dict(size=24, color="#add568"),
            title_x=0.25
		)
        
        st.plotly_chart(fig, use_container_width=True)

    c0,col2_c2,c100 = st.columns([1,98,1],vertical_alignment="center")

    with col2_c2:
        
        payment_method_data = filtered_data[filtered_data['payment_type'] != 'not_defined']
        payment_methods = payment_method_data.groupby("payment_type")["payment_value"].sum().sort_values(ascending = False).reset_index()
        #st.write(payment_methods)
        #st.write(payment_methods[payment_methods['payment_type']])
        # Enhanced Plotly Pie Chart for Review Score Distribution
        fig_payment_method = px.pie(
            payment_methods, 
            names="payment_type", 
            values="payment_value", 
            title="Payment Method Distribution", 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Viridis)

        # Customize colors and font sizes
        fig_payment_method.update_layout(
            font=dict(family="Arial", size=14),
            title_font=dict(size=24, color="#add568"),
            title_x=0.25,
            legend_font=dict(size=12),
            height = 380
        )
        fig_payment_method.update_traces(marker=dict(line=dict(color="black", width=1.5)))
        st.plotly_chart(fig_payment_method, use_container_width=True)


col3, col4 = st.columns(2)
with col3:
    top_states = filtered_data[["customer_state", "price"]].groupby("customer_state").sum().sort_values(by="price", ascending=False).head(10).reset_index()
    
    # Create a bar chart with 'customer_state' on the x-axis and 'price' on the y-axis
    fig = px.bar(top_states, x="customer_state", y="price", color="customer_state", title="Top States by Total Sales")

    fig.update_layout(
        font=dict(family="Arial", size=14),
        title_font=dict(size=24, color="#add568"),
        title_x=0.33,
        xaxis_title="Customer State",
        yaxis_title="Total Sales",
        legend_title="Customer State",
        legend_font=dict(size=12),
    )

    st.plotly_chart(fig, use_container_width=True, height=500)

with col4:
    top_product_categories = filtered_data.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).head(10).reset_index()

    # Create a pie chart using Plotly Express
    fig = px.pie(top_product_categories, names="product_category_name_english", values="price", title="Top Product Categories", 
    color_discrete_sequence=px.colors.sequential.PuRd)

    # Customize colors and font sizes
    fig.update_layout(
        font=dict(family="Arial", size=14),
        title_font=dict(size=24, color="#add568"),
        title_x=0.33,
        legend_font=dict(size=12),
        height = 500
    )

    st.plotly_chart(fig, use_container_width=True)