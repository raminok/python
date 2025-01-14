# Extracting and Visualizing Stock Data
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# Define the ticker symbol for Tesla
ticker_symbol = "TSLA"

# Create a ticker object using the ticker symbol
tesla_ticker = yf.Ticker(ticker_symbol)

# Print the ticker object (optional)
print(tesla_ticker) 


# Reset the index 
tesla_data.reset_index(inplace=True)

tesla_data = tesla_ticker.history(period="max")
print(tesla_data.head()) 

# Define the URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send a GET request to the URL
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Extract the HTML content from the response
    html_data = response.text

    # Parse the HTML content using BeautifulSoup with 'html.parser'
    soup = BeautifulSoup(html_data, 'html.parser')

    # Use pandas read_html to extract the table
    tesla_revenue = pd.read_html(str(soup), match='Tesla Quarterly Revenue', flavor='bs4')[0]

    # Rename columns to 'Date' and 'Revenue'
    tesla_revenue.columns = ['Date', 'Revenue']

    # Display the first 5 rows
    print(tesla_revenue.head())

else:
    print(f"Failed to download webpage. Status code: {response.status_code}")

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# Define the URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send a GET request to the URL
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Extract the HTML content from the response
    html_data = response.text

    # Parse the HTML content using BeautifulSoup with 'html.parser'
    soup = BeautifulSoup(html_data, 'html.parser')

    # Use pandas read_html to extract the table
    tesla_revenue = pd.read_html(str(soup), match='Tesla Quarterly Revenue', flavor='bs4')[0]

    # Rename columns to 'Date' and 'Revenue'
    tesla_revenue.columns = ['Date', 'Revenue']

    # Display the last 5 rows
    print(tesla_revenue.tail())

else:
    print(f"Failed to download webpage. Status code: {response.status_code}")


