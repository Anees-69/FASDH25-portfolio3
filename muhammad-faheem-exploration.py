import pandas as pd
import plotly.express as px

#Load the csv file  
df = pd.read_csv("data/dataframes/length/length.csv")

#Your original analysis code 
print(df['length'])

#find the length of the longest article
max_length = df['length'].max()

#filter the rows with max length 
longest_article = df[df['length'] == max_length]

#print the title of the longest article
print(longest_article['length'].values[0])

#print the sum of all article length
print("total length of articles:", df['length'].sum())

#export the top 20 longest articles
top20 = df.sort_values(by='length', ascending=False).head(20)
#arrange the articles from bt length from longest to shortest and keep the top 20 longest ones
top20.to_csv('outputs/muhammad-faheem-top20.csv',index=False)

#Combine the year, month and day into a new columns as of year, month and date  
df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-' + df['day'].astype(str).str.zfill(2)

#export aall the articles that were written in the first 6 months of 2023
six_months_2023 = df[(df['year'] == 2023) & (df['month'] <= 6)]
six_months_2023.to_csv('outputs/muhammad-faheem.csv', index=False)
