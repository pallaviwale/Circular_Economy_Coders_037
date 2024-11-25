import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import Preprocessor_marketing_dashboard as mb
import altair as alt
#set streamlit layout wide
st.set_page_config(layout="wide")

alt.themes.enable("dark")
# st.title("Marketing Team Dashboad")
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
    <h1 class="styled-title">Marketing Team Dashboard</h1>
""", unsafe_allow_html=True)


## Load datasets
customers = pd.read_csv('olist_customers_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
orders = pd.read_csv('olist_orders_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
sellers = pd.read_csv('olist_sellers_dataset.csv')
category_translation = pd.read_csv('product_category_name_translation.csv')
## merege datasets
product_trans=pd.merge(products,category_translation,on='product_category_name',how='left')
customers = pd.merge(customers,orders,on='customer_id',how='left')
customer_order = pd.merge(customers,order_items,on='order_id',how='left')

reviews=reviews.drop(columns=['review_comment_title','review_comment_message'])
customer_order = pd.merge(customer_order,reviews,on='order_id',how='left')
customer_order = pd.merge(customer_order,sellers,on='seller_id',how='left')
final_df = pd.merge(customer_order,product_trans,on='product_id',how='left')

df = mb.fetch_time_features(final_df)
# filtering 
selected_year_month = mb.multiselect("Select Year-Month", df["Year_month"].unique())
selected_product = mb.multiselect("Select Product", df["product_category_name_english"].unique())
selected_customer_state = mb.multiselect("Select Customer State", df["customer_state"].unique())
selected_seller_state = mb.multiselect("Select Seller State", df["seller_state"].unique())

# Global filtering
filtered_df = df[(df["Year_month"].isin(selected_year_month)) & (df["product_category_name_english"].isin(selected_product)) & (df["customer_state"].isin(selected_customer_state)) & (df["seller_state"].isin(selected_seller_state))]

# KPI 's
# total_sales_revenue = filtered_df['price'].sum()
# total_orders = filtered_df['order_id'].nunique()
# average_order_value = total_sales_revenue / total_orders if total_orders > 0 else 0
total_reviews = filtered_df['review_id'].count()
average_review_score = filtered_df['review_score'].mean()

metric_card = """
    <div style="background-color: #5f5f5f; padding: 5px; border-radius: 10px;
                border: 1px solid #add568 ; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                text-align: center;">
        <h2 style="color: #add568 ; font-size: 2.5em;">{value}</h2>
        <p style="font-size: 1.2em; color: #add568 ;">{label}</p>
    </div>
"""

# Display metrics with custom cards
col1,col2, col3,col4 = st.columns([1,4,4,1])

with col2:
    st.markdown(metric_card.format(value=total_reviews, label="Total Reviews"), unsafe_allow_html=True)

with col3:
    st.markdown(metric_card.format(value=round(average_review_score, 2), label="⭐ Average Review Score"), unsafe_allow_html=True)

st.markdown('---')

col3, col4 = st.columns(2)

with col3:
    st.markdown("<h3 style='color: #FF5733;'>Review Score Distribution</h3>", unsafe_allow_html=True)
    review_dist = df['review_score'].value_counts().sort_index()

# Enhanced Plotly Pie Chart for Review Score Distribution
    fig_reviews = px.pie(
        names=review_dist.index,  # Categories (review scores)
        values=review_dist.values,  # Values (counts)
        labels={'index': 'Review Score', 'y': 'Count'},
        title="Review Score Distribution",
        hole=0.4,  # This makes it a donut chart
        color_discrete_sequence=px.colors.sequential.Viridis,  # Custom color palette
    )

    # Customizing the layout for better appearance
    fig_reviews.update_layout(
        title={'x': 0.5, 'xanchor': 'center'},  # Centered title
        font=dict(size=14),  # Font size for better readability
        #plot_bgcolor="white",  # Background color
    )

    # Optionally, customize the trace for border around pie slices
    fig_reviews.update_traces(marker=dict(line=dict(color="black", width=1.5)))

    # Display the pie chart in Streamlit
    st.plotly_chart(fig_reviews, use_container_width=True)

with col4:
    #st.write("Average Review Score per Product Category")
    st.markdown("<h3 style='color: #FF5733;'>Average Review Score per Product Category</h3>", unsafe_allow_html=True)
    avg_review_score = filtered_df.groupby('product_category_name_english')['review_score'].mean().reset_index().sort_values(by='review_score',ascending=False).reset_index(drop=True)
    
    #Enhanced Plotly Bar Chart for Average Review Score by Product Category
    fig_avg_reviews = px.bar(
        avg_review_score,
        x='product_category_name_english',
        y='review_score',
        title="Average Review Score by Product Category",
        color_discrete_sequence=["#FFA15A"],
        labels={'product_category_name_english': 'Product Category', 'review_score': 'Average Score'}
        
    )
    
    fig_avg_reviews.update_layout(
        title={'x':0.5, 'xanchor': 'center'},
        xaxis_title="Product Category",
        yaxis_title="Average Review Score",
        #plot_bgcolor="white",
        font=dict(size=14),
        xaxis_tickangle=-45,
        bargap=0.2,
    )

    
    fig_avg_reviews.update_traces(marker_line_width=1.5, marker_line_color="black")
    
    st.plotly_chart(fig_avg_reviews, use_container_width=True)
   
st.markdown('---')
st.markdown("<h3 style='color: #FF5733;'>Customer Acquisition Over Time</h3>", unsafe_allow_html=True)
customer_acquisition = filtered_df.groupby('Year_month')['customer_unique_id'].nunique().reset_index()
customer_acquisition['Year_month'] = customer_acquisition['Year_month'].astype(str)
# Create a Plotly line chart for customer acquisition
fig_acquisition = px.line(
    customer_acquisition,
    x='Year_month',
    y='customer_unique_id',
    title="Customer Acquisition Over Time",
    labels={'Year_month': 'Month-Year', 'customer_unique_id': 'New Customers'},
    markers=True  # Add markers to the line for better visibility
)

# Customize the layout for a polished look
fig_acquisition.update_layout(
    title={'x':0.5, 'xanchor': 'center'},  # Center the title
    #plot_bgcolor='white',  # Set background to white
    xaxis_title="Month-Year",
    yaxis_title="New Customers",
    font=dict(size=14),  # Set font size for better readability
    xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
    hovermode="x",  # Hover mode to show info at each x point
)

# Customize the line appearance
fig_acquisition.update_traces(
    line_color='royalblue',  # Custom line color
    line_width=3,  # Thicker line for visibility
    marker=dict(size=8, symbol="circle", color="orange")  # Marker styling for data points
)

st.plotly_chart(fig_acquisition, use_container_width=True)

st.markdown('---')

# Customer distribution by state
col5, col6 = st.columns(2)

with col5:
    st.markdown("<h3 style='color: #FF5733;'>Customer Distribution By State</h3>", unsafe_allow_html=True)
    #st.write('Customer Distribution By State')
    # Prepare the data
    customer_dist = filtered_df.groupby('customer_state').size().reset_index(name='No of Customers').sort_values(by='No of Customers', ascending=False).reset_index()

    #Create a Plotly bar chart for Customer Distribution by State
    fig_customer_dist = px.bar(
        customer_dist, 
        x='customer_state', 
        y='No of Customers', 
        title="Customer Distribution By State",
        labels={'customer_state': 'State', 'No of Customers': 'Number of Customers'},
        color_discrete_sequence=['#636EFA'],  # Use a custom color
    )

    # Customize the layout for readability
    fig_customer_dist.update_layout(
        title={'x': 0.5, 'xanchor': 'center'},
        #plot_bgcolor='white',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        font=dict(size=14),
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig_customer_dist, use_container_width=True)

# Top 10 and Bottom 10 States with number of customers
with col6:
    st.markdown("<h3 style='color: #FF5733;'>Average Freight Value by Seller State</h3>", unsafe_allow_html=True)
# Average freight value by seller state
    avg_freight_by_state = filtered_df.groupby('seller_state')['freight_value'].mean().reset_index()

    # Create a Plotly bar chart for Average Freight Value by Seller State
    fig_freight_value = px.bar(
        avg_freight_by_state,
        x='seller_state',
        y='freight_value',
        title="Average Freight Value by Seller State",
        labels={'seller_state': 'State', 'freight_value': 'Freight Value'},
        color_discrete_sequence=['#FFA15A'],  # Custom color for bars
    )

    # Customize layout for better readability
    fig_freight_value.update_layout(
        title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        #plot_bgcolor='white',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        font=dict(size=14),  # Set font size for better clarity
        xaxis_title="Seller State",
        yaxis_title="Average Freight Value",
    )

# Display the chart in Streamlit
    st.plotly_chart(fig_freight_value, use_container_width=True)
