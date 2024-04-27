import streamlit as st
from function import companies,api_key, fetch_financial_data, fetch_financial_statements, plot_ratios, calculate_financial_ratios
import pandas as pd
import plotly.graph_objs as go
from function import company_colors,display_cash_flow_charts, fetch_stock_data,plot_stock_data
from test import get_stock_price, setup_ui,set_layout,load_data,format_ratio,display_company_info
import streamlit.components.v1 as components

from datetime import datetime
st.set_page_config(layout='wide')


# Update placeholders with your actual content

financial_ratios_text = "This section will display key financial ratios calculated from the company's financial data."
current_liabilities_text = "This section will analyze the company's current assets in relation to current liabilities."
cash_flow_text = "This section will delve into the company's cash flow and its impact on financial health."
historical_analysis_text = "This section will present historical stock analysis, including price trends and other relevant data."



# Sidebar options
options = ["Overview", "Financial Ratios", "Cash Flow Analysis", "Historical Stock Analysis"]
selected_option = st.sidebar.selectbox("Select a view:", options)



# Display content based on selection
if selected_option == "Overview":
    
    # Read the HTML file
    canva_url = "https://www.canva.com/design/DAGDkE2TLXg/fnkWFkwMBtvTQ2U4HotRVw/view?embed"
    # Adjust width and height for better visibility and layout fit
    components.html(f'<iframe src="{canva_url}" width="100%" height="800" style="border:none;"></iframe>', height=800,width= 900)


elif selected_option == "Financial Ratios":
    set_layout()
    financial_ratios, logos = load_data()
    companies = ["AME", "FTV", "ROP"]
    col1, col2, col3 = st.columns(3)

    for i, company in enumerate(financial_ratios):
        if i % 3 == 0:
            with col1:
                display_company_info(company, financial_ratios, logos[company])
        elif i % 3 == 1:
            with col2:
                display_company_info(company, financial_ratios, logos[company])
        else:
            with col3:
                display_company_info(company, financial_ratios, logos[company])
        
    # Additional analyses or conclusion
    st.write("--")
    st.markdown("""
    This section provides a detailed comparison of key financial ratios across AME, FTV, and ROP. Enhanced visual representation with styled boxes helps users quickly assess the financial health and profitability of these companies.
    """)
    st.header("Financial Ratios")
    financial_ratios_text = "Here are the financial ratios that help assess the financial health of selected companies."
    st.write(financial_ratios_text)
    # Fetch financial data and calculate ratios
    financial_data = {company: fetch_financial_statements(api_key, company, 2019, 2024) for company in companies}
    financial_ratios = {company: calculate_financial_ratios(data) for company, data in financial_data.items()}
        
     # Plot the ratios using Plotly
    plot_ratios(financial_ratios, company_colors)
    

elif selected_option == "Cash Flow Analysis":
    # Add calculations and display of cash flow here
    setup_ui()
    display_cash_flow_charts('ame_cash.csv', 'ftv_cash.csv', 'rop_cash.csv')
    # Conclusion or additional analyses
    st.markdown("""
    This dashboard allows users to compare the financial growth rates of AME, FTV, and ROP across various metrics.
    Select different metrics from the dropdown to see the comparative growth bars. Analyze how each company is performing in terms of revenue and cash flow management, helping in making informed investment or analytical decisions.
    """)
elif selected_option == "Historical Stock Analysis":
    st.header("Historical Stock Analysis")
    historical_analysis_text = "This analysis provides an overview of historical closing prices for selected stocks. Below you can see the trend in closing prices over time."
    st.write(historical_analysis_text)
    
    symbols = ['ROP', 'AME', 'FTV']
    chart_type = st.selectbox('Select chart type:', ['Line', 'Candlestick'])
    start_date, end_date = st.date_input("Select date range:", value=[datetime(2020, 1, 1), datetime.now()], min_value=datetime(2015, 1, 1))

    st.plotly_chart(plot_stock_data(symbols, api_key, chart_type, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
