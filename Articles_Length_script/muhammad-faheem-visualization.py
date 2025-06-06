import pandas as pd
import plotly.express as px

#Load the CSV file
df = pd.read_csv("data/dataframes/length/length.csv")

#Line plotting the monthly average article lengths and combining 
monthly_avg = df.groupby(['year', 'month'])['length'].mean().reset_index()                 #used chatgpt for this line of code
monthly_avg['year_month'] = monthly_avg['year'].astype(str) + '-' + monthly_avg['month'].astype(str).str.zfill(2)

fig1 = px.line(
    monthly_avg,
    x='year_month',
    y='length',
    title='Average Article Length by Month',
    labels={'length': 'Average Length (words)', 'year_month': 'Month'}
)
fig1.write_html("outputs/muhammad-faheem-monthly-avg-lengths.html")

#Box plot the distribution of article lengths by year
fig2 = px.box(
    df,
    x='year',
    y='length',
    title='Distribution of Article Lengths by Year',
    labels={'length': 'Article Length (words)', 'year': 'Year'}
)
fig2.write_html("outputs/muhammad-faheem-yearly-length-dist.html")

#Box plot monthly distributions by year 
df['month_name'] = pd.to_datetime(df['month'], format='%m').dt.month_name()    #this line of code is taken from chatgpt because of mentioning months in numeric instead of names

fig3 = px.box(
    df,
    x='month_name',
    y='length',
    facet_col='year',
    title='Monthly Length Distributions by Year',
    category_orders={'month_name': [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]},
    labels={'length': 'Article Length (words)', 'month_name': 'Month'}
)
fig3.write_html("outputs/muhammad-faheem-monthly-dist-by-year.html")

