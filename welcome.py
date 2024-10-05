import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(layout="wide")

alt.themes.enable("dark")
# Set page configuration
st.set_page_config(page_title="E-commerce Dashboard Overview", page_icon=":bar_chart:", layout="wide")
# Add CSS for custom styling with a background color for the entire page
st.markdown("""
    <style>
        /* Set a background color for the entire page */
        body {
            background-color: #F0F2F5;
            font-family: 'Arial', sans-serif;
        }
        .main-header {
            background-color: #28b78d; /* Primary color */
            padding: 8px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .main-header h1 {
            color: #FFFFFF;
            font-size: 40px;
            font-weight: bold;
        }
        .header-description {
            color: #FFFFFF;
            font-size: 18px;
            margin-top: 10px;
        }
        .subheader-text {
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            background: #5f5f5f; /* Accent color */
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .dashboard-info {
            font-size: 18px;
            color: #FFFFFF;
            
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .footer-note {
            font-size: 14px;
            color: #6C757D;
            text-align: center;
            margin-top: 50px;
        }
        /* Sidebar logo at the bottom */
        .sidebar-logo {
            position: fixed;
            bottom: 20px;
            width: 240px;
            padding: 10px;
            background-color: #FFFFFF;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Include the project logo at the bottom of the sidebar
st.sidebar.image("EcomDash_Logo.png", use_column_width=True)

col1,col2 = st.columns([10,90],vertical_alignment="center")
with col1:
# Header with logo on the main page
    st.image("EcomDash_Logo.png", width=150)  # Adjust size as needed

with col2:
# Header with background styling
    st.markdown("""
        <div class="main-header">
            <h1>Welcome to EcomDash</h1>
            <p class="header-description">Your one-stop solution for e-commerce analytics and insights</p>
        </div>
    """, unsafe_allow_html=True)

# Welcome message with background color
st.markdown("""
    <div class="dashboard-info">
        This application provides comprehensive insights into various aspects of our e-commerce operations.
        Navigate through the different dashboards to explore detailed analytics for each team, identify key trends,
        and make data-driven decisions to improve business performance.
    </div>
""", unsafe_allow_html=True)
# Overview of dashboards
st.header("Dashboards Overview")
# Operations Team Dashboard
st.markdown('<h2 class="subheader-text">Operations Team Dashboard</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="dashboard-info">
- **Average Order Value Over Time**: Track the average value of orders over different time periods to understand customer spending patterns and evaluate pricing strategies.<br>
- **Monthly Total Sales**: Monitor total sales generated each month to identify seasonality and plan inventory accordingly.<br>
- **Delivery Time Distribution**: Analyze the distribution of delivery times to ensure timely deliveries and identify bottlenecks in logistics.<br>
- **Average Delivery Time Over Time**: Observe trends in average delivery time to improve fulfillment efficiency.
</div>
""", unsafe_allow_html=True)
# Sales Team Dashboard
st.markdown('<h2 class="subheader-text">Sales Team Dashboard</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="dashboard-info">
- **Total Monthly Year Sales**: View total sales for each month and year to evaluate overall performance and compare growth across periods.<br>
- **Sales Forecast**: Predict future sales based on historical data to aid in setting realistic targets.<br>
- **Top States by Total Sales**: Identify states with the highest sales to tailor marketing campaigns.<br>
- **Top Product Categories**: Focus on best-selling product categories to optimize inventory and prioritize marketing efforts.
</div>
""", unsafe_allow_html=True)
# Marketing Team Dashboard
st.markdown('<h2 class="subheader-text">Marketing Team Dashboard</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="dashboard-info">
- **Review Score Distribution**: Visualize review score distribution to gauge customer satisfaction levels and identify improvement areas.<br>
- **Average Review Score per Product Category**: Compare average review scores across categories to assess strengths and weaknesses.<br>
- **Customer Acquisition Over Time**: Track new customer acquisition to evaluate marketing effectiveness.<br>
- **Customer Distribution by State**: Analyze geographical distribution of customers to identify key markets.<br>
- **Average Freight Value by Seller State**: Understand logistics costs and optimize shipping strategies.
</div>
""", unsafe_allow_html=True)
# Footer
st.markdown("""
    ---
    <p class="footer-note">**Note**: Use the sidebar to navigate to specific dashboards for more detailed insights and make informed decisions to optimize business operations.</p>
""", unsafe_allow_html=True)