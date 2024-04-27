import requests
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import streamlit as st

companies = ['ROP', 'AME', 'FTV']
api_key = 'MPUo7JToMtlR3e1Z8fxdRV3uerljb8r8'
API_KEY= 'wEusDH25PPRSM6aXtjRMmiuFoAgIzzK9'
company_colors = {
        'ROP': ['#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4'],
        'AME': ['#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#F44336'],
        'FTV': ['#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50']}

from datetime import datetime


def fetch_stock_data(symbol, api_key):
    """Fetch stock data from API and handle potential errors."""
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data['historical']
    except requests.RequestException as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return []

def plot_stock_data(symbols, api_key, chart_type, start_date, end_date):
    """Plot stock data using Plotly for multiple symbols."""
    fig = go.Figure()

    for symbol in symbols:
        historical = fetch_stock_data(symbol, api_key)
        if not historical:
            continue  # Skip this symbol if data could not be fetched
        
        # Filter data based on selected date range
        filtered_data = [item for item in historical if start_date <= item['date'] <= end_date]

        if chart_type == 'Line':
            dates = [item['date'] for item in filtered_data]
            closes = [item['close'] for item in filtered_data]
            fig.add_trace(go.Scatter(x=dates, y=closes, mode='lines', name=symbol))
        elif chart_type == 'Candlestick':
            dates = [item['date'] for item in filtered_data]
            opens = [item['open'] for item in filtered_data]
            highs = [item['high'] for item in filtered_data]
            lows = [item['low'] for item in filtered_data]
            closes = [item['close'] for item in filtered_data]
            fig.add_trace(go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes, name=symbol))

    fig.update_layout(
    title=f'{chart_type} Chart for Multiple Stocks',
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    legend_title='Stock Symbols',
    template='plotly_dark',
    xaxis=dict(rangeslider=dict(visible=True), type='date'),
    # Define the size of the figure
    width=1000,  # Width of the figure in pixels
    height=600,  # Height of the figure in pixels
    margin=dict(l=50, r=50, b=100, t=100, pad=4)  # Adjust margins to make sure titles and labels are visible
)


    return fig


def fetch_financial_data(ticker):
    global rop_ratios, ame_ratios, ftv_ratios, rop_balance_sheet, ame_balance_sheet, ftv_balance_sheet

    balance_sheet_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={API_KEY}"
    balance_sheet_response = requests.get(balance_sheet_url)
    balance_sheet_data = balance_sheet_response.json()

    income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}"
    income_statement_response = requests.get(income_statement_url)
    income_statement_data = income_statement_response.json()

    ratios = {}
    balance_sheet_ratios = {}

    

    for balance_sheet_year_data, income_statement_year_data in zip(balance_sheet_data, income_statement_data):
        year = balance_sheet_year_data['calendarYear']

        gross_profit = income_statement_year_data['grossProfit']
        revenue = income_statement_year_data['revenue']
        net_income = income_statement_year_data['netIncome']
        total_assets = balance_sheet_year_data['totalAssets']
        total_stockholders_equity = balance_sheet_year_data['totalStockholdersEquity']
        operating_income = income_statement_year_data['operatingIncome']
        ebitda = income_statement_year_data['ebitda']

        gross_profit_margin = gross_profit / revenue
        net_profit_margin = net_income / revenue
        return_on_assets = net_income / total_assets
        return_on_equity = net_income / total_stockholders_equity
        operating_profit_margin = operating_income / revenue
        ebitda_margin = ebitda / revenue

        ratios[year] = {
            'gross_profit_margin': gross_profit_margin,
            'net_profit_margin': net_profit_margin,
            'return_on_assets': return_on_assets,
            'return_on_equity': return_on_equity,
            'operating_profit_margin': operating_profit_margin,
            'ebitda_margin': ebitda_margin
        }

        balance_sheet_columns = ['cashAndCashEquivalents', 'netReceivables', 'inventory', 'propertyPlantEquipmentNet']
        balance_sheet_row = {column: balance_sheet_year_data[column] for column in balance_sheet_columns}

        if ticker == 'ROP':
            rop_balance_sheet[year] = balance_sheet_row
        elif ticker == 'AME':
            ame_balance_sheet[year] = balance_sheet_row
        elif ticker == 'FTV':
            ftv_balance_sheet[year] = balance_sheet_row

    if ticker == 'ROP':
        rop_ratios.update(ratios)
        return ratios, balance_sheet_ratios, rop_balance_sheet
    elif ticker == 'AME':
        ame_ratios.update(ratios)
        return ratios, balance_sheet_ratios, ame_balance_sheet
    elif ticker == 'FTV':
        ftv_ratios.update(ratios)
        return ratios, balance_sheet_ratios, ftv_balance_sheet
    


def fetch_financial_statements(api_key, company_symbol, start_year, end_year):
    financial_data = {}
    for year in range(start_year, end_year + 1):
        balance_sheet_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company_symbol}?period=annual&limit=1&apikey={api_key}"
        income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{company_symbol}?period=annual&limit=1&apikey={api_key}"

        balance_sheet_response = requests.get(balance_sheet_url).json()[0]
        income_statement_response = requests.get(income_statement_url).json()[0]

        financial_data[year] = {
            'Balance Sheet': balance_sheet_response,
            'Income Statement': income_statement_response,
        }
    return financial_data

def calculate_financial_ratios(financial_data):
    ratios = {}
    for year, data in financial_data.items():
        balance_sheet = data['Balance Sheet']
        income_statement = data['Income Statement']
        ratios[year] = {
            "Current Ratio": balance_sheet['totalCurrentAssets'] / balance_sheet['totalCurrentLiabilities'],
            "Debt-to-Equity Ratio": balance_sheet['totalDebt'] / balance_sheet['totalStockholdersEquity'],
            "Gross Profit Margin": income_statement['grossProfit'] / income_statement['revenue'],
            "Return on Equity": income_statement['netIncome'] / balance_sheet['totalStockholdersEquity'],
            "Earnings Per Share": income_statement['netIncome'] / income_statement['weightedAverageShsOut'],
        }
    return ratios

def plot_ratios(ratios, company_colors):
    ratios_keys = list(ratios[next(iter(ratios))][next(iter(ratios[next(iter(ratios))]))].keys())
    selected_ratio = st.selectbox('Select a Financial Ratio', ratios_keys)
    
    data = []
    for year in range(2019, 2025):
        year_data = [
            ratios.get(company, {}).get(year, {}).get(selected_ratio, 0) for company in ['ROP', 'AME', 'FTV']
        ]
        data.append(
            go.Bar(
                x=['Roper Technologies', 'AMETEK', 'FortiveCorps'],
                y=year_data,
                name=str(year),
                marker_color=[company_colors['ROP'][(year-2019) % len(company_colors['ROP'])],
                              company_colors['AME'][(year-2019) % len(company_colors['AME'])],
                              company_colors['FTV'][(year-2019) % len(company_colors['FTV'])]],
                hovertemplate='Company: %{x}<br>Year: %{name}<br>Ratio: %{y:.2f}<extra></extra>'
            )
        )
    
    layout = go.Layout(
        title=dict(
            text=f'Financial Ratios Dashboard - {selected_ratio}',
            font=dict(size=24, color='#333333')
        ),
        height=600,
        width=800,
        barmode='group',
        xaxis=dict(
            title='Company',
            tickfont=dict(size=14, color='#333333')
        ),
        yaxis=dict(
            title='Ratio',
            tickfont=dict(size=14, color='#333333')
        ),
        legend=dict(
            x=1,
            y=1.1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='#333333',
            borderwidth=2,
            font=dict(size=12, color='#333333')
        )
    )
    
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)





def clean_column_names(df):
    df.columns = [col.strip() for col in df.columns]
    return df

def display_cash_flow_charts(ame_cash_path, ftv_cash_path, rop_cash_path):
    # Read the CSV files and clean column names
    ame_cash = clean_column_names(pd.read_csv(ame_cash_path))
    ftv_cash = clean_column_names(pd.read_csv(ftv_cash_path))
    rop_cash = clean_column_names(pd.read_csv(rop_cash_path))

    # Convert calendarYear to int (handle non-numeric values)
    ame_cash['calendarYear'] = pd.to_numeric(ame_cash['calendarYear'], errors='coerce')
    ftv_cash['calendarYear'] = pd.to_numeric(ftv_cash['calendarYear'], errors='coerce')
    rop_cash['calendarYear'] = pd.to_numeric(rop_cash['calendarYear'], errors='coerce')

    # Get unique years
    ame_years = ame_cash['calendarYear'].dropna().unique().astype(int).tolist()
    ftv_years = ftv_cash['calendarYear'].dropna().unique().astype(int).tolist()
    rop_years = rop_cash['calendarYear'].dropna().unique().astype(int).tolist()
    years = sorted(list(set(ame_years + ftv_years + rop_years)))

    # Create a dropdown menu for selecting the year
    selected_year = st.sidebar.selectbox("Select Year", years, index=len(years) - 1)

    # Create a dropdown menu for selecting the cash flow activity
    activity_options = ['Cash Flow from Operations', 'Cash Flow from Investing', 'Cash Flow from Financing']
    selected_activity = st.sidebar.selectbox("Select Cash Flow Activity", activity_options)

    # Filter data based on selected year
    ame_cash_filtered = ame_cash[ame_cash['calendarYear'] == selected_year]
    ftv_cash_filtered = ftv_cash[ftv_cash['calendarYear'] == selected_year]
    rop_cash_filtered = rop_cash[rop_cash['calendarYear'] == selected_year]

    # Calculate cash flow activities for the selected year and activity
    ame_activities = {selected_activity: calculate_activities(ame_cash_filtered, selected_activity)}
    ftv_activities = {selected_activity: calculate_activities(ftv_cash_filtered, selected_activity)}
    rop_activities = {selected_activity: calculate_activities(rop_cash_filtered, selected_activity)}

    # Create bar chart
    fig = go.Figure()

    if ame_activities[selected_activity]:
        fig.add_trace(go.Bar(x=['AME'], y=[ame_activities[selected_activity]], name='AME'))
    else:
        st.warning("No data available for AME in the selected year and activity.")

    if ftv_activities[selected_activity]:
        fig.add_trace(go.Bar(x=['FTV'], y=[ftv_activities[selected_activity]], name='FTV'))
    else:
        st.warning("No data available for FTV in the selected year and activity.")

    if rop_activities[selected_activity]:
        fig.add_trace(go.Bar(x=['ROP'], y=[rop_activities[selected_activity]], name='ROP'))
    else:
        st.warning("No data available for ROP in the selected year and activity.")

    if not ame_activities[selected_activity] and not ftv_activities[selected_activity] and not rop_activities[selected_activity]:
        st.error("No data available for any company in the selected year and activity.")
        return

    fig.update_layout(title_text=f'{selected_activity} ({selected_year})', title_x=0.5, font=dict(size=16),
                      barmode='group', xaxis_tickangle=0, height=600, width=1200)

    # Display the chart using Streamlit
    st.subheader('Cash Flow Analysis')
    st.plotly_chart(fig, use_container_width=True)

def calculate_activities(df, activity):
    if activity == 'Cash Flow from Operations':
        return df['netCashProvidedByOperatingActivities'].sum()
    elif activity == 'Cash Flow from Investing':
        return df['netCashUsedForInvestingActivites'].sum()
    elif activity == 'Cash Flow from Financing':
        return df['netCashUsedProvidedByFinancingActivities'].sum()
    else:
        return 0
