# Circular-Economy-Coders_037

# E-commerce Insights Dashboard
<img src="EcomDash_Logo.png" alt="EcomDash" width='200'/>
## Description
This project is an interactive, data-driven dashboard designed to provide insights for three key teams: Sales, Operations, and Marketing. The dashboard allows users to explore key metrics and trends related to sales performance, customer behavior, and operational efficiency using filters for products, months, and states. The application is built using Streamlit and deployed on Streamlit Cloud.

## Features by Team

### **Sales Team Insights**
- **Yearly-Monthly Sales**: Track sales trends over time.
- **Top States by Total Sales**: Identify regions with the highest sales.
- **Top Products**: See which products are most popular.
- **Payment Methods**: Analyze which payment methods are frequently used.
- **KPIs**:
  - Total Sales
  - Total Orders
  - Average Order Value
  - Total Customers

### **Operations Team Insights**
- **Average Order Value Over Time**: Track the changes in average order value.
- **Monthly Total Sales**: Measure sales performance over months.
- **Delivery Time Distribution**: Analyze how long deliveries take.
- **Average Delivery Time Over Time**: Track how delivery times are evolving.
- **KPIs**:
  - Total Revenue
  - Total Orders
  - Average Order Value
  - Average Monthly Sales

### **Marketing Team Insights**
- **Review Score Distribution**: Analyze customer reviews.
- **Average Review Score per Product**: See which products are performing best.
- **Customer Acquisition Over Time**: Track the growth of new customers.
- **Customer Distribution by State**: Visualize customer distribution across regions.
- **Average Freight Value by Seller State**: Understand shipping cost patterns.
- **KPIs**:
  - Total Reviews
  - Average Review Score

## Filtering Options
Users can filter the dashboard data using:
- **Product**: View specific product insights.
- **Month**: Analyze data over a selected time period.
- **State**: Focus on specific regions for sales and customer behavior.

## Project Structure

- `welcome.py`: The entry point for the app. Allows navigation between sales, operations, and marketing dashboards.
- `2_sales_dashboard.py`: Displays sales-related insights.
- `Preprocessor_sales_dashboard.py`: Handles data processing for the sales team.
- `1_operations_dashboard.py`: Displays operations-related insights.
- `Preprocessor_operations_dashboard.py`: Handles data processing for the operations team.
- `3_marketing_dashboard.py`: Displays marketing-related insights.
- `Preprocessor_marketing_dashboard.py`: Handles data processing for the marketing team.
- `EcomDash_Logo.png`: The logo displayed on the website.
- `requirements.txt`: Lists the Python dependencies needed for the project.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pallaviwale/Circular_Economy_Coders_037.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Circular_Economy_Coders_037
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run welcome.py
   ```

## Deployment on Streamlit
This project is deployed on Streamlit Cloud. To deploy your own version:
1. Fork this repository on GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and sign in.
3. Click **Deploy an app** and point it to your forked repository and `main.py`.
4. Customize your app settings (title, description, logo), then click **Deploy**.

## Dependencies

- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly

