import base64
import requests
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import streamlit as st

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
    
    return financial_ratios


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def display_company_info(company, financial_ratios):
    """
    Generate and display HTML content for each company's financial ratios.
    """
    if company == "AME":
        logo_base64 = "data:image/jpeg;base64,{AME_LOGO_BASE64}"
    elif company == "FTV":
        logo_base64 = "data:image/png;base64,{FTV_LOGO_BASE64}"
    elif company == "ROP":
        logo_base64 = "data:image/png;base64,{ROP_LOGO_BASE64}"
    else:
        logo_base64 = ""

    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 8px; padding: 15px; width: 300px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); background-color: #f9f9f9;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="{logo_base64}" alt="{company} Logo" style="width: 60px; height: 50px; margin-right: 20px;">
            <span style="font-size: 20px; font-weight: bold;">{company}</span>
        </div>
        <div style="font-size: 14px;">
            Current Ratio: {format_ratio(financial_ratios[company]['currentRatio'])}<br>
            Gross Profit Margin: {format_ratio(financial_ratios[company]['grossProfitMargin'])}<br>
            Return on Equity: {format_ratio(financial_ratios[company]['returnOnEquity'])}<br>
            Debt to Equity Ratio: {format_ratio(financial_ratios[company]['debtEquityRatio'])}<br>
            P/E Ratio: {format_ratio(financial_ratios[company]['priceEarningsRatio'])}<br>
            FCF per Share: {format_ratio(financial_ratios[company]['freeCashFlowPerShare'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

