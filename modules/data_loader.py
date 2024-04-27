import requests
import pandas as pd

API_KEY = "Pznigh25tSpIit6nctNSkzK0IRtXUZDB"
companies = ['ROP', 'AME', 'FTV']

# Initialize dictionaries to store financial ratios and balance sheet data for each company and year
rop_ratios = {}
ame_ratios = {}
ftv_ratios = {}
rop_balance_sheet = {}
ame_balance_sheet = {}
ftv_balance_sheet = {}

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