import streamlit as st
st.set_page_config(page_title="Financial Ratios Dashboard", layout="wide")

from modules.data_loader import rop_ratios, ame_ratios, ftv_ratios, rop_balance_sheet, ame_balance_sheet, ftv_balance_sheet, fetch_financial_data
import pandas as pd
import plotly.graph_objs as go

# Call the fetch_financial_data function to fetch the data
rop_ratios, rop_balance_sheet_ratios, rop_balance_sheet = fetch_financial_data('ROP')
ame_ratios, ame_balance_sheet_ratios, ame_balance_sheet = fetch_financial_data('AME')
ftv_ratios, ftv_balance_sheet_ratios, ftv_balance_sheet = fetch_financial_data('FTV')

rop_year_colors = ['#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4']  # Shades of blue
ame_year_colors = ['#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#F44336']  # Shades of red
ftv_year_colors = ['#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50']  # Shades of green

# Create a container for the header
header = st.container()

with header:
    st.title("Financial Ratios Dashboard")
    st.markdown("""
    This dashboard allows you to visualize and compare financial ratios for three companies: Roper Technologies, AMETEK, and FortiveCorps.
    """)

# Create columns
col1, col2, col3 = st.columns(3)

# Create a container for the user inputs
user_inputs = st.sidebar.container()

with user_inputs:
    st.header("User Inputs")
    selected_year_range = st.slider(
        "Select Year Range",
        min_value=2019,
        max_value=2023,
        value=(2019, 2023),
        step=1,
    )
    selected_ratio = st.radio(
        "Select Ratio",
        options=["Gross Profit Margin", "Net Profit Margin", "Return on Assets", "Return on Equity"],
        index=0,
    )
    view_type = st.radio(
        "View Type",
        options=["Financial Ratios", "Profitability Ratios", "Current Assets vs. Current Liabilities", "Total Assets vs. Total Liabilities"],
        index=0,
    )

# Create a container for the chart
chart_container = st.container()

# Filter data based on selected year range
filtered_years = list(range(selected_year_range[0], selected_year_range[1] + 1))

# Financial Ratios Chart
if view_type == "Financial Ratios":
    with chart_container:
        data = []
        for idx, year in enumerate(filtered_years):
            rop_ratio_value = rop_ratios.get(str(year), {}).get(selected_ratio.lower().replace(" ", "_"), None)
            ame_ratio_value = ame_ratios.get(str(year), {}).get(selected_ratio.lower().replace(" ", "_"), None)
            ftv_ratio_value = ftv_ratios.get(str(year), {}).get(selected_ratio.lower().replace(" ", "_"), None)

            if rop_ratio_value is not None and ame_ratio_value is not None and ftv_ratio_value is not None:
                data.append(
                    go.Bar(
                        x=['Roper Technologies', 'AMETEK', 'FortiveCorps'],
                        y=[rop_ratio_value, ame_ratio_value, ftv_ratio_value],
                        name=str(year),
                        marker_color=[rop_year_colors[idx % len(rop_year_colors)],
                                    ame_year_colors[idx % len(ame_year_colors)],
                                    ftv_year_colors[idx % len(ftv_year_colors)]],
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
                y=1,
                traceorder='reversed',
                bgcolor='rgba(255, 255, 255, 0.5)',
                bordercolor='#333333',
                borderwidth=2,
                font=dict(size=12, color='#333333')
            ),
            annotations=[
                dict(
                    x=0,
                    y=1.07,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    text='Roper Technologies',
                    font=dict(size=14, color='#6495ED')
                ),
                dict(
                    x=1,
                    y=1.07,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    text='AMETEK',
                    font=dict(size=14, color='#DC143C')
                ),
                dict(
                    x=2,
                    y=1.07,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    text='FortiveCorps',
                    font=dict(size=14, color='#008000')
                )
            ]
        )

        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

# Profitability Ratios Chart
elif view_type == "Profitability Ratios":
    with chart_container:
        profitability_ratios_data = []

        for year in filtered_years:
            rop_ratios_row = [rop_ratios.get(str(year), {}).get('gross_profit_margin', None),
                               rop_ratios.get(str(year), {}).get('operating_profit_margin', None),
                               rop_ratios.get(str(year), {}).get('ebitda_margin', None),
                               rop_ratios.get(str(year), {}).get('net_profit_margin', None)]

            ame_ratios_row = [ame_ratios.get(str(year), {}).get('gross_profit_margin', None),
                               ame_ratios.get(str(year), {}).get('operating_profit_margin', None),
                               ame_ratios.get(str(year), {}).get('ebitda_margin', None),
                               ame_ratios.get(str(year), {}).get('net_profit_margin', None)]

            ftv_ratios_row = [ftv_ratios.get(str(year), {}).get('gross_profit_margin', None),
                               ftv_ratios.get(str(year), {}).get('operating_profit_margin', None),
                               ftv_ratios.get(str(year), {}).get('ebitda_margin', None),
                               ftv_ratios.get(str(year), {}).get('net_profit_margin', None)]

            if all(ratio is not None for ratio in rop_ratios_row + ame_ratios_row + ftv_ratios_row):
                profitability_ratios_data.append(
                    go.Bar(
                        x=['Roper Technologies', 'AMETEK', 'FortiveCorps'],
                        y=[rop_ratios_row, ame_ratios_row, ftv_ratios_row],
                        name=str(year),
                        marker_color=[rop_year_colors[filtered_years.index(year)],
                                      ame_year_colors[filtered_years.index(year)],
                                      ftv_year_colors[filtered_years.index(year)]],
                        hovertemplate='Company: %{x}<br>Year: %{name}<br>Gross Profit Margin: %{y[0]:.2f}<br>Operating Profit Margin: %{y[1]:.2f}<br>EBITDA Margin: %{y[2]:.2f}<br>Net Profit Margin: %{y[3]:.2f}<extra></extra>'
                    )
                )

        profitability_ratios_layout = go.Layout(
            title=dict(text='Profitability Ratios', font=dict(size=24, color='#333333')),
            height=600,
            width=800,
            barmode='group',
            xaxis=dict(title='Company', tickfont=dict(size=14, color='#333333')),
            yaxis=dict(title='Ratio Value', tickfont=dict(size=14, color='#333333')),
            legend=dict(title='Year', x=1, y=1, traceorder='reversed', bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='#333333', borderwidth=2, font=dict(size=12, color='#333333'))
        )

        profitability_ratios_fig = go.Figure(data=profitability_ratios_data, layout=profitability_ratios_layout)
        st.plotly_chart(profitability_ratios_fig, use_container_width=True)

elif view_type == "Current Assets vs. Current Liabilities":
    with chart_container:
        # Use a consistent color scheme for assets and liabilities
        colors = {'assets': 'blue', 'liabilities': 'red'}

        # Dropdown to select a specific year from the filtered range
        selected_year = st.selectbox("Select Year", filtered_years)

        # Data lists for plotting
        assets_data = []
        liabilities_data = []

        # Dictionary for each company's balance sheet
        company_balance_sheets = {
            'Roper Technologies': rop_balance_sheet,
            'AMETEK': ame_balance_sheet,
            'FortiveCorps': ftv_balance_sheet
        }

        # Log current assets and liabilities for debugging
        st.write("Current Assets and Liabilities Data (for debugging):")
        
        # Compute current assets and liabilities for each company for the selected year
        for company, balance_sheet in company_balance_sheets.items():
            # Get the balance sheet for the selected year
            year_data = balance_sheet.get(str(selected_year), {})
            
            # Calculate current assets and current liabilities
            current_assets = year_data.get('cashAndCashEquivalents', 0) + \
                             year_data.get('netReceivables', 0) + \
                             year_data.get('inventory', 0)
            current_liabilities = year_data.get('totalCurrentLiabilities', 0)

            # Log the values
            st.write(f"{company} - {selected_year}: Assets: {current_assets}, Liabilities: {current_liabilities}")

            # Append the values to the lists for plotting
            assets_data.append(go.Bar(x=[company], y=[current_assets], name='Current Assets', marker_color=colors['assets']))
            liabilities_data.append(go.Bar(x=[company], y=[current_liabilities], name='Current Liabilities', marker_color=colors['liabilities']))

        # Create the Plotly figure
        fig = go.Figure(data=assets_data + liabilities_data)
        fig.update_layout(
            barmode='group',
            title=f"Current Assets vs. Current Liabilities ({selected_year})",
            xaxis_title="Company",
            yaxis_title="Value ($)",
            legend_title_text='Metric',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Display the figure in the Streamlit container
        st.plotly_chart(fig, use_container_width=True)


# Total Assets vs. Total Liabilities
elif view_type == "Total Assets vs. Total Liabilities":
    with chart_container:
        for year in filtered_years:
            rop_total_assets = rop_balance_sheet.get(str(year), {}).get('totalAssets', 0)
            rop_total_liabilities = rop_balance_sheet.get(str(year), {}).get('totalLiabilities', 0)

            ame_total_assets = ame_balance_sheet.get(str(year), {}).get('totalAssets', 0)
            ame_total_liabilities = ame_balance_sheet.get(str(year), {}).get('totalLiabilities', 0)

            ftv_total_assets = ftv_balance_sheet.get(str(year), {}).get('totalAssets', 0)
            ftv_total_liabilities = ftv_balance_sheet.get(str(year), {}).get('totalLiabilities', 0)

            data = [
                go.Bar(x=['Roper Technologies'], y=[rop_total_assets], name='Total Assets', marker_color='#4FC3F7'),
                go.Bar(x=['Roper Technologies'], y=[rop_total_liabilities], name='Total Liabilities', marker_color='#03A9F4'),
                go.Bar(x=['AMETEK'], y=[ame_total_assets], name='Total Assets', marker_color='#EF9A9A'),
                go.Bar(x=['AMETEK'], y=[ame_total_liabilities], name='Total Liabilities', marker_color='#F44336'),
                go.Bar(x=['FortiveCorps'], y=[ftv_total_assets], name='Total Assets', marker_color='#A5D6A7'),
                go.Bar(x=['FortiveCorps'], y=[ftv_total_liabilities], name='Total Liabilities', marker_color='#4CAF50')
            ]

            fig = go.Figure(data=data)
            fig.update_layout(barmode='group', xaxis_tickangle=-45, title=f"Total Assets vs. Total Liabilities ({year})",
                              xaxis_title="Company", yaxis_title="Value ($)")
            st.plotly_chart(fig, use_container_width=True)

# Define colors in increasing order of contrast and brightness
