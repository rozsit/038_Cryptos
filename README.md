# <p align="center">Cryptocurrency Dashboard</p>

## Overview
The Cryptocurrency Dashboard is an interactive web application that visualizes real-time data for selected cryptocurrencies. It allows users to view price trends, monitor the volume of trades, and export data in Excel format. The dashboard is built using Dash and Plotly for visualizations, and it fetches cryptocurrency data using the yfinance library.

## Features
- Real-time Price Monitoring: View the closing prices of selected cryptocurrencies over various time periods.
- Volume Visualization: Monitor the trading volume for selected cryptocurrencies over time.
- Interactive Charts: Price and volume data are displayed as area and bar charts, respectively, for selected cryptocurrencies and time ranges, also included chart export to .png file.
- Data Export: Download cryptocurrency data (prices and volumes) in Excel format.
- Responsive Design: The layout is responsive and works well across different devices and screen sizes.

## Technologies Used
- Python 3.12.1
- Dash: A web framework for Python built on top of Flask, Plotly, and React.js.
- Plotly: For creating interactive charts.
- yfinance: For fetching real-time cryptocurrency data from Yahoo Finance.
- Pandas: For data manipulation and exporting data to Excel.
- XlsxWriter: For writing data to Excel files.
