import streamlit as st
import pandas as pd
import requests

# Function to fetch the latest stock price and the change
def get_stock_price(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'historical' in data and len(data['historical']) > 0:
        latest_close = data['historical'][0]['close']
        previous_close = data['historical'][1]['close'] if len(data['historical']) > 1 else latest_close
        # Calculate the percentage change
        delta = ((latest_close - previous_close) / previous_close) * 100 if previous_close != 0 else 0
        return latest_close, delta
    else:
        return None, None

# Function to setup Streamlit UI
def setup_ui():
    st.title('Financial Growth Comparison and cash flow overview')
    st.subheader("This section will delve into the company's cash flow and its impact on financial health.")
    # API key (replace 'your_api_key' with your actual Financial Modeling Prep API key)
    api_key = 'Pznigh25tSpIit6nctNSkzK0IRtXUZDB'

    # Define your data (normally you would load this from a data source)
    data = {
        "Company": ["AME", "FTV", "ROP"],
        "Mean growthNetIncome": [0.11, 0.12, 0.17],
        "Mean growthOperatingCashFlow": [0.15, 0.03, 0.30],
        "Mean growthFreeCashFlow": [0.16, 0.03, 0.33],
        "Mean growthNetCashProvidedByOperatingActivities": [0.15, 0.03, 0.30],
        "Mean growthNetChangeInCash": [13.51, 6.24, 1.60]
    }

    df = pd.DataFrame(data)

    # Define your data
    data2 = {
        "Company": ["AME", "FTV", "ROP"],
        "Symbols": ["AME", "FTV", "ROP"],  # Replace with actual stock symbols
        "Logo": ["logo2.jpeg", "logo3.png", "logo1.png"]  # Add correct logo file paths
    }

    df2 = pd.DataFrame(data2)

    # Define columns for layout
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    # Loop to create a column for each company
    for idx, row in df2.iterrows():
        with columns[idx]:
            st.image(row['Logo'], width=100)  # Adjust width to fit your layout
            st.subheader(row['Company'])
            price, delta = get_stock_price(row['Symbols'], api_key)
            if price is not None:
                delta_symbol = "🔼" if delta > 0 else "🔽"
                st.metric(label="Stock Price", value=f"${price:.2f}", delta=f"{delta:.2f}% {delta_symbol}")
            else:
                st.metric(label="Stock Price", value="N/A", delta="No data")

    # Display the data
    st.dataframe(df.set_index('Company'))




def set_layout():
    """ Set page configuration. """
    
    st.title('Financial Ratios Comparison and Overview')

def load_data():
    """ Load financial ratios and logos for companies. """
    financial_ratios = {
        "AME": {
            "currentRatio": 1.54,
            "grossProfitMargin": 0.35,
            "returnOnEquity": 0.15,
            "debtEquityRatio": 0.40,
            "priceEarningsRatio": 29.83,
            "freeCashFlowPerShare": 5.11
        },
        "FTV": {
            "currentRatio": 1.24,
            "grossProfitMargin": 0.56,
            "returnOnEquity": 0.10,
            "debtEquityRatio": 0.50,
            "priceEarningsRatio": 29.58,
            "freeCashFlowPerShare": 3.40
        },
        "ROP": {
            "currentRatio": 0.70,
            "grossProfitMargin": 0.67,
            "returnOnEquity": 0.10,
            "debtEquityRatio": 0.59,
            "priceEarningsRatio": 40.33,
            "freeCashFlowPerShare": 14.09
        }
    }
    logos = {
        "AME": "logo2.jpeg",
        "FTV": "logo3.png",
        "ROP": "logo1.png"
    }
    return financial_ratios, logos

def format_ratio(ratio):
    """ Format the ratio value with arrows indicating increase or decrease. """
    arrow = "🔼" if ratio > 0 else "🔽"
    return f"{ratio:.2f} {arrow}" if ratio != 0 else f"{ratio:.2f}"

def display_company_info(company, financial_ratios, logo_path):
    """
    Display company information with logo and financial ratios.
    """
    with st.expander(f"{company} - Financial Ratios", expanded=True):
        st.image(logo_path, width=60)
        st.markdown(f"<span style='font-size: 20px; font-weight: bold;'>{company}</span>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="font-size: 14px;">
            Current Ratio: {format_ratio(financial_ratios[company]['currentRatio'])}<br>
            Gross Profit Margin: {format_ratio(financial_ratios[company]['grossProfitMargin'])}<br>
            Return on Equity: {format_ratio(financial_ratios[company]['returnOnEquity'])}<br>
            Debt to Equity Ratio: {format_ratio(financial_ratios[company]['debtEquityRatio'])}<br>
            P/E Ratio: {format_ratio(financial_ratios[company]['priceEarningsRatio'])}<br>
            FCF per Share: {format_ratio(financial_ratios[company]['freeCashFlowPerShare'])}
        </div>
        """, unsafe_allow_html=True)
