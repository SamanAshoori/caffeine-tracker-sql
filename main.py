#This code assumes you use my data scheme to create the sql to load it into here properly
#I use this and the index.html (which I embed onto my main website)

import json
import pandas as pd
import plotly
import plotly.express as px
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# Database connection
DATABASE_URL = 'INSERT OWN STUFF HERE PAL - NOT GIVING YOU MY SQL DATABASE THATS FOR SURE'


def get_data():
    conn = psycopg2.connect(DATABASE_URL)
    query = """
    SELECT 
    DATE_TRUNC('week', t.transactiondate) AS week_start, 
    t.drinkid,
    d.drinkname,
    b.brandname,
    SUM(t.transactioncost) AS total_cost,
    COUNT(t.transactionid) AS transaction_count
    FROM transaction t
    JOIN drink d ON t.drinkid = d.drinkid
    JOIN brand b ON d.brandid = b.brandid
    GROUP BY week_start, t.drinkid, d.drinkname, b.brandname
    ORDER BY week_start, t.drinkid;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def get_transactiondata():
    conn = psycopg2.connect(DATABASE_URL)
    query ="""
    SELECT 
    transactionid, 
    drinkid, 
    transactiondate 
    FROM transaction;
    """
    df_transactions = pd.read_sql_query(query, conn)
    conn.close()
    return df_transactions
def get_drinkdata():
    conn = psycopg2.connect(DATABASE_URL)
    query ="""
    SELECT 
    drinkid, 
    drinkcaffeine 
    FROM drink;
    """
    df_drinks = pd.read_sql_query(query, conn)
    conn.close()
    return df_drinks
@app.route('/')
def index():
    df = get_data()
    df_transactions = get_transactiondata()
    df_drinks = get_drinkdata()

    df['drinkid'] = df['drinkid'].astype(str)

    # Prepare data for the pie chart (sum transactions per drink)
    total_transactions = df.groupby('drinkid', as_index=False).agg(
        total_count=('transaction_count', 'sum'),
        drinkname=('drinkname', 'first'),
        brandname=('brandname', 'first')
    )

    # Create bar chart
    fig_bar = px.bar(
        df,
        x='week_start',
        y='total_cost',
        color='drinkid',
        title='Weekly Transaction Cost by Drink',
        labels={'total_cost': "Total Cost (£)", 'week_start': "Week Start"},
        color_discrete_map={str(k): v for k, v in custom_colors.items()},
        hover_data=['drinkname', 'brandname']
    )

    # Add dark mode layout to the bar chart
    fig_bar.update_layout(
        plot_bgcolor='#121212',  # Dark background
        paper_bgcolor='#121212',  # Dark background
        font=dict(color='#e0e0e0'),  # Light text
        xaxis=dict(gridcolor='#333'),  # Dark grid lines
        yaxis=dict(gridcolor='#333'),  # Dark grid lines
        yaxis_tickprefix="£"
    )

    # Create pie chart
    fig_pie = px.pie(
        total_transactions,
        names='drinkname',
        values='total_count',
        title='Total Transactions by Drink',
        color='drinkid',
        color_discrete_map={str(k): v for k, v in custom_colors.items()},
    )

    # Add dark mode layout to the pie chart
    fig_pie.update_layout(
        plot_bgcolor='#121212',  # Dark background
        paper_bgcolor='#121212',  # Dark background
        font=dict(color='#e0e0e0'),  # Light text
    )

    # Merge transaction and drink data for caffeine calculation
    df_merged = pd.merge(df_transactions, df_drinks, on='drinkid', how='left')
    df_merged['total_caffeine'] = df_merged['drinkcaffeine']
    total_caffeine_consumed = df_merged['total_caffeine'].sum()

    # Convert figures to JSON
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_pie = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html', 
        graphJSON_bar=graphJSON_bar, 
        graphJSON_pie=graphJSON_pie,
        total_caffeine_consumed=total_caffeine_consumed
    )

@app.after_request
def add_headers(response):
    # Allow embedding from any site
    response.headers['Content-Security-Policy'] = "frame-ancestors *;"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
